# Abstraction Is Compression: proof companion

This companion supports [the essay](https://www.danaedwards.info/essays/abstraction-is-compression.html). It checks elementary statements about compression, reachability, and quantifier order. **It does not prove that a useful physical AI containment configuration exists.**

The essay's physical existence claim is a research hypothesis. The seven theorems below make its logical structure and its missing obligations explicit.

## Statements and assumptions

| Lean theorem | What it establishes | What must already hold |
| --- | --- | --- |
| `compression_preserves_decision` | Equal summaries give the same answer to the chosen question. | A readout from the summary reproduces that answer for every concrete state. |
| `reachable_invariant` | Every reachable state lies inside an invariant region. | The initial state is inside; **every** modeled transition preserves the region. |
| `reachability_maps` | Every concrete execution prefix maps to an abstract execution prefix. | Every concrete step has a corresponding abstract step, including self-loops for hidden internal moves. |
| `abstract_safety_transfers` | Absence of abstract bad states implies absence of concrete bad states. | Transition coverage, bad-state coverage, and abstract unreachability all hold. |
| `witness_refutes_universal_escape` | One admissible design that defeats every modeled strategy refutes the claim that every admissible design can be escaped. | Such a witness is supplied. The theorem assumes it; it does not construct hardware. |
| `quantifier_order_matters` | Being able to choose a different response to each attack does not imply one response works against every attack. | A two-element Boolean example; no physical assumptions. |
| `omitted_edge_changes_answer` | A correct unreachability proof for an incomplete transition relation can give the wrong answer for a larger relation. | A two-state example showing an omitted transition. |

`Reach` represents finite execution prefixes. An invariant therefore covers arbitrarily long finite executions, not merely a tested horizon. It does not establish liveness, model a continuous plant, or handle limit-time events without an appropriate transition model.

For the containment theorem, put admitted design constraints and useful-service requirements in `admissible`. A common strategy type `P` can encode configuration-dependent validity by defining `escapes c p` as “`p` is physically valid for `c` and reaches a forbidden outcome.” Environmental disturbances and outside assistance must be included if they are in scope.

The quantifiers are:

```text
exists c, admissible(c) and forall p, not escapes(c,p)
```

This contradicts `forall c, admissible(c) -> exists p, escapes(c,p)` for the **same** definitions. It says nothing about a changed environment, an omitted channel, or a physical implementation whose behavior is not covered by the model.

## Replay

Use the official Lean 4.19.0 release, pinned in `lean-toolchain`. Only `Std` is imported; no Mathlib download is needed.

```sh
cd proofs/abstraction
lean -DwarningAsError=true Abstraction.lean
```

From the repository root, validate the receipt as well:

```sh
python3 tools/check-abstraction.py
python3 tools/render_mental_toolkits.py --check
python3 tools/render_abstraction.py
git diff --exit-code -- assets/essays/abstraction-map.svg assets/essays/containment-search.svg assets/essays/abstraction-visual-checks.json
```

All seven statements report **no axiom dependencies**. There are no admitted proofs or custom axioms. The [verification receipt](verification.json) records the source hash, version, command, and individual reports. CI installs the official release with a pinned archive checksum and replays the check. The trusted base still includes Lean's kernel and its execution environment.

The local authoring environment needed a narrow adapter for Lean's lookup of its own executable: `/proc/<own-pid>/exe` was redirected to `/proc/self/exe`. Official Lean binaries were unmodified. The adapter and its rationale are documented in the [finite-search companion](../finite-search/README.md). Normal Linux CI runs without it.

## The separately replayed covert-channel model

The essay also uses [CovertChannelLab at revision ae90bb8](https://github.com/TheDarkLightX/CovertChannelLab/tree/ae90bb88273e82620f2e643c19f23aeea0d9b31c). Its existing model and Lean source were independently executed for this essay:

```sh
python3 lab.py
python3 -m unittest -q test_lab
lean Proofs.lean
```

The [replay receipt](covert-replay.json) records the pinned input hashes, outputs, and a derived axiom audit of all 24 public theorems. The exhaustive catalogue has 1,760 configurations, 19 feasible, and a least-cost witness `(s,r)=(7,2)` of cost 57. An integer lower-bound proof covers settings beyond the catalogue.

This remains a modeled result. The real-valued thermal plant's refinement to the Lean integer envelope, physical calibration, complete observer/actuator coverage, and concrete trusted-gate implementation remain open. The quantized observation guarantee does not cover an independent raw-temperature sensor. The service score and cost curve are stipulated, not measured hardware performance. No hardware experiment was performed for this essay.

The [claim map](../../data/abstraction-reading-map.json) separates the hypothesis, conditional theorems, replayed model, and open physical obligations. The [abstraction cards](../../data/essay-abstractions.json) provide the shared human-readable handles. Neither JSON schema is claimed to be a Research Kernel MCP import contract.
