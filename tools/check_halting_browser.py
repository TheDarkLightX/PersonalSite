#!/usr/bin/env python3
"""Rendered browser regression checks for the illustrated computability essay.

Uses Selenium and headless Chrome. Run the site's static HTML directly so the
test never needs the deployed domain or credentials.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from PIL import Image, ImageOps, ImageDraw

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait


ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "essays" / "why-cant-a-turing-machine-predict-its-own-death.html"


def inspect(browser, width: int, height: int, output: Path):
    browser.set_window_size(width, height)
    browser.get(ARTICLE.as_uri())
    WebDriverWait(browser, 15).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, ".essay-plate svg")) == 12
    )
    result = browser.execute_script("""
      const problems = [];
      const diagrams = [...document.querySelectorAll('.essay-plate')];
      for (const [index, figure] of diagrams.entries()) {
        const svg = figure.querySelector('svg');
        const texts = [...svg.querySelectorAll('text')];
        const svgRect = svg.getBoundingClientRect();
        const vb = svg.viewBox.baseVal;
        const expectedHeight = svgRect.width * vb.height / vb.width;
        if (Math.abs(svgRect.height - expectedHeight) > 4) {
          problems.push('Figure '+(index+1)+' is vertically cropped: '+Math.round(svgRect.height)+' px vs expected '+Math.round(expectedHeight)+' px');
        }
        if (texts.length < 4) problems.push('Figure '+(index+1)+' is empty');
        for (const text of texts) {
          const box = text.getBBox();
          if (!(box.width > 0 && box.height > 0)) {
            problems.push('Figure '+(index+1)+' has invisible text: '+text.textContent);
          }
          if (box.y < -4 || box.y + box.height > vb.height - 2 ||
              box.x < -4 || box.x + box.width > vb.width + 4) {
            problems.push('Figure '+(index+1)+' clips text: '+text.textContent);
          }
        }
        const caption = figure.querySelector('figcaption');
        if (caption.querySelector('rect,path,text,svg')) {
          problems.push('Figure '+(index+1)+' has drawing markup in its caption');
        }
        const panel = figure.querySelector('.diagram-window');
        const rect = panel.getBoundingClientRect();
        if (rect.width > innerWidth + 2) {
          problems.push('Figure '+(index+1)+' exceeds the mobile viewport');
        }
        if (innerWidth < 701 && panel.scrollWidth <= panel.clientWidth) {
          problems.push('Figure '+(index+1)+' cannot pan on a narrow screen');
        }
      }
      const cover = document.querySelector('img.visual-intro');
      if (!cover.complete || !cover.naturalWidth) problems.push('Cover did not load');
      if (document.documentElement.scrollWidth > innerWidth + 4) {
        problems.push('Page has horizontal overflow');
      }
      return {problems, figureCount:diagrams.length, viewport:innerWidth,
              pageWidth:document.documentElement.scrollWidth};
    """)
    if result["problems"]:
        raise AssertionError(f"Viewport {width}: {result['problems']}")
    buttons = browser.find_elements(By.CSS_SELECTOR, "[data-prediction]")
    if len(buttons) != 2:
        raise AssertionError("Halting exercise buttons missing")
    for guess, expected in (("halts", "D loops forever"), ("loops", "D halts")):
        button = browser.find_element(By.CSS_SELECTOR, f'[data-prediction="{guess}"]')
        browser.execute_script(
            "arguments[0].scrollIntoView({block:'center',behavior:'instant'});", button
        )
        try:
            button.click()
        except ElementClickInterceptedException:
            # Some headless runners confuse document and viewport coordinates
            # after SVG-heavy layouts. The event handler must still work.
            browser.execute_script("arguments[0].click();", button)
        output_text = browser.find_element(By.ID, "fate-output").text
        assert expected in output_text, (guess, output_text)

    output.mkdir(parents=True, exist_ok=True)
    first = browser.find_element(By.CSS_SELECTOR, ".essay-plate")
    browser.execute_script(
        "arguments[0].scrollIntoView({block:'center',behavior:'instant'});", first
    )
    time.sleep(0.3)
    browser.save_screenshot(str(output / f"article-{width}.png"))
    image_file = output / f"first-diagram-{width}.png"
    first.screenshot(str(image_file))
    pixels = Image.open(image_file).convert("RGB")
    # The illustration has a large dark-blue background. A blank, white
    # screenshot must not count as proof that the SVG visibly rendered.
    sample = [pixels.getpixel((x, y)) for y in range(50, pixels.height-30, 16)
              for x in range(10, pixels.width-10, 16)]
    dark_fraction = sum(max(rgb) < 130 for rgb in sample) / max(1, len(sample))
    if dark_fraction < 0.18:
        raise AssertionError(
            f"Viewport {width}: SVG screenshot blank, dark pixel share {dark_fraction:.2%}"
        )
    if width > 700:
        captures = []
        for i, figure in enumerate(browser.find_elements(By.CSS_SELECTOR, ".essay-plate"), 1):
            browser.execute_script(
                "arguments[0].scrollIntoView({block:'center',behavior:'instant'});", figure
            )
            time.sleep(0.06)
            name = output / f"diagram-{i:02d}-{width}.png"
            figure.screenshot(str(name))
            img = Image.open(name).convert("RGB")
            if img.getpixel((min(20,img.width-1),min(100,img.height-1))) == (255,255,255):
                raise AssertionError(f"Diagram {i} was captured as a blank white image.")
            thumb = ImageOps.contain(img, (560, 370))
            captures.append(thumb)
        sheet = Image.new("RGB", (1170, 6 * 415), "#edf1f5")
        draw = ImageDraw.Draw(sheet)
        for i, thumb in enumerate(captures):
            x = 16 + (i % 2) * 580
            y = 12 + (i // 2) * 415
            sheet.paste(thumb, (x,y + 27))
            draw.text((x+2,y+3), f"FIGURE {i+1:02d}", fill="#172c3d")
        sheet.save(output / "diagram-contact-sheet.png")
    print(json.dumps({"viewport": width, "figures": result["figureCount"],
                      "pageWidth": result["pageWidth"], "controls": "PASS",
                      "diagramDarkPixelShare": round(dark_fraction, 3)}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("/tmp/halting-qa"))
    args = parser.parse_args()
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--force-device-scale-factor=1")
    browser = webdriver.Chrome(options=options)
    try:
        inspect(browser, 1365, 900, args.output)
        inspect(browser, 390, 844, args.output)
    finally:
        browser.quit()


if __name__ == "__main__":
    main()
