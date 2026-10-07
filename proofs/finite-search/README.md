# Finite search with sound negative memory

Companion to [The Maze That Remembers](../../essays/the-maze-that-remembers.html),
October 7, 2026. These are elementary facts about scheduling and filtering, not
novel mathematics or a proof of an empirical AI scaling law.

## Replay

With [elan](https://github.com/leanprover/elan) installed:

```sh
cd proofs/finite-search
lean --version
lean FiniteSearch.lean
```

The local `lean-toolchain` pins **Lean 4.19.0**. Only `Std` is imported; no
Mathlib download, Lake dependency, custom axiom, or admitted proof is needed.
The final commands print every named theorem's axiom dependencies. The allowed
foundations for this artifact are `propext`, `Classical.choice`, and `Quot.sound`.

From the repository root, the independent browser-model checks are:

```sh
node tools/check-search-memory.cjs
node tools/check-maze-witness.cjs
```

## Exact model

For `k > 0`, `rounds n k` is zero when `n = 0`, otherwise `(n - 1) / k + 1`,
using natural-number division. Thus it is the integer ceiling of `n/k`.
Candidate position `i` is assigned to round `i / k`, worker `i % k` (zero-based).
Each worker completes one independent check per round. Final partial batches
may leave workers idle. Fixed costs, contention, communication, dependencies,
and unequal checking times are outside the model.

| Lean theorem | Statement |
| --- | --- |
| `rounds_le_iff_capacity` | For positive k, `rounds n k ≤ r ↔ n ≤ r*k`. |
| `more_workers` | For `0 < k₁ ≤ k₂`, `rounds n k₂ ≤ rounds n k₁`. |
| `less_work` | For `m ≤ n` and `0 < k`, `rounds m k ≤ rounds n k`. |
| `candidate_covered` | For `i < n` and `0 < k`, round and worker are in range and reconstruct i. |
| `assignment_injective` | Equal round and worker imply equal candidate positions. |
| `pruning_preserves_solutions` | Sound rejection preserves every member satisfying `good`. |
| `pruning_reduces_rounds` | Filtering cannot increase the remaining round count. This alone says nothing about soundness. |
| `memory_and_workers` | Sound pruning preserves all solutions and, combined with more workers, cannot increase rounds. |

`SoundRejections good rejected` is the explicit assumption
`∀ x, rejected x = true → ¬good x`. `remaining` is the list filtered by the
negation of the rejection flag. The proof does not manufacture a sound checker
or establish that any particular rejection receipt is trustworthy.

The list permits duplicate values. Assignment uniqueness is about **positions**;
to interpret it as duplicate-free candidate work, supply a duplicate-free
enumeration. The browser model's shuffled enumeration is tested for this
property. It is an illustrative implementation, not a formally proved refinement.

To conclude that search finds an actual solution, one must additionally show a
solution exists in the enumerated domain and the terminating checker recognizes
it correctly. To conclude absence, every candidate must be checked completely.
A timeout supplies neither conclusion. A refuted proof script is not a refuted
theorem; pruning a branch requires a scoped argument about that entire branch.

The essay's expectation and independent-trial formulas, throughput ceiling,
claims about external projects, empirical science, and recursive improvement
are **not** formalized by this file.

## Verification record

See [verification.json](verification.json) for the exact source hash, toolchain,
command, exit code, and reported axiom dependencies. AI assisted with the
formalization. The statements and checked artifacts are available for review.

The local execution environment exposes `/proc/self/exe` but not
`/proc/<getpid()>/exe`. An environment-only `readlink` compatibility adapter
redirected exactly that self-executable lookup to `/proc/self/exe`; the official
Lean executable and libraries were unmodified. The adapter did not intercept
proof checking, file contents, exit status, or the axiom report. Ordinary Linux
replay and GitHub CI do not need it. The adapter source is included below so the
local environment can be audited:

```c
#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
ssize_t readlink(const char *path, char *buffer, size_t size) {
    ssize_t (*real_readlink)(const char *, char *, size_t) = dlsym(RTLD_NEXT, "readlink");
    char own_exe[80];
    snprintf(own_exe, sizeof own_exe, "/proc/%ld/exe", (long)getpid());
    return real_readlink(strcmp(path, own_exe) == 0 ? "/proc/self/exe" : path, buffer, size);
}
```

Rejection controls in `tools/check-search-memory.cjs` exhibit both a bad pruning
decision losing a solution and perfectly correlated retries never reaching it.
They test the importance of the assumptions; they do not replace the general
Lean proofs. CI reruns the source and checks that its hash matches the receipt.
