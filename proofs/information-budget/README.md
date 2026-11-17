# What a Smaller Map Forgets: evidence

The four-light task covers all sixteen starting patterns, with target `0001`.
Legal buttons XOR the current pattern with `0011`, `0101`, or `1111`.
The eight reachable net corrections are `0000`, `0011`, `0101`, `0110`,
`1001`, `1010`, `1100`, and `1111`.

## Exact scope

- The minimum number of labels for an exact yes/no answer is two.
- For returning a valid correction using a decoder that cannot reread the
  original starting pattern, the minimum is nine. Solvable inputs must yield
  at least one answer; every answer offered by the reduced task must decode
  to a valid correction. Impossible inputs must remain impossible.
- These bounds count labels, not computation time, source expression length,
  average code length, or storage with access to external information.
- With access to the original input, a decoder can reconstruct the correction
  after a YES decision. It uses `start XOR goal`; the original input remains
  part of the available information.

The existing private shift synthesizer enumerated 32 affine bit encoders,
each paired with two Boolean output interpretations. The actual ZAL checker
accepted two of the 64 candidates, both the parity partition with consistent
output labeling. It also checked the constructed nine-label representation,
the decoder with original-input access, and two deliberately broken decoders.
This is bounded synthesis, not a search over all possible encodings.

`replay.py` is an independent implementation with Python's standard library,
using tuples of Booleans and graph closure. It does not import the private
synthesizer or ZAL runtime. Run:

```sh
python3 replay.py
```

The output matches `results.json`. The replay checks all sixteen starts and
all 64 candidate pairs; it also checks 36 pairwise distinguishing corrections
among nine representative inputs. These checks independently reproduce the
finite mathematical results; they do not verify the private checker itself.

## Lean

`InformationBudget.lean` was compiled with Lean **4.24.0**, Mathlib commit
`f897ebcf72cd16f89ab4577d0c826cd14afaafc7`.
In a Mathlib project pinned to this commit, place the source in the project
root and run:

```sh
lake env lean InformationBudget.lean
```

`lean-build.txt` records the axiom output. There are no `sorry` placeholders,
`admit`, custom axioms, or uses of `native_decide` in this module. The
standard foundations printed for some theorems are `propext`,
`Classical.choice`, and `Quot.sound`.

The Lean development defines the correction relation using the listed eight
masks. It proves the general `m + 1` label bound, the nine-label necessity and
sufficiency results for this relation, and the exact two-label decision bound.
The executable replay connects these eight masks to the three legal buttons
by complete closure. The JavaScript interface is not covered by the Lean proof.

`Positive_Seeds_and_Certified_Synthesis.pdf` and `paper.md` contain the
underlying paper. The 2-versus-9 result is an extension for the essay. It
applies established ideas about preserving answers and distinguishing inputs;
no worldwide novelty is claimed.
