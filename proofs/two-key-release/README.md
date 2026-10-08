# Release desk policy proofs

`ReleaseDesk.lean` defines the finite policy used in the essay and proves seven
statements. All source is checked with Lean 4.19.0 and warnings treated as errors.

| Theorem | Obligation |
| --- | --- |
| `step_preserves` | Every step from a valid state leaves a valid state |
| `reject_changes_nothing` | Rejection preserves state and emits no release |
| `release_requires_two_keys` | A release has two recognized, different IDs and closes as approved |
| `release_spends_credit` | Emitted intents plus remaining credit never exceeds previous credit |
| `history_preserves` | State validity holds through every finite command/caller history |
| `history_spends_credit` | The credit bound holds through every finite history |
| `every_history_is_safe` | Every history from genesis stays valid and emits at most one release intent |

A pending request has one release credit; a closed request has zero. This
potential-function argument lifts a finite local check into a theorem about
arbitrary finite histories. The bound is on logical intents for one request,
not real delivery count or database rollback.

`Export.lean` evaluates the **same `step` definition** on all 384 typed tuples.
`../../examples/two-key-release/check_lean.py` compares class, successor state
and release count with the real Rust Authority's recorded answers. That
comparison is exhaustive executable evidence; it is not a machine-checked
Rust-to-Lean refinement or verified compiler. Native tests additionally compare
reason, before/after fields, patches, empty effects and full outbox metadata.

```sh
python3 examples/two-key-release/check_lean.py
```

Run the command from the repository root with pinned `lean` on PATH. The check
requires source hashes, compiler version, all seven axiom reports and all 384
projection rows to match `verification.json`. The last two theorems use Lean's
standard propositional extensionality axiom (`propext`); the others have no
axiom dependencies. No custom axioms or admitted goals are used.

Local execution used the official unmodified Lean release. This environment
requires the already documented `/proc/self/exe` path adapter from
`../finite-search/README.md`. Hosted CI uses the same official Lean release
without that adapter. Its archive SHA-256 is
`6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`.

The model does not prove authentication, delivery semantics, browser behavior,
SQLite correctness, the compiler/platform, or that the human intended this
policy. The shared Rust core has its own separately linked Verus evidence.
