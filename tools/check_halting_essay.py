#!/usr/bin/env python3
"""Validate the illustrated Gödel–Turing essay before publication.

Usage:
    python3 tools/check_halting_essay.py
    python3 tools/check_halting_essay.py --html path/to/essay.html

The previous publishing error left the SVGs empty while painting their intended
shapes into captions. This test checks actual SVG children rather than counting
figure tags alone.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
import xml.etree.ElementTree as ET
from html.parser import HTMLParser


DEFAULT = (
    Path(__file__).resolve().parents[1]
    / "essays"
    / "why-cant-a-turing-machine-predict-its-own-death.html"
)
NS = "{http://www.w3.org/2000/svg}"


class Structure(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.duplicate_ids = set()
        self.fragment_links = []
        self._figures = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            if a["id"] in self.ids:
                self.duplicate_ids.add(a["id"])
            self.ids.add(a["id"])
        if tag == "a" and a.get("href", "").startswith("#"):
            self.fragment_links.append(a["href"][1:])
        if tag == "figure" and "essay-plate" in a.get("class", "").split():
            self._figures += 1


def validate(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    parser = Structure()
    parser.feed(html)
    errors = []
    figures = re.findall(
        r'<figure class="essay-plate">([\s\S]*?)</figure>', html
    )
    if len(figures) != 12 or parser._figures != 12:
        errors.append(f"Expected 12 figures, got {len(figures)}.")

    for number, figure in enumerate(figures, 1):
        svg_match = re.search(r"<svg\b[\s\S]*?</svg>", figure)
        cap_match = re.search(r"<figcaption>([\s\S]*?)</figcaption>", figure)
        if not svg_match or not cap_match:
            errors.append(f"Figure {number}: missing SVG or caption.")
            continue
        if re.search(r"<(?:rect|path|text|line|polygon)\b", cap_match[1]):
            errors.append(f"Figure {number}: drawing markup leaked into caption.")
        if not re.search(r"[A-Za-z]{5,}", re.sub(r"<[^>]+>", "", cap_match[1])):
            errors.append(f"Figure {number}: caption does not explain anything.")
        try:
            svg = ET.fromstring(svg_match[0])
        except ET.ParseError as exc:
            errors.append(f"Figure {number}: malformed SVG XML: {exc}")
            continue
        if svg.tag != f"{NS}svg":
            errors.append(f"Figure {number}: wrong namespace.")
        if not svg.find(f"{NS}title") is not None or svg.find(f"{NS}desc") is None:
            errors.append(f"Figure {number}: missing accessible title/description.")
        txt = list(svg.iter(f"{NS}text"))
        shapes = sum(1 for e in svg.iter() if e.tag in {
            f"{NS}rect", f"{NS}path", f"{NS}line",
            f"{NS}polygon", f"{NS}circle"
        })
        if len(txt) < 4 or shapes < 3:
            errors.append(
                f"Figure {number}: only {len(txt)} text and {shapes} shapes."
            )
        if any(not (t.text or "").strip() for t in txt):
            errors.append(f"Figure {number}: empty text element.")
        print(f"Figure {number:>2}: {len(txt):>2} labels, {shapes:>2} shapes, valid SVG")

    if parser.duplicate_ids:
        errors.append(f"Duplicate HTML IDs: {sorted(parser.duplicate_ids)}.")
    missing = sorted(set(parser.fragment_links) - parser.ids)
    if missing:
        errors.append(f"Broken fragment links: {missing}.")
    if 'data-prediction="halts"' not in html or 'data-prediction="loops"' not in html:
        errors.append("Missing interactive halting scenario controls.")
    if "effective_computation_by_human_and_machine.pdf" not in html:
        errors.append("Missing requested Shagrir reference.")
    if errors:
        raise SystemExit("\n".join(errors))
    print("PASS: valid explanatory SVG content, captions, page anchors and experiment.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", type=Path, default=DEFAULT)
    validate(ap.parse_args().html)
