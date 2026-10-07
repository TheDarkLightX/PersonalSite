"""Replay the essay's Lean proof, enforce its axiom policy, and verify its receipt."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PROOFS = ROOT / "proofs" / "finite-search"
receipt = json.loads((PROOFS / "verification.json").read_text())
source_hash = hashlib.sha256((PROOFS / "FiniteSearch.lean").read_bytes()).hexdigest()
if source_hash != receipt["source_sha256"]:
    raise SystemExit("Proof changed: regenerate and review the verification receipt.")
version = subprocess.run(["lean", "--version"], cwd=PROOFS, text=True, capture_output=True, check=True)
if "version 4.19.0," not in version.stdout:
    raise SystemExit(f"Wrong Lean version: {version.stdout.strip()}")
result = subprocess.run(["lean", "-DwarningAsError=true", "FiniteSearch.lean"],
                        cwd=PROOFS, text=True, capture_output=True)
if result.returncode:
    raise SystemExit(result.stdout + result.stderr)
observed = {}
for line in result.stdout.splitlines():
    match = re.fullmatch(r"'FiniteSearch\.(\w+)' depends on axioms: \[(.*)\]", line)
    if not match:
        raise SystemExit(f"Unexpected verifier output: {line}")
    name, axioms = match.groups()
    if name in observed:
        raise SystemExit(f"Duplicate theorem report: {name}")
    observed[name] = [a.strip() for a in axioms.split(",") if a.strip()]
if result.stderr or observed != receipt["axioms"]:
    raise SystemExit("Axiom report differs from the reviewed receipt.")
allowed = {"propext", "Classical.choice", "Quot.sound"}
if any(set(axioms) - allowed for axioms in observed.values()):
    raise SystemExit("Unapproved axiom dependency.")
print(f"PASS: {len(observed)} Lean theorems; source hash, pinned version, and axiom policy match.")
