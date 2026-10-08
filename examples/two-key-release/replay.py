#!/usr/bin/env python3
"""Rebuild the pinned factory, reproduce generated source, and replay evidence."""
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT/'.zenofcis-source'
PIN = 'a1ce03e2bcd917ecb9a61a29be429f5ca09a85b8'


def run(args, cwd=ROOT):
    p = subprocess.run([str(a) for a in args], cwd=cwd, text=True, capture_output=True)
    if p.returncode:
        raise SystemExit(p.stdout + p.stderr)
    return p.stdout


def main():
    if not SOURCE.exists():
        SOURCE.mkdir()
        run(['git','init','--quiet',SOURCE])
        run(['git','remote','add','origin','https://github.com/TheDarkLightX/ZenoFCIS.git'], SOURCE)
        run(['git','fetch','--depth=1','origin',PIN], SOURCE)
        run(['git','checkout','--detach',PIN], SOURCE)
    assert run(['git','rev-parse','HEAD'], SOURCE).strip() == PIN, 'Wrong framework revision'
    assert not run(['git','status','--porcelain','--untracked-files=no'], SOURCE).strip(), 'Modified framework source'
    print('Building the pinned 2.1 development factory…', flush=True)
    run(['cargo','build','--release','--locked','-p','zeno-fcis-cli'], SOURCE)
    cli = SOURCE/'target/release/zeno-fcis'
    with tempfile.TemporaryDirectory(prefix='two-key-replay-') as tmp:
        tmp = Path(tmp)
        fresh = tmp/'app'
        run([cli,'new',fresh,'--contract',ROOT/'contract','--source',SOURCE])
        generated = []
        for path in sorted(fresh.rglob('*')):
            if not path.is_file(): continue
            relative = path.relative_to(fresh)
            if str(relative) == 'Cargo.lock':
                # Factory copies its workspace lock. Cargo resolves the app's
                # package graph once; the committed app lock is tested --locked.
                continue
            expected = path.read_bytes()
            if str(relative) == 'Cargo.toml':
                expected = expected.decode().replace(str(SOURCE.resolve())+'/', '../.zenofcis-source/').encode()
            assert expected == (ROOT/'app'/relative).read_bytes(), f'Factory output differs: {relative}'
            generated.append(str(relative))
        run([cli,'generate','contract',ROOT/'app','--check'])
        packet = tmp/'review.json'
        run([cli,'contract','review',ROOT/'app','--out',packet,'--format','json'])
        assert packet.read_bytes() == (ROOT/'evidence/contract-review.json').read_bytes(), 'Review drift'
        run(['cargo','test','--locked','--manifest-path',ROOT/'app/Cargo.toml'])
        binary = ROOT/'app/target/debug/two-key-release'
        journey = json.loads(run([binary,tmp/'release.sqlite']))
        head = json.loads(run([binary,'--audit',tmp/'release.sqlite']))
        assert journey['bundles'] == head['commits'] == 2
        assert head['pending'] == 0
        print(f'Reproduced {len(generated)} factory files; seven native tests; real SQLite journey.', flush=True)
    for script in ['check_case.py','check_lean.py']:
        print(run([sys.executable, ROOT/script]).strip(), flush=True)
    provenance = json.loads((ROOT/'evidence/provenance.json').read_text())
    for relative, expected in provenance['artifact_sha256'].items():
        assert sha256((ROOT/relative).read_bytes()).hexdigest() == expected, relative
    print('PASS: factory generation, source binding, review, native app, finite model, Lean and artifact hashes.')


if __name__ == '__main__':
    main()
