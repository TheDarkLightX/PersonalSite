#!/usr/bin/env python3
"""Check the halting essay's references, graphics and accessible structure."""
from html.parser import HTMLParser
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / 'essays/why-cant-a-turing-machine-predict-its-own-death.html'
ASSETS = ROOT / 'assets/essays/halting-paradox'
FIGURES = ('prediction.svg', 'waiting.svg', 'repeated-state.svg')
NS = '{http://www.w3.org/2000/svg}'


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.duplicates = set()
        self.anchors = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            if attrs['id'] in self.ids:
                self.duplicates.add(attrs['id'])
            self.ids.add(attrs['id'])
        if tag == 'a' and attrs.get('href', '').startswith('#'):
            self.anchors.append(attrs['href'][1:])


def check_svg(path):
    root = ET.parse(path).getroot()
    assert root.tag == NS + 'svg', f'{path}: wrong SVG namespace'
    assert root.find(NS + 'title') is not None, f'{path}: missing title'
    assert root.find(NS + 'desc') is not None, f'{path}: missing description'
    width, height = int(root.attrib['width']), int(root.attrib['height'])
    assert tuple(map(int, root.attrib['viewBox'].split())) == (0, 0, width, height)
    assert width >= 720 and height >= 200, f'{path}: unexpected dimensions'
    return root


def main():
    html = HTML.read_text(encoding='utf-8')
    page = Page()
    page.feed(html)
    assert not page.duplicates, f'Duplicate IDs: {page.duplicates}'
    assert not (set(page.anchors) - page.ids), f'Broken anchors: {set(page.anchors) - page.ids}'
    figures = re.findall(r'<figure class="search-figure hl-min-figure">([\s\S]*?)</figure>', html)
    assert len(figures) == len(FIGURES), f'Expected {len(FIGURES)} explanatory figures'
    for figure, name in zip(figures, FIGURES):
        img = re.search(r'<img\b[^>]*>', figure)
        caption = re.search(r'<figcaption>([\s\S]*?)</figcaption>', figure)
        assert img and name in img.group(), f'Missing figure {name}'
        assert re.search(r'alt="[^"]{40,}"', img.group()), f'Missing accessible text for {name}'
        assert caption and len(re.sub(r'<[^>]*>', '', caption.group(1)).strip()) >= 40
        check_svg(ASSETS / name)
        print(f'{name}: accessible image, valid SVG and caption')
    check_svg(ASSETS / 'cover.svg')
    assert 'effective_computation_by_human_and_machine.pdf' in html
    assert 'data-prediction="halts"' in html and 'data-prediction="loops"' in html
    assert 'aria-live="polite"' in html
    print('PASS: figures, navigation, Shagrir reference and interaction structure')


if __name__ == '__main__':
    main()
