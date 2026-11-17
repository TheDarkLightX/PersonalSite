# Additional deductions for “What One Operation Can Build”

This supplement accompanies the essay's exact-label argument and accuracy–description-size relation. They are deductions beyond the supplied paper's exposition, not claims of priority over the mathematical literature.

## Exact labels: checked theorem

`ExactScalarQuotient.lean` proves that if a map h assigns one label to each real number and a deterministic rule G satisfies

    h(exp(a) − log(b)) = G(h(a), h(b))

for every real a and positive b, then h is injective or constant. Consequently, a finite label set forces h to be constant.

The proof derives label propagation through every valid expression. It then uses the strict-domain subtraction and multiplication recipes from `Arithmetic.lean`, copied unchanged from the paper's public supplement. It does not assume that Mathlib's total logarithm makes an invalid calculator expression legal.

If h(a)=h(b) for distinct a,b, subtraction yields h(a−b)=h(0). Multiplying by 1/(a−b) yields h(1)=h(0). Multiplying by any x yields h(x)=h(0). This is the familiar algebraic argument behind the simplicity of a field, applied to the calculator through its arithmetic recipes.

The fixed parameters 1 and 1/(a−b) are legitimate because this representation is assumed on all real inputs. Their use does not assert that seed 2 can manufacture either. The theorem does not exclude an invariant only on a seed's reachable numbers, a relation on multiple answer columns, a decision-specific reduction, or sound approximations that retain several possible outcomes.

### Lean replay

Use Lean 4.24.0 and Mathlib commit `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`. In a Mathlib checkout with its dependencies and cache installed, copy `Arithmetic.lean` and `ExactScalarQuotient.lean` into the checkout root and run:

```sh
lake env lean -o .lake/build/lib/lean/Arithmetic.olean Arithmetic.lean
lake env lean ExactScalarQuotient.lean
```

`lean-build.txt` records the successful axiom report. Both the initial build and an independent replay succeeded. The main theorem uses only Lean's standard `propext`, `Classical.choice`, and `Quot.sound`; the four-equation Boolean obstruction uses only `propext`. No admitted proof or custom axiom was added.

## Finite synthesis and independent replay

A finite affine shift search proposed the four maps x ↦ (a x+b) mod 2, with a,b in {0,1}, on the integers modulo 4. Requiring different labels for 0 and 1 left exactly parity and parity with its labels reversed. The exact shift checker accepted the induced subtraction and multiplication representations on every input pair. These shifts preserve the labels of answers; they do not reconstruct the original residues.

The standalone `replay_colors.py` uses no synthesis or checking library. It checks all 16 maps from four residues to two labels, including non-affine maps, and all possible two-label operation tables. It confirms the same two representations.

It then enumerates all 2,048 configurations assigning two labels to 0,1,2,1/2 (with 0 and 1 distinct) and selecting arbitrary subtraction and multiplication tables. No configuration satisfies all four equations:

| Equation | Required result |
| --- | --- |
| 2 − 1 | 1 |
| 1 − 1 | 0 |
| 2 × (1/2) | 1 |
| 0 × (1/2) | 0 |

Removing each equation individually admits a model; the replay retains those four controls. This shows that every equation contributes to this particular obstruction, without claiming it is a globally smallest certificate.

```sh
python3 replay_colors.py --out replay.json
```

`independent-replay.json` is the saved result. The finite check motivates the all-real theorem; it does not prove it.

## Accuracy and size: written deduction

Let b₀=F(c,c), c>0; let bₙ₊₁=T(bₙ) be the paper's four-press iteration; let εₙ=bₙ−1. The paper proves εₙ>0, εₙ→0 and T′(1)=exp(−e). Differentiability gives εₙ₊₁/εₙ→exp(−e). Taking logarithms, the successive changes in log(1/εₙ) tend to e. Averaging these changes gives log(1/εₙ)/n→e.

For decimal accuracy dₙ=−log₁₀(εₙ), this yields:

- dₙ₊₁−dₙ→e/ln(10)≈1.180534798.
- Saved instructions pₙ=1+4n satisfy pₙ/dₙ→4ln(10)/e≈3.388294869.
- Copied instructions mₙ=2·5ⁿ−1 satisfy ln(mₙ)/dₙ→ln(5)ln(10)/e≈1.363312555.

Thus copied size has exponential growth rate approximately 3.909121057 raised to decimal accuracy. More precisely, mₙ=exp((ln(5)ln(10)/e)dₙ+o(dₙ)). This does not assert that mₙ/3.909121057^dₙ tends to 1, or that successive integer accuracy targets multiply size by that factor: rounds are discrete.

These conclusions hold for this construction. They are not optimality, runtime or bit-complexity bounds. This asymptotic deduction has a written proof here; it is not part of the new Lean file.

`generate_accuracy.py` uses mpmath at 120 decimal digits to produce `accuracy-size.csv`, showing every round from 0 to 20 for seed 2. Those numerical illustrations are not exact real-number certificates.

```sh
python3 generate_accuracy.py
```
