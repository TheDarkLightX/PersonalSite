#!/usr/bin/env python3
"""Collect public portfolio metrics from clean local repo checkouts.

Usage:
  python3 tools/collect_portfolio_metrics.py \
    --repo MPRD=/tmp/dana-metrics/MPRD \
    --repo ZenoDEX=/tmp/dana-metrics/ZenoDEX \
    --repo Formal_Methods_Philosophy=/tmp/dana-metrics/Formal_Methods_Philosophy \
    --output data/portfolio-metrics.json

The default "curated" footprint excludes common vendor, generated, data,
internal, and lockfile bulk. The raw artifact footprint is still reported.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import subprocess
from pathlib import Path


SOURCE_EXT = {
    ".py", ".rs", ".js", ".ts", ".tsx", ".jsx", ".sh", ".bash", ".c",
    ".h", ".cpp", ".hpp", ".go", ".java", ".rb", ".lean", ".tla", ".tau",
}
PROOF_EXT = {".lean", ".tla", ".smt2", ".v", ".thy", ".agda"}
DOC_EXT = {".md", ".rst", ".txt", ".adoc"}
LANGUAGE_LABELS = {
    ".py": "Python",
    ".rs": "Rust",
    ".lean": "Lean",
    ".md": "Markdown",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".toml": "TOML",
    ".json": "JSON",
    ".sh": "Shell",
    ".js": "JavaScript",
    ".html": "HTML",
    ".css": "CSS",
    ".txt": "Text",
    ".tla": "TLA+",
    ".tau": "Tau",
    ".tsx": "TSX",
    ".ts": "TypeScript",
    ".jsx": "JSX",
}
EXCLUDE_PARTS = {
    ".git", ".venv", "venv", "env", "node_modules", "target", "dist",
    "build", "__pycache__", "generated", "data", "internal", ".mypy_cache",
    ".pytest_cache",
}
EXCLUDE_NAMES = {
    "Cargo.lock", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "poetry.lock",
}
EXCLUDE_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".sqlite", ".db",
    ".csv", ".tsv", ".pem",
}

COCOMO_A = 2.94
COCOMO_EXPONENT = 1.0997
BLS_SOFTWARE_DEVELOPER_MEDIAN_ANNUAL_USD = 133_080
BLS_SOFTWARE_DEVELOPER_P90_ANNUAL_USD = 211_450
GITHUB_SEARCH_COUNTS_2026_06_17 = {
    "language:Lean": 11_100,
    "language:TLA": 1_385,
    "language:Rust": 1_216_021,
    "language:Python": 30_357_305,
}
DEFI_COMPARABLES_2026_06_17 = {
    "uniswap_uni_market_cap_usd": 2_243_488_243,
    "aave_aave_market_cap_usd": 1_152_460_097,
    "curve_crv_market_cap_usd": 371_705_769,
}
PROTOCOL_BENCHMARKS_2026_06_17 = {
    "uniswap_v3": {
        "public_build_cost_disclosed": False,
        "core_repo_contributor_accounts": 15,
        "periphery_repo_contributor_accounts": 16,
        "distinct_contributor_accounts_across_core_and_periphery": 23,
        "estimated_non_bot_contributor_accounts": 22,
        "visible_public_repo_window_months": 12,
        "sensitivity_window_months": 18,
        "core_repo_created": "2020-04-29",
        "public_launch_target": "2021-05-05",
        "core_repo_stars": 5004,
        "core_repo_forks": 3029,
        "periphery_repo_stars": 1327,
        "periphery_repo_forks": 1247,
        "later_company_series_b_usd": 165_000_000,
        "later_company_valuation_usd": 1_660_000_000,
    },
    "liquity_v1": {
        "public_build_cost_disclosed": False,
        "dev_repo_contributor_accounts": 15,
        "estimated_non_bot_contributor_accounts": 14,
        "documented_build_window_months": 18,
        "seed_funding_usd": 2_400_000,
        "series_a_funding_usd": 6_000_000,
        "disclosed_funding_before_or_near_launch_usd": 8_400_000,
        "launch_date": "2021-04-05",
        "dev_repo_created": "2019-12-02",
        "dev_repo_stars": 354,
        "dev_repo_forks": 339,
    },
    "liquid_loans": {
        "public_build_cost_disclosed": False,
        "public_repo_found": False,
        "founded": 2021,
        "linkedin_company_size": "11-50 employees",
        "audit_window": "2023-06-20 to 2023-07-12",
        "audit_full_time_security_engineers": 1,
        "audit_duration_weeks": 3,
        "protocol_lineage": "Liquity fork adapted for PulseChain.",
        "public_usage_wallets_connected": 9325,
        "public_usage_usdl_minted_usd": 6_100_000,
    },
}


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True)


def git_files(root: Path) -> list[Path]:
    out = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"])
    return [root / item.decode() for item in out.split(b"\0") if item]


def read_text(path: Path) -> str | None:
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if b"\0" in raw[:4096]:
        return None
    return raw.decode("utf-8", errors="ignore")


def nonblank_lines(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip())


def is_curated(rel: Path) -> bool:
    if rel.name in EXCLUDE_NAMES:
        return False
    if set(rel.parts) & EXCLUDE_PARTS:
        return False
    if rel.suffix.lower() in EXCLUDE_EXT:
        return False
    return True


def is_test(rel: Path) -> bool:
    name = rel.name.lower()
    parts = [part.lower() for part in rel.parts]
    return (
        "test" in parts
        or "tests" in parts
        or name.startswith("test_")
        or name.endswith("_test.py")
        or ".test." in name
        or ".spec." in name
    )


def is_verification_artifact(rel: Path) -> bool:
    text = str(rel).lower()
    return rel.suffix.lower() in PROOF_EXT or any(
        key in text
        for key in (
            "proof", "verify", "verification", "invariant", "spec", "model",
            "theorem", "lean", "tla", "tau",
        )
    )


def is_tau_related(rel: Path) -> bool:
    return rel.suffix.lower() == ".tau" or "tau" in [part.lower() for part in rel.parts]


def empty_metrics() -> dict[str, int]:
    return {
        "tracked_files": 0,
        "artifact_nonblank_lines": 0,
        "curated_files": 0,
        "curated_nonblank_lines": 0,
        "source_nonblank_lines": 0,
        "proof_nonblank_lines": 0,
        "documentation_nonblank_lines": 0,
        "test_files": 0,
        "test_nonblank_lines": 0,
        "verification_files": 0,
        "ci_workflows": 0,
        "tau_related_files": 0,
        "tau_related_nonblank_lines": 0,
    }


def collect_repo(name: str, root: Path) -> dict:
    metrics = empty_metrics()
    languages: dict[str, int] = {}

    for path in git_files(root):
        rel = path.relative_to(root)
        text = read_text(path)
        if text is None:
            continue

        count = nonblank_lines(text)
        metrics["tracked_files"] += 1
        metrics["artifact_nonblank_lines"] += count

        if not is_curated(rel):
            continue

        suffix = rel.suffix.lower()
        label = LANGUAGE_LABELS.get(suffix, suffix[1:].upper() if suffix else "[no extension]")
        languages[label] = languages.get(label, 0) + count
        metrics["curated_files"] += 1
        metrics["curated_nonblank_lines"] += count

        if suffix in SOURCE_EXT:
            metrics["source_nonblank_lines"] += count
        if suffix in PROOF_EXT:
            metrics["proof_nonblank_lines"] += count
        if suffix in DOC_EXT:
            metrics["documentation_nonblank_lines"] += count
        if is_test(rel):
            metrics["test_files"] += 1
            metrics["test_nonblank_lines"] += count
        if is_verification_artifact(rel):
            metrics["verification_files"] += 1
        if is_tau_related(rel):
            metrics["tau_related_files"] += 1
            metrics["tau_related_nonblank_lines"] += count
        if str(rel).startswith(".github/workflows/") and suffix in {".yml", ".yaml"}:
            metrics["ci_workflows"] += 1

    return {
        "name": name,
        "url": git(root, "remote", "get-url", "origin").strip(),
        "commit": git(root, "rev-parse", "--short=12", "HEAD").strip(),
        "metrics": metrics,
        "top_languages_by_nonblank_lines": dict(
            sorted(languages.items(), key=lambda item: item[1], reverse=True)[:8]
        ),
    }


def add_dicts(items: list[dict[str, int]]) -> dict[str, int]:
    total = empty_metrics()
    for item in items:
        for key, value in item.items():
            total[key] += value
    return total


def economic_model(source_nonblank_lines: int) -> dict:
    ksloc = source_nonblank_lines / 1000
    person_months = COCOMO_A * (ksloc ** COCOMO_EXPONENT) if ksloc else 0
    median_cost = person_months * (BLS_SOFTWARE_DEVELOPER_MEDIAN_ANNUAL_USD / 12)
    p90_cost = person_months * (BLS_SOFTWARE_DEVELOPER_P90_ANNUAL_USD / 12)
    return {
        "ksloc": round(ksloc, 3),
        "cocomo_nominal_person_months": round(person_months, 1),
        "salary_only_reproduction_cost_usd_median": round(median_cost),
        "salary_only_reproduction_cost_usd_p90": round(p90_cost),
    }


def rarity_proxy() -> dict:
    lean = GITHUB_SEARCH_COUNTS_2026_06_17["language:Lean"]
    tla = GITHUB_SEARCH_COUNTS_2026_06_17["language:TLA"]
    rust = GITHUB_SEARCH_COUNTS_2026_06_17["language:Rust"]
    python = GITHUB_SEARCH_COUNTS_2026_06_17["language:Python"]
    return {
        "source": "GitHub repository search counts checked on 2026-06-17.",
        "counts": GITHUB_SEARCH_COUNTS_2026_06_17,
        "ratios": {
            "lean_as_percent_of_python": round(lean / python * 100, 4),
            "lean_python_repo_ratio": round(python / lean, 1),
            "tla_as_percent_of_python": round(tla / python * 100, 4),
            "tla_python_repo_ratio": round(python / tla, 1),
            "lean_as_percent_of_rust": round(lean / rust * 100, 4),
            "tla_as_percent_of_rust": round(tla / rust * 100, 4),
        },
    }


def tau_option_value_proxy() -> dict:
    combined = sum(DEFI_COMPARABLES_2026_06_17.values())
    return {
        "source": "CoinGecko market-cap snapshots checked on 2026-06-17.",
        "comparables": DEFI_COMPARABLES_2026_06_17,
        "combined_comparable_market_cap_usd": combined,
        "scenario_capture_values_usd": {
            "0.1_percent": round(combined * 0.001),
            "1_percent": round(combined * 0.01),
            "5_percent": round(combined * 0.05),
        },
        "interpretation": "Scenario value for Tau if proof-oriented DEX and governance primitives help capture a small share of comparable DeFi protocol value. This is not a valuation of the current repos.",
    }


def salary_only_team_cost(headcount: int, months: int) -> dict:
    median_monthly = BLS_SOFTWARE_DEVELOPER_MEDIAN_ANNUAL_USD / 12
    p90_monthly = BLS_SOFTWARE_DEVELOPER_P90_ANNUAL_USD / 12
    return {
        "headcount": headcount,
        "months": months,
        "person_months": headcount * months,
        "salary_only_cost_usd_median": round(headcount * months * median_monthly),
        "salary_only_cost_usd_p90": round(headcount * months * p90_monthly),
    }


def protocol_benchmark_proxy() -> dict:
    uniswap = PROTOCOL_BENCHMARKS_2026_06_17["uniswap_v3"]
    liquity = PROTOCOL_BENCHMARKS_2026_06_17["liquity_v1"]
    return {
        "source": "Public protocol source, funding, audit, and GitHub API snapshots checked on 2026-06-17.",
        "benchmarks": PROTOCOL_BENCHMARKS_2026_06_17,
        "salary_only_team_cost_models": {
            "uniswap_v3_22_non_bot_accounts_12_months": salary_only_team_cost(
                uniswap["estimated_non_bot_contributor_accounts"],
                uniswap["visible_public_repo_window_months"],
            ),
            "uniswap_v3_22_non_bot_accounts_18_months": salary_only_team_cost(
                uniswap["estimated_non_bot_contributor_accounts"],
                uniswap["sensitivity_window_months"],
            ),
            "liquity_v1_14_non_bot_accounts_18_months": salary_only_team_cost(
                liquity["estimated_non_bot_contributor_accounts"],
                liquity["documented_build_window_months"],
            ),
        },
        "interpretation": "These are benchmark and replacement-cost models, not verified historical build budgets. They exclude benefits, management, legal, audit vendor pricing, infrastructure, opportunity cost, token economics, and market value.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", action="append", required=True, help="NAME=/path/to/repo")
    parser.add_argument("--output", default="data/portfolio-metrics.json")
    args = parser.parse_args()

    repos = []
    for spec in args.repo:
        name, sep, path = spec.partition("=")
        if not sep:
            raise SystemExit(f"Invalid --repo value: {spec}")
        repos.append(collect_repo(name, Path(path).resolve()))

    aggregate = add_dicts([repo["metrics"] for repo in repos])
    data = {
        "generated_at": dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat(),
        "methodology": {
            "line_count": "Nonblank lines in git-tracked UTF-8 text files.",
            "curated_exclusions": sorted(EXCLUDE_PARTS | EXCLUDE_NAMES | EXCLUDE_EXT),
            "economic_model": "COCOMO II nominal effort on curated source/proof KSLOC, converted to salary-only replacement cost using BLS software developer wages.",
        },
        "repositories": repos,
        "aggregate": aggregate,
        "economic_model": economic_model(aggregate["source_nonblank_lines"]),
        "rarity_proxy": rarity_proxy(),
        "tau_option_value_proxy": tau_option_value_proxy(),
        "protocol_benchmark_proxy": protocol_benchmark_proxy(),
        "sources": {
            "bls_software_developers": "https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm",
            "cocomo_ii_manual": "https://www.rose-hulman.edu/class/cs/csse372/201310/Homework/CII_modelman2000.pdf",
            "stackoverflow_2025_survey": "https://survey.stackoverflow.co/2025",
            "github_search_lean": "https://github.com/search?q=language%3ALean&type=repositories",
            "github_search_tla": "https://github.com/search?q=language%3ATLA&type=repositories",
            "github_search_python": "https://github.com/search?q=language%3APython&type=repositories",
            "github_search_rust": "https://github.com/search?q=language%3ARust&type=repositories",
            "coingecko_uniswap": "https://www.coingecko.com/en/coins/uniswap",
            "coingecko_aave": "https://www.coingecko.com/en/coins/aave",
            "coingecko_curve": "https://www.coingecko.com/en/coins/curve-dao-token",
            "uniswap_v3_blog": "https://blog.uniswap.org/uniswap-v3",
            "uniswap_v3_core_github": "https://github.com/Uniswap/v3-core",
            "uniswap_v3_periphery_github": "https://github.com/Uniswap/v3-periphery",
            "uniswap_labs_series_b": "https://techcrunch.com/2022/10/13/uniswap-labs-raises-165-million-in-new-funding/",
            "liquity_launch_details": "https://www.liquity.org/blog/liquity-launch-details",
            "liquity_seed_funding": "https://www.liquity.org/blog/liquity-protocol-raises-2-4m-in-seed-funding-led-by-polychain-capital",
            "liquity_series_a_funding": "https://www.liquity.org/blog/liquity-raises-6m-in-series-a-funding",
            "liquity_dev_github": "https://github.com/liquity/dev",
            "liquid_loans_audit": "https://llprod-resource.s3.ap-southeast-2.amazonaws.com/Audit/Liquid_Loans_Protocol_Smart_Contract_Security_Assessment_Report_Halborn.pdf",
            "liquid_loans_site": "https://www.liquidloans.io/",
            "liquid_loans_linkedin": "https://www.linkedin.com/company/liquid-loans",
        },
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2) + "\n")
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
