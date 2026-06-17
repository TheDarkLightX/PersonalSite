#!/usr/bin/env python3
"""Render the REAL stdout of a command into a looping animated terminal SVG.

Usage: python3 tools/make_terminal_svg.py "<command>" <out.svg> "<title>"

The SVG types out the captured lines (clip-path reveal), then loops. It is a
faithful recording of an actual run -- nothing is hand-edited. Standard library
only; produces a self-contained, dependency-free SVG suitable for GitHub Pages.
"""
import html
import re
import subprocess
import sys

CHARW = 8.6      # px per monospace glyph at 15px
LINEH = 22       # px line height
FONT = 15
PAD = 18
BAR = 34         # title-bar height


def esc(s):
    return html.escape(s, quote=True)


def spans(line):
    """Colorize a line into <tspan>s (prompt, comment, accept/reject tags)."""
    if line.startswith("#"):
        return f'<tspan class="cm">{esc(line)}</tspan>'
    out = []
    if line.startswith("$ "):
        out.append('<tspan class="pr">$</tspan>')
        line = line[1:]
    for part in re.split(r"(\[ACCEPT\]|\[REJECT\]|\[HOLDS\]|\[FAILS\]|MATCHES|DIFFERS)", line):
        if part in ("[ACCEPT]", "MATCHES", "[HOLDS]"):
            out.append(f'<tspan class="ok">{esc(part)}</tspan>')
        elif part in ("[REJECT]", "DIFFERS", "[FAILS]"):
            out.append(f'<tspan class="no">{esc(part)}</tspan>')
        elif part:
            out.append(esc(part))
    return "".join(out)


def main():
    cmd, out_path, title = sys.argv[1], sys.argv[2], sys.argv[3]
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    lines = res.stdout.rstrip("\n").split("\n")

    maxlen = max((len(ln) for ln in lines), default=40)
    width = max(620, int(PAD * 2 + maxlen * CHARW))
    body_h = len(lines) * LINEH
    height = BAR + PAD + body_h + PAD

    reveal = max(3.2, len(lines) * 0.34)
    hold = 2.4
    total = round(reveal + hold, 2)
    k = round(reveal / total, 4)

    rows = []
    y = BAR + PAD + FONT
    for ln in lines:
        rows.append(f'<text x="{PAD}" y="{y:.0f}">{spans(ln)}</text>')
        y += LINEH
    cursor_y = BAR + PAD + (len(lines)) * LINEH - LINEH + 4

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="{esc(title)}: real terminal output">
  <title>{esc(title)} — real terminal output</title>
  <style>
    .term {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: {FONT}px; }}
    .term text {{ fill: #d7e2dd; white-space: pre; }}
    .term .pr {{ fill: #44c7b5; font-weight: 700; }}
    .term .cm {{ fill: #80978d; }}
    .term .ok {{ fill: #46d39a; font-weight: 700; }}
    .term .no {{ fill: #e0a64e; font-weight: 700; }}
  </style>
  <rect x="0" y="0" width="{width}" height="{height}" rx="12" fill="#0d1411" stroke="#22302b"/>
  <rect x="0" y="0" width="{width}" height="{BAR}" rx="12" fill="#15211d"/>
  <rect x="0" y="{BAR - 12}" width="{width}" height="12" fill="#15211d"/>
  <circle cx="20" cy="{BAR // 2}" r="5" fill="#ff5f56"/>
  <circle cx="38" cy="{BAR // 2}" r="5" fill="#ffbd2e"/>
  <circle cx="56" cy="{BAR // 2}" r="5" fill="#27c93f"/>
  <text x="{width // 2}" y="{BAR // 2 + 4}" text-anchor="middle" class="term" style="font-size:12px" fill="#7f9b91">{esc(title)}</text>
  <clipPath id="reveal">
    <rect x="0" y="{BAR}" width="{width}" height="0">
      <animate attributeName="height" values="0;{body_h + PAD * 2};{body_h + PAD * 2}" keyTimes="0;{k};1" dur="{total}s" repeatCount="indefinite"/>
    </rect>
  </clipPath>
  <g class="term" clip-path="url(#reveal)">
    {chr(10).join("    " + r for r in rows)}
    <rect x="{PAD}" y="{cursor_y:.0f}" width="9" height="16" fill="#44c7b5">
      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/>
    </rect>
  </g>
</svg>
'''
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {out_path}  ({width}x{height}, {len(lines)} lines)")


if __name__ == "__main__":
    main()
