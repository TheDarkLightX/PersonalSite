"""Replay the abstraction companion and require every theorem to be axiom-free."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PROOFS = ROOT / "proofs" / "abstraction"
receipt = json.loads((PROOFS / "verification.json").read_text())
source = (PROOFS / "Abstraction.lean").read_bytes()
if hashlib.sha256(source).hexdigest() != receipt["source_sha256"]:
    raise SystemExit("Proof changed: regenerate and review its receipt.")
version = subprocess.run(["lean", "--version"], cwd=PROOFS,
                         text=True, capture_output=True, check=True)
if version.stdout.strip() != receipt["toolchain"]:
    raise SystemExit(f"Unexpected Lean version: {version.stdout.strip()}")
result = subprocess.run(["lean", "-DwarningAsError=true", "Abstraction.lean"],
                        cwd=PROOFS, text=True, capture_output=True)
if result.returncode or result.stderr:
    raise SystemExit(result.stdout + result.stderr)
observed = {}
for line in result.stdout.splitlines():
    match = re.fullmatch(r"'Abstraction\.(\w+)' does not depend on any axioms", line)
    if not match:
        raise SystemExit(f"Unexpected axiom report: {line}")
    name = match.group(1)
    if name in observed:
        raise SystemExit(f"Duplicate theorem report: {name}")
    observed[name] = []
declared = set(re.findall(r"^theorem (\w+)", source.decode(), re.M))
if set(observed) != declared or observed != receipt["axioms"]:
    raise SystemExit("The receipt must cover every declared theorem exactly.")
print(f"PASS: all {len(observed)} theorems checked; no axiom dependencies; source and toolchain match.")
