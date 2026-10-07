"""Render the essay's illustrative capacity model, not benchmark measurements."""
from fractions import Fraction
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "essays" / "memory-capacity.svg"
C, overhead = 100, 5
d0, d1 = Fraction(3, 10), Fraction(1, 10)
base = C * (1 - d0)
with_memory = (C - overhead) * (1 - d1)
gain = with_memory - base
efficiency = [1, 2, 4]
totals = [float(q * with_memory) for q in efficiency]
without = [float(q * base) for q in efficiency]
extra = [float(q * gain) for q in efficiency]

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 17, "svg.fonttype": "none", "svg.hashsalt": "memory-capacity-v1"})
fig, ax = plt.subplots(figsize=(7.2, 5.3))
paper, ink, grey, teal = "#faf9f5", "#182326", "#52636a", "#08705b"
fig.set_facecolor(paper)
ax.set_facecolor(paper)
fig.subplots_adjust(left=.14, right=.94, top=.70, bottom=.19)
fig.text(.06, .91, "More capacity from the same memory", size=20, weight="bold", color=ink)
fig.text(.06, .84, "Illustration · fixed compute budget and overhead", size=14, color="#52636a")
fig.legend(handles=[Patch(color=grey, label="Without memory"), Patch(color=teal, label="Added by memory")],
           loc="upper left", bbox_to_anchor=(.045, .81), ncol=2, frameon=False, fontsize=14,
           handlelength=1.1, columnspacing=1.5)

ys = [2, 1, 0]
ax.barh(ys, without, height=.50, color=grey)
ax.barh(ys, extra, left=without, height=.50, color=teal, edgecolor=paper, linewidth=1.5)
for y, original, added, total in zip(ys, without, extra, totals):
    ax.text(original / 2, y, f"{original:g}", ha="center", va="center", color="white", fontsize=17)
    ax.text(original + added / 2, y + .34, f"+{added:g}", ha="center", va="bottom", color=teal, fontsize=16, weight="bold")
    ax.text(total + 6, y, f"{total:g}", ha="left", va="center", color=ink, fontsize=16)
ax.set_yticks(ys, [f"q = {q}" for q in efficiency], fontsize=16)
ax.set_xticks([0, 100, 200, 300], ["0", "100", "200", "300"], fontsize=14)
ax.set_xlim(0, 380)
ax.set_ylim(-.5, 2.75)
ax.tick_params(axis="both", length=0, pad=8, colors=ink)
ax.xaxis.grid(True, color="#d4d7d4", linewidth=.6)
ax.set_axisbelow(True)
for spine in ax.spines.values():
    spine.set_visible(False)
fig.text(.14, .10, "Reference-equivalent capacity", size=15, color=ink)
fig.text(.06, .035, "C = 100; h = 5; d₀ = 30%; d₁ = 10%. Gains remain 22.1%.", size=12, color="#52636a")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUTPUT, metadata={"Date": None, "Title": "Memory capacity at three assumed research efficiencies", "Description": "Illustrative values from the essay: q=1 gives 70 without memory and 85.5 with it; q=2 gives 140 and 171; q=4 gives 280 and 342. Not TasteVal measurements."})
plt.close(fig)
print(OUTPUT)
