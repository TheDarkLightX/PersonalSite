"""Numerical illustration of the paper's attractor, not a proof or exact-value certificate."""
from pathlib import Path
import csv
import mpmath as mp

mp.mp.dps = 120
b = mp.exp(2) - mp.log(2)
with Path(__file__).with_name('accuracy-size.csv').open('w') as f:
    writer = csv.writer(f)
    writer.writerow(['round', 'value', 'gap_to_one', 'decimal_accuracy',
                     'saved_operations', 'copied_operation_occurrences', 'copied_total_nodes'])
    for n in range(21):
        gap = b - 1
        writer.writerow([n, mp.nstr(b, 45), mp.nstr(gap, 40), mp.nstr(-mp.log10(gap), 30),
                         1 + 4*n, 2*5**n - 1, 4*5**n - 1])
        log_b = mp.log(b)
        # Algebraically identical to the strict four-operation recipe; avoids
        # intermediate exp/log cancellation when computing a tiny final gap.
        b = b - log_b + b*b*log_b / (mp.exp(mp.exp(b)) - b*log_b)
