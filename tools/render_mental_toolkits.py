#!/usr/bin/env python3
"""Render the standard abstraction-card format in the linked essays."""
import argparse
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START, END = '<!-- MENTAL_TOOLKIT_START -->', '<!-- MENTAL_TOOLKIT_END -->'


def render(cards):
    parts = [START, '<section class="mental-toolkit" id="mental-toolkit" aria-labelledby="toolkit-title">',
             '<p class="eyebrow">Carry these ideas forward</p>',
             '<h2 id="toolkit-title">Mental toolkit</h2>',
             '<p class="toolkit-intro">Four handles for the argument. Open a card to recover its definition, limits, and evidence.</p>',
             '<div class="toolkit-grid">']
    for c in cards:
        links = ' · '.join(f'<a href="{escape(link["href"], quote=True)}">{escape(link["label"])}</a>' for link in c['links'])
        parts.extend([
            f'<div class="toolkit-card" id="{escape(c["id"])}">',
            f'<h3>{escape(c["label"])}</h3>',
            f'<p class="toolkit-symbol" aria-label="{escape(c["symbol_reading"], quote=True)}">{escape(c["symbol"])}</p>',
            f'<p class="toolkit-phrase">{escape(c["phrase"])}</p>',
            '<details><summary>Definition, limits, evidence</summary>',
            f'<p><strong>Meaning.</strong> {escape(c["meaning"])}</p>',
            f'<p><strong>Boundary.</strong> {escape(c["boundary"])}</p>',
            f'<p class="toolkit-links">{links}</p>', '</details></div>'])
    parts.extend(['</div>', '<p class="toolkit-foot">The symbols are shorthand for the scoped definitions above. <a href="../data/essay-abstractions.json">Machine-readable cards</a>.</p>', '</section>', END])
    return '\n'.join(parts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    spec = json.loads((ROOT/'data/essay-abstractions.json').read_text())
    for essay in spec['essays']:
        path = ROOT/essay['path']
        text = path.read_text()
        if START not in text:
            text = text.replace('        </article>', f'        {START}\n        {END}\n        </article>')
        assert START in text and END in text, path
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        updated = before + render(essay['cards']) + after
        if args.check:
            assert updated == path.read_text(), f'Stale abstraction cards: {path}'
        else:
            path.write_text(updated)
    print(f'{"Checked" if args.check else "Rendered"} {len(spec["essays"])} mental toolkits.')


if __name__ == '__main__':
    main()
