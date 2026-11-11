#!/usr/bin/env python3
"""Rendered browser regression checks for the illustrated computability essay.

Uses Selenium and headless Chrome. Run the site's static HTML directly so the
test never needs the deployed domain or credentials.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

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
        if (texts.length < 4) problems.push('Figure '+(index+1)+' is empty');
        for (const text of texts) {
          const box = text.getBBox();
          if (!(box.width > 0 && box.height > 0)) {
            problems.push('Figure '+(index+1)+' has invisible text: '+text.textContent);
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
    browser.save_screenshot(str(output / f"article-{width}.png"))
    browser.find_element(By.CSS_SELECTOR, ".essay-plate").screenshot(
        str(output / f"first-diagram-{width}.png")
    )
    print(json.dumps({"viewport": width, "figures": result["figureCount"],
                      "pageWidth": result["pageWidth"], "controls": "PASS"}))


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
