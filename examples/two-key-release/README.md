# Two-key release desk

A small case for [Meaning Before Mechanism](https://www.danaedwards.info/essays/meaning-before-mechanism.html).
Try the [browser demonstration](https://www.danaedwards.info/examples/two-key-release/).

One recognized approver records the first approval. A different recognized
approver produces one release intent and closes the request. Repeated approval,
unknown IDs, and commands against a closed request are rejected. Any recognized
ID may cancel while pending: cancellation commits a closed state and no release.
Here, “key” means an approval by an ID, not a cryptographic signature.

## How it was produced

The actual ZenoFCIS **2.1 development factory**, revision
`a1ce03e2bcd917ecb9a61a29be429f5ca09a85b8` on `agent/v21-factory-20261004`,
generated this app. Its package version remains `1.1.0`; this is not a claim
that a tagged 2.1 or 2.2 release exists. The source inputs adapt that revision's
`examples/dual-approval`, with destination/name changes and a second state law:
a non-approved committed state cannot contain a second approval.

```sh
zeno-fcis new app --contract contract --source PINNED_ZENOFCIS_SOURCE
zeno-fcis generate contract app --check
zeno-fcis contract review app --out evidence/contract-review.json --format json
```

The factory emitted `app/src/v2_contract.rs`, the canonical schema/policy bytes,
the generic library and SQLite session, and four native tests. Generated Rust
source is unchanged. The only packaging change replaces machine-specific Cargo
source paths with `../.zenofcis-source/`; the source checkout is pinned and
checked before replay. Cargo produced the app's resolved lockfile from the
factory's copied workspace lock. Two additional test files, the Python/Lean
companions, diagrams, and browser adapter were added for the case study.

The human supplied the task, purpose and desired explanation. Contract rules,
examples and formalizations were prepared by an AI assistant. A separately
assigned adversarial AI reviewed the app. **No independent human acceptance of
the examples or ZAL model is claimed.** The raw factory packet's generic
`owner-example` and `owner_agrees_with` field names do not change that provenance.
ZAL's review gesture was not simulated. This app uses the 2.1 declarations;
the separate experimental ZAL authoring layer is discussed in the essay.

## Reproduce

On Linux x86_64, install Rust **1.97.1**, Lean **4.19.0**, Python 3.11+,
Git, and a C compiler. Run from this repository:

```sh
python3 examples/two-key-release/replay.py
```

The script fetches the pinned public framework into the ignored
`.zenofcis-source` directory when absent, builds its real CLI, generates a
fresh app, compares factory files (normalizing only Cargo source paths),
reproduces the review packet, runs all seven native tests, executes/audits a
real SQLite journey, compares finite policy answers, and checks the Lean
proofs and their decision projection. It refuses a different or modified
framework checkout. Internet access is needed for the initial tool/dependency
downloads. All files in `evidence/provenance.json` must match their hashes.

To run the native generated app after replay, choose a new database path:

```sh
examples/two-key-release/app/target/debug/two-key-release /tmp/release-example.sqlite
examples/two-key-release/app/target/debug/two-key-release --audit /tmp/release-example.sqlite
```

The generated CLI executes its built-in example journey. It uses a recording
`MemoryDestination`; it does not send a real payment. The interactive browser
is a separate presentation adapter for the **actual Authority-recorded table**,
not a Rust/Wasm deployment. Serve the repository root, for example with
`python3 -m http.server 8000`, then open `/examples/two-key-release/`.

## What the evidence establishes

| Layer | Evidence | Limit |
| --- | --- | --- |
| Framework core | Exact-source upstream [Verus Authority qualification](https://github.com/TheDarkLightX/ZenoFCIS/actions/runs/37592277998/job/112696381253) passed, including mutation controls | Inspected hosted CI; full Verus suite not rerun locally |
| Generation | Fresh factory replay and byte comparison of generated Rust/schema/policy | Generator and specification meaning remain separate trust obligations |
| Native policy | Every one of 384 typed combinations checked for class, reason, pre/post, patch, effects and full delivery metadata | A finite app domain, not every malformed byte string |
| Graph | 14 reachable states, all 112 outgoing command/context combinations; one-use release credit preserved | A logical request history, not hostile-host rollback or delivery count |
| Lean | Seven policy theorems, including arbitrary finite histories; executable class/next/release projection matches all 384 Authority rows | No proved compiler or end-to-end Rust/Lean refinement |
| Shell | Exact replay, changed replay, stale state, duplicate publication and wrong acknowledgement probes; real SQLite journey | Trusted host/storage and destination observations |
| Adversarial review | Separate review of native code, boundary attacks, UI and claims | Absence of a found policy bypass is not a security theorem |

The factory's 33 policy mutations yielded 25 concrete differences, seven
generation refusals, and one full-domain equivalent. Mutation detection is
not an exploit count. Forty-five typed combinations refuse law 503; these
attempt bad **successors** from invalid supplied states. Some other invalid
supplied pre-states can produce a valid decision. The persistent shell binds
publication to its actual history; the claim is not “every invalid pre-state
is refused by evaluation.”

The Lean proof's standard axiom dependencies are recorded explicitly: the
last two theorems depend on propositional extensionality (`propext`); the
others are axiom-free. There are no custom axioms, `sorry`, or admitted goals.
Lean's executable export is a test of the same `step` definition used by the
proofs, comparing class, successor state and release count. Rust/Python tests
add reason, patch and complete delivery checks.

## Boundaries the review demonstrated

- **Identity:** a caller can select another officer ID. Production needs
  authenticated identity outside the core; two enum values do not prove two people.
- **Delivery:** `MemoryDestination` deduplicates within one instance. A fresh
  instance can record the same pending intent again. No external exactly-once
  guarantee is made.
- **Host writes:** changing acknowledgement fields directly can make an audit
  report no pending delivery. Audit does not prove an external delivery occurred.
- **Rollback:** restoring an older valid database can repeat delivery with
  the same content-bound ID. A hash chain alone does not establish freshness.
- **Browser:** JavaScript and static assets are not a security authority.
  New simulation means a separate genesis, not reopening a protected request.

The core excludes ambient I/O and application callbacks; immutable bindings
prevent mutable-alias changes during publication use. Schema/law checks and
private publication construction provide other protections. These are distinct
mechanisms, not consequences of purity alone. The broader trusted base includes
the intended specification, Verus/vstd/Z3, Rust compiler/platform, Lean kernel,
and the relevant shell/deployment assumptions.

## Inspectable files

- `contract/`: the source declarations, rules and AI-authored example expectations.
- `app/`: factory-produced native application plus explicitly added tests.
- `evidence/contract-review.json`: unmodified factory output.
- `check_case.py`: independent executable policy model and graph check.
- `../../proofs/two-key-release/`: Lean model, export and checked receipt.
- `evidence/adversarial-review.json`: findings, fixes and remaining assumptions.
- `evidence/provenance.json`: source pin, provenance and artifact digests.

The browser table is derived from the factory packet; it is not substituted
for native verification. No claim of production authentication, payment custody,
secure remote service, or a universal absence of attack surfaces is made.
