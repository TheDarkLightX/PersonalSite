#!/usr/bin/env python3
"""Replay the dated cost sensitivity from pinned Git objects, never worktree bytes.

Uses the June collector's source extensions and publication exclusions to keep
the footprint comparison consistent. Nonblank lines include comments and are
not physical SLOC. No measured human-effort or market-value claim follows.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path

from collect_portfolio_metrics import SOURCE_EXT, is_publish_headline_file, nonblank_lines


def git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args])


def collect(root: Path, repo: dict) -> tuple[dict, list[dict]]:
    commit = repo["commit"]
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("A full pinned commit SHA is required")
    tree = git(root, "rev-parse", f"{commit}^{{tree}}").decode().strip()
    if tree != repo["tree"]:
        raise ValueError(f"Tree mismatch for {repo['name']}")
    rows = git(root, "ls-tree", "-rz", commit).split(b"\0")
    manifest = []
    cache = {}
    duplicate_lines = 0
    with subprocess.Popen(["git", "-C", str(root), "cat-file", "--batch"],
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE) as batch:
        try:
            for row in rows:
                if not row:
                    continue
                spec, path = row.split(b"\t", 1)
                mode, kind, blob = spec.split()
                rel = Path(path.decode("utf-8"))
                if mode not in {b"100644", b"100755"} or kind != b"blob":
                    continue
                if rel.suffix.lower() not in SOURCE_EXT or not is_publish_headline_file(repo["name"], rel):
                    continue
                if blob in cache:
                    count = cache[blob]
                    duplicate_lines += count
                else:
                    batch.stdin.write(blob + b"\n")
                    batch.stdin.flush()
                    header = batch.stdout.readline().split()
                    if len(header) != 3 or header[0] != blob or header[1] != b"blob":
                        raise ValueError(f"Missing or invalid blob: {blob!r}")
                    raw = batch.stdout.read(int(header[2]))
                    if len(raw) != int(header[2]) or batch.stdout.read(1) != b"\n":
                        raise ValueError("Truncated Git object")
                    if b"\0" in raw:
                        raise ValueError(f"Binary source file: {rel}")
                    count = nonblank_lines(raw.decode("utf-8"))
                    cache[blob] = count
                manifest.append({"repository": repo["name"], "path": str(rel),
                                 "blob": blob.decode(), "nonblank_lines": count})
        finally:
            batch.stdin.close()
        if batch.wait() != 0:
            raise ValueError("Git object reader failed")
    result = dict(repo, selected_files=len(manifest),
                  selected_nonblank_lines=sum(row["nonblank_lines"] for row in manifest),
                  exact_duplicate_nonblank_lines_within_repo=duplicate_lines)
    return result, manifest


def model(lines: int, scenarios: dict, fraction: float = 1.0) -> dict:
    if lines < 0 or not math.isfinite(fraction) or not 0 <= fraction <= 1:
        raise ValueError("Invalid source size or fraction")
    result = {}
    for label, scenario in scenarios.items():
        for key in ["coefficient", "exponent", "annual_wage_usd", "labor_multiplier"]:
            if not math.isfinite(scenario[key]) or scenario[key] <= 0:
                raise ValueError(f"Invalid scenario {key}")
        pm = scenario["coefficient"] * (lines * fraction / 1000) ** scenario["exponent"]
        result[label] = {"person_months": round(pm, 4),
                         "cost_usd": round(pm / 12 * scenario["annual_wage_usd"] * scenario["labor_multiplier"])}
    return result


def build(inputs: dict, paths: dict[str, Path], baseline: dict) -> tuple[dict, list[dict]]:
    names = [repo["name"] for repo in inputs["repositories"]]
    if len(names) != len(set(names)) or set(paths) != set(names):
        raise ValueError("Provide exactly one checkout for each configured repository")
    repos, manifest = [], []
    for repo in inputs["repositories"]:
        result, files = collect(paths[repo["name"]], repo)
        result["scenarios"] = model(result["selected_nonblank_lines"], inputs["scenarios"])
        repos.append(result)
        manifest.extend(files)
    total = sum(repo["selected_nonblank_lines"] for repo in repos)
    baseline_lines = baseline["publish_aggregate"]["authored_source_nonblank_lines"]
    old_model = baseline["publish_economic_model"]
    manifest_bytes = (json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n").encode()
    output = {
        "schema_version": 1, "as_of": inputs["as_of"], "inputs": inputs,
        "measure": "Nonblank lines in selected source/proof files; includes comments, tests and examples. Not physical SLOC or verified authorship.",
        "method": "June 2026 source extensions and publication exclusions, replayed on pinned Git objects. Primary scenario pools the three repositories to preserve the prior formula. Duplicate files are reported, not removed from this comparison.",
        "repositories": repos, "selected_nonblank_lines": total,
        "selected_files": sum(repo["selected_files"] for repo in repos),
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "pooled_scenarios": model(total, inputs["scenarios"]),
        "sum_of_repository_scenarios_usd": {
            label: sum(repo["scenarios"][label]["cost_usd"] for repo in repos)
            for label in inputs["scenarios"]
        },
        "size_sensitivity": [{"input_fraction": fraction, "scenarios": model(total, inputs["scenarios"], fraction)}
                             for fraction in [0.25, 0.5, 1.0]],
        "baseline": {"as_of": baseline["generated_at"], "selected_nonblank_lines": baseline_lines,
                     "low_cost_usd": old_model["loaded_build_cost_equivalent_low_usd"],
                     "high_cost_usd": old_model["loaded_build_cost_equivalent_high_usd"],
                     "line_change": total - baseline_lines,
                     "line_change_percent": round((total / baseline_lines - 1) * 100, 2)},
        "limits": [
            "Scenario outputs, not confidence bounds, a rebuild quote, a measured cost, savings, or market value.",
            "Legacy COCOMO equations are extrapolated using a nonblank-line proxy. They are not calibrated for these repositories, AI-assisted development, formal proofs, or mixed research artifacts.",
            "Known vendor/generated/data/internal paths are excluded; the path filters do not prove all third-party or generated content is absent.",
            "No semantic deduplication or contribution/authorship audit was performed. Tests and proofs are included once in the selected file footprint, not added as extra labor.",
            "Pooling independent repositories increases the nonlinear model output; the sum of separate repository scenarios is also reported.",
            "The 25% and 50% size cases are arbitrary input sensitivities, not measured AI productivity discounts.",
            "Wages use May 2025 BLS data without an inflation forecast. Labor multipliers are retained assumptions; external audits, legal fees, deployment and ongoing operations are not separately priced."
        ]
    }
    return output, manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=Path("data/cost-model-inputs.json"))
    parser.add_argument("--repo", action="append", required=True, help="NAME=/path/to/git/repository")
    parser.add_argument("--output", type=Path, default=Path("data/cost-estimates.json"))
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--check", action="store_true", help="Compare with the saved output without writing")
    args = parser.parse_args()
    pairs = [spec.split("=", 1) for spec in args.repo]
    if any(len(pair) != 2 for pair in pairs) or len({pair[0] for pair in pairs}) != len(pairs):
        parser.error("--repo must be a unique NAME=/path pair")
    inputs = json.loads(args.inputs.read_text())
    baseline = json.loads(Path(inputs["baseline"]).read_text())
    output, manifest = build(inputs, {name: Path(path) for name, path in pairs}, baseline)
    rendered = json.dumps(output, indent=2) + "\n"
    if args.check:
        if args.output.read_text() != rendered:
            raise SystemExit("Cost estimate replay differs from saved output")
        print("Cost estimate replay matches saved output")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
        print(f"Wrote {args.output}")
    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
