#!/usr/bin/env python3
"""Chrome QA for the external SVG artwork and its responsive essay layout.

Runs without credentials. Each explanatory figure is rendered in a real browser; SVG labels are
checked for clipping and a contact sheet preserves visual QA.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from PIL import Image, ImageOps, ImageDraw
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementClickInterceptedException

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "essays/why-cant-a-turing-machine-predict-its-own-death.html"
ASSETS = ROOT / "assets/essays/halting-paradox"
FIGURES = ("prediction", "waiting", "repeated-state")


def check_article(browser, width: int, height: int, output: Path) -> None:
    browser.set_window_size(width, height)
    browser.get(ARTICLE.as_uri())
    WebDriverWait(browser, 15).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, ".hl-min-figure img")) == len(FIGURES)
    )
    # Lazy-loaded SVGs below the fold are intentionally incomplete until
    # scrolled into view. Visit all figures before checking natural dimensions.
    for figure in browser.find_elements(By.CSS_SELECTOR, ".hl-min-figure"):
        browser.execute_script(
            "arguments[0].scrollIntoView({block:'center',behavior:'instant'});",
            figure
        )
        img = figure.find_element(By.TAG_NAME, "img")
        WebDriverWait(browser, 10).until(
            lambda d: d.execute_script(
                "return arguments[0].complete && arguments[0].naturalWidth > 0;",
                img
            )
        )
    result = browser.execute_script("""
      const problems = [];
      const figures = [...document.querySelectorAll('.hl-min-figure')];
      for (const [i, figure] of figures.entries()) {
        const img = figure.querySelector('img');
        const rect = img.getBoundingClientRect();
        const caption = figure.querySelector('figcaption');
        if (!img.complete || img.naturalWidth !== 720 || img.naturalHeight < 200)
          problems.push('Figure '+(i+1)+' did not load or has wrong natural dimensions');
        if (rect.width > innerWidth + 2)
          problems.push('Figure '+(i+1)+' overflows viewport');
        if (Math.abs(rect.height - rect.width * img.naturalHeight / img.naturalWidth) > 3)
          problems.push('Figure '+(i+1)+' is distorted');
        if (!caption || caption.querySelector('svg,rect,path,text'))
          problems.push('Figure '+(i+1)+' caption invalid');
        if (!figure.classList.contains('zoomable') ||
            figure.getAttribute('role') !== 'button' ||
            figure.getAttribute('tabindex') !== '0')
          problems.push('Figure '+(i+1)+' lacks accessible native zoom');
      }
      const cover = document.querySelector('img.visual-intro');
      if (!cover || !cover.complete || !cover.naturalWidth)
        problems.push('Cover did not load');
      if (document.documentElement.scrollWidth > innerWidth + 4)
        problems.push('Document-level horizontal overflow');
      return { problems, count: figures.length, viewport: innerWidth,
               pageWidth: document.documentElement.scrollWidth };
    """)
    if result["problems"]:
        raise AssertionError(f"{width}px: {result['problems']}")
    details = browser.find_element(By.CSS_SELECTOR, "#prediction-experiment > summary")
    browser.execute_script("arguments[0].scrollIntoView({block:'center',behavior:'instant'});", details)
    details.click()
    for guess, expected in (("halts", "D runs forever"), ("loops", "D halts")):
        button = browser.find_element(By.CSS_SELECTOR, f'[data-prediction="{guess}"]')
        browser.execute_script(
            "arguments[0].scrollIntoView({block:'center',behavior:'instant'});", button
        )
        try:
            button.click()
        except ElementClickInterceptedException:
            browser.execute_script("arguments[0].click();", button)
        outcome = browser.find_element(By.ID, "fate-output").text
        if expected not in outcome:
            raise AssertionError(f"Interactive scenario {guess} returned {outcome!r}")

    # The existing site script makes figures keyboard-zoomable. Verify the
    # same viewer rather than adding a competing link or nested button.
    central = browser.find_elements(By.CSS_SELECTOR, ".hl-min-figure")[0]
    browser.execute_script(
        "arguments[0].scrollIntoView({block:'center',behavior:'instant'});", central
    )
    browser.execute_script("arguments[0].click();", central)
    modal = browser.find_element(By.CSS_SELECTOR, ".figure-modal")
    if not modal.is_displayed():
        raise AssertionError("Site's native figure enlargement did not open")
    browser.execute_script(
        "arguments[0].click();",
        browser.find_element(By.CSS_SELECTOR, ".figure-modal-close")
    )
    if modal.is_displayed():
        raise AssertionError("Enlarged figure dialog did not close")
    output.mkdir(parents=True, exist_ok=True)
    central = browser.find_elements(By.CSS_SELECTOR, ".hl-min-figure")[0]
    browser.execute_script(
        "arguments[0].scrollIntoView({block:'center',behavior:'instant'});", central
    )
    time.sleep(.15)
    central.screenshot(str(output / f"paradox-on-page-{width}.png"))
    browser.save_screenshot(str(output / f"page-{width}.png"))
    print(json.dumps({"viewport":width,"figures":result["count"],
                      "documentWidth":result["pageWidth"],"interaction":"PASS"}))


def check_artwork(browser, output: Path) -> None:
    """Read each SVG directly in Chrome to inspect actual glyph geometry."""
    gallery = []
    for i, name in enumerate(FIGURES, 1):
        file = ASSETS / f"{name}.svg"
        browser.set_window_size(1050, 900)
        browser.get(file.as_uri())
        result = browser.execute_script("""
          const root = document.querySelector('svg');
          const b = root.viewBox.baseVal;
          const labels = [...root.querySelectorAll('text')];
          const errors = [];
          for (const t of labels) {
            const r = t.getBBox();
            if (r.width <= 0 || r.height <= 0)
              errors.push('invisible: '+t.textContent);
            if (r.x < -3 || r.y < -3 || r.x + r.width > b.width + 3 ||
                r.y + r.height > b.height + 3)
              errors.push('clipped: '+t.textContent);
          }
          // Report visible label collisions. Minor glyph-edge intersections
          // under 2 px are not treated as an overlap.
          for (let a = 0; a < labels.length; a++) {
            const p = labels[a].getBBox();
            for (let j = a+1; j < labels.length; j++) {
              const q = labels[j].getBBox();
              const w = Math.min(p.x+p.width,q.x+q.width)-Math.max(p.x,q.x);
              const h = Math.min(p.y+p.height,q.y+q.height)-Math.max(p.y,q.y);
              if (w > 4 && h > 5)
                errors.push('overlapping labels: '+labels[a].textContent+
                            ' / '+labels[j].textContent);
            }
          }
          return {errors, labels:labels.length, width:b.width, height:b.height};
        """)
        if result["errors"]:
            raise AssertionError(f"SVG {i:02d}: {result['errors']}")
        element = browser.find_element(By.TAG_NAME, "svg")
        shot = output / f"{name}.png"
        element.screenshot(str(shot))
        picture = Image.open(shot).convert("RGB")
        # A cream background with no actual content would have almost no
        # dark pixels. Earlier CI erroneously counted empty SVG containers.
        samples = [picture.getpixel((x,y))
                   for y in range(10,picture.height-10,12)
                   for x in range(10,picture.width-10,12)]
        ink = sum(min(pixel) < 170 for pixel in samples) / max(1,len(samples))
        if ink < .009:
            raise AssertionError(f"SVG {i:02d} appears visually blank: ink={ink:.2%}")
        thumb = ImageOps.contain(picture, (565, 400))
        gallery.append(thumb)
        print(json.dumps({"svg":i,"labels":result["labels"],
                          "inkRatio":round(ink,4),"geometry":"PASS"}))
    # The cover is a diagram too. Check it at its native size and keep a
    # rendered copy so the publication preview is reviewable.
    browser.set_window_size(1440, 900)
    browser.get((ASSETS / "cover.svg").as_uri())
    cover = browser.execute_script("""
      const s = document.querySelector('svg');
      const vb=s.viewBox.baseVal;
      const problems=[];
      for(const t of s.querySelectorAll('text')){
        const b=t.getBBox();
        if(b.width<=0 || b.x<-2 || b.y<-2 || b.x+b.width>vb.width+2 ||
           b.y+b.height>vb.height+2) problems.push('cover text out of bounds: '+t.textContent);
      }
      return {problems,labels:s.querySelectorAll('text').length};
    """)
    if cover["problems"]:
        raise AssertionError(str(cover["problems"]))
    browser.find_element(By.TAG_NAME,"svg").screenshot(str(output / "minimalist-cover.png"))

    sheet = Image.new("RGB",(1174,2*430),"#f0f0ec")
    draw = ImageDraw.Draw(sheet)
    for i,img in enumerate(gallery):
        x=14+(i%2)*585
        y=12+(i//2)*430
        sheet.paste(img,(x,y+24))
        draw.text((x+5,y+4),f"FIGURE {i+1:02d}",fill="#242b2b")
    sheet.save(output / "minimalist-figures-contact-sheet.png")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=Path("/tmp/halting-qa"))
    args=parser.parse_args()
    opts=Options()
    for arg in ("--headless=new","--no-sandbox","--disable-dev-shm-usage",
                "--disable-gpu","--force-device-scale-factor=1"):
        opts.add_argument(arg)
    driver=webdriver.Chrome(options=opts)
    try:
        check_article(driver,1365,900,args.output)
        check_article(driver,390,844,args.output)
        check_artwork(driver,args.output)
    finally:
        driver.quit()
    print("PASS: responsive article, interaction, and all explanatory SVG illustrations.")


if __name__=="__main__":
    main()
