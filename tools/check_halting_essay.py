#!/usr/bin/env python3
"""Static validation for the 12 minimalist, external SVG figures.

The page once shipped 12 empty SVG elements with all drawing markup in their
captions. This test checks the actual files and figure references, not counts of
containers. Live layout and text geometry are checked in Chrome separately.
"""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "essays/why-cant-a-turing-machine-predict-its-own-death.html"
ASSET = ROOT / "assets/essays/halting-paradox"
NS = "{http://www.w3.org/2000/svg}"


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.duplicates = set()
        self.anchors = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            if a["id"] in self.ids:
                self.duplicates.add(a["id"])
            self.ids.add(a["id"])
        if tag == "a" and a.get("href", "").startswith("#"):
            self.anchors.append(a["href"][1:])


def run() -> None:
    html = HTML.read_text(encoding="utf-8")
    page = Page()
    page.feed(html)
    errs = []

    figures = re.findall(
        r'<figure class="search-figure hl-min-figure">([\s\S]*?)</figure>',
        html,
    )
    if len(figures) != 12:
        errs.append(f"Expected 12 figures, found {len(figures)}")
    for i, figure in enumerate(figures, 1):
        expected = f"figure-{i:02d}.svg"
        m = re.search(r'<img\b[^>]*>', figure)
        caption = re.search(r"<figcaption>([\s\S]*?)</figcaption>", figure)
        if not m or not caption:
            errs.append(f"Figure {i} missing img or caption")
            continue
        tag = m.group(0)
        if expected not in tag:
            errs.append(f"Figure {i} references wrong file")
        if not re.search(r'alt="[^"]{40,}"', tag):
            errs.append(f"Figure {i} missing meaningful alt text")
        if len(re.sub(r"<[^>]*>", "", caption.group(1)).strip()) < 40:
            errs.append(f"Figure {i} has poor caption")
        if re.search(r"<(?:rect|path|svg|circle|line|text)\b", caption.group(1)):
            errs.append(f"Figure {i} has shape tags in its caption")
        filepath = ASSET / expected
        if not filepath.exists():
            errs.append(f"Figure {i} missing SVG file {filepath}")
            continue
        try:
            root = ET.parse(filepath).getroot()
        except ET.ParseError as exc:
            errs.append(f"Figure {i} has invalid XML: {exc}")
            continue
        if root.tag != NS + "svg":
            errs.append(f"Figure {i} wrong SVG namespace")
        if root.find(NS + "title") is None or root.find(NS + "desc") is None:
            errs.append(f"Figure {i} missing accessible title and description")
        labels = list(root.iter(NS + "text"))
        shapes = sum(node.tag in {
            NS + "rect", NS + "path", NS + "circle", NS + "line"
        } for node in root.iter())
        if len(labels) < 5 or shapes < 3:
            errs.append(f"Figure {i} empty or decorative: {len(labels)} labels, {shapes} shapes")
        try:
            width = int(root.attrib["width"])
            height = int(root.attrib["height"])
            vb = tuple(map(int, root.attrib["viewBox"].split()))
            if width != 720 or height < 300 or vb != (0, 0, width, height):
                errs.append(f"Figure {i} incorrect dimensions: {width}x{height}, {vb}")
        except (ValueError, KeyError) as exc:
            errs.append(f"Figure {i} missing explicit consistent viewBox: {exc}")
        print(f"Figure {i:02d}: {len(labels)} labels, {shapes} shapes, {width}x{height}")

    if page.duplicates:
        errs.append(f"Duplicate HTML IDs: {page.duplicates}")
    missing = set(page.anchors) - page.ids
    if missing:
        errs.append(f"Broken internal section links: {missing}")
    if "effective_computation_by_human_and_machine.pdf" not in html:
        errs.append("Shagrir source is missing")
    if 'data-prediction="halts"' not in html or 'data-prediction="loops"' not in html:
        errs.append("Interactive prediction controls missing")

    cover = ASSET / "cover.svg"
    try:
        root = ET.parse(cover).getroot()
        if len(list(root.iter(NS + "text"))) < 8:
            errs.append("Cover is not an explanatory illustration")
    except (ET.ParseError, FileNotFoundError) as exc:
        errs.append(f"Cover SVG cannot be read: {exc}")

    if errs:
        raise SystemExit("\n".join(errs))
    print("PASS: external figures, XML geometry, captions and links checked.")


if __name__ == "__main__":
    run()
