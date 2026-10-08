#!/usr/bin/env python3
"""Replay the kernel proofs and compare the Lean projection with Authority."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

from check_case import read_table

HERE = Path(__file__).resolve().parent
PROOFS = HERE.parents[1]/'proofs/two-key-release'


def run(args, **kwargs):
    p = subprocess.run(args, text=True, capture_output=True, **kwargs)
    if p.returncode or p.stderr:
        raise SystemExit(p.stdout + p.stderr)
    return p.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--record', action='store_true')
    args = parser.parse_args()
    version = run(['lean', '--version']).strip()
    assert version == 'Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)'
    source = (PROOFS/'ReleaseDesk.lean').read_bytes()
    assert not re.search(r'\b(sorry|admit|axiom)\b', source.decode())
    with tempfile.TemporaryDirectory(prefix='release-lean-') as tmp:
        report = run(['lean', '-DwarningAsError=true', '-o', str(Path(tmp)/'ReleaseDesk.olean'),
                      'ReleaseDesk.lean'], cwd=PROOFS)
        axioms = {}
        for line in report.splitlines():
            match = re.fullmatch(r"'ReleaseDesk\.(\w+)' (does not depend on any axioms|depends on axioms: \[([^]]*)\])", line)
            assert match, line
            values = match[3].split(', ') if match[3] else []
            assert set(values) <= {'propext'}, values
            assert match[1] not in axioms
            axioms[match[1]] = values
        assert set(axioms) == set(re.findall(r'^theorem (\w+)', source.decode(), re.M))
        env = dict(os.environ, LEAN_PATH=tmp + os.pathsep + os.environ.get('LEAN_PATH', ''))
        projection = run(['lean', '-DwarningAsError=true', 'Export.lean'], cwd=PROOFS, env=env)
    actual = read_table(json.loads((HERE/'evidence/contract-review.json').read_text()))
    observed = set()
    for line in projection.splitlines():
        left, right = line.split(' | ')
        key = tuple(map(int, left.split()))
        assert key in actual and key not in observed, key
        observed.add(key)
        cls, *numbers = right.split()
        nxt, releases = tuple(map(int, numbers[:3])), int(numbers[3])
        d = actual[key]
        expected_next = key[:3] if d['class'] in ('Reject', 'refused') else tuple(f['value']['variant'] for f in d['post'])
        assert (cls, nxt, releases) == (d['class'], expected_next, len(d.get('outbox', []))), key
    assert len(observed) == len(actual) == 384
    receipt = {'schema':'release-desk/lean-verification/1', 'toolchain':version,
               'source_sha256':sha256(source).hexdigest(),
               'export_sha256':sha256((PROOFS/'Export.lean').read_bytes()).hexdigest(),
               'authority_review_sha256':sha256((HERE/'evidence/contract-review.json').read_bytes()).hexdigest(),
               'axioms':axioms, 'proof_stdout':report, 'matching_projected_decisions':len(observed),
               'projection_sha256':sha256(projection.encode()).hexdigest(),
               'projection_fields':['class','next_state','release_count'],
               'scope':'Seven policy-model theorems plus executable finite projection agreement; not a proved Rust/Lean compiler or full-system security proof.'}
    path = PROOFS/'verification.json'
    if args.record:
        receipt['checked_at_utc'] = datetime.now(timezone.utc).isoformat()
        path.write_text(json.dumps(receipt,indent=2)+'\n')
    else:
        expected = json.loads(path.read_text())
        expected.pop('checked_at_utc')
        assert expected == receipt, 'Lean evidence changed; inspect before recording a new receipt.'
    print('PASS: seven Lean theorems; 384 Authority/Lean projected decisions agree; no custom axioms or gaps.')


if __name__ == '__main__':
    main()
