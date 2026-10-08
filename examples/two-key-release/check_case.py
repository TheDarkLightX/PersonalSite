#!/usr/bin/env python3
"""Compare the Authority's finite table with a separately written policy model.

This script does not interpret policy.json or copy its expression graph. It is
another AI-generated implementation, not independent human approval or a proof
of the Rust/Lean translation. Native tests additionally inspect patch/effects.
"""
if not __debug__:
    raise SystemExit('Verification requires assertions; remove -O/-OO and PYTHONOPTIMIZE.')

import argparse
from collections import Counter, deque
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PIN = 'a1ce03e2bcd917ecb9a61a29be429f5ca09a85b8'
GENESIS = (150, 160, 160)
COMMANDS = (140, 141)
OFFICERS = (160, 161, 162, 163)


def invariant(s):
    status, first, second = s
    return ((first != 160 and second != 160 and first != second)
            if status == 151 else second == 160)


def fields(s):
    return [{'field': f, 'value': {'type_id': t, 'variant': v}}
            for f, t, v in zip((110, 111, 112), (105, 106, 106), s)]


def model(s, command, officer):
    status, first, second = s
    if status != 150:
        return {'class': 'Reject', 'reason': 200, 'post': [], 'outbox': []}
    if officer == 160:
        return {'class': 'Reject', 'reason': 201, 'post': [], 'outbox': []}
    if command == 141:
        post, cls, reason = (152, first, second), 'CommittedFailure', 202
    elif officer == first:
        return {'class': 'Reject', 'reason': 203, 'post': [], 'outbox': []}
    elif first == 160:
        post, cls, reason = (150, officer, second), 'Accept', None
    else:
        post, cls, reason = (151, first, officer), 'Accept', None
    if not invariant(post):
        return {'class': 'refused', 'law': 503}
    delivery = [] if post[0] != 151 else [{
        'ordinal': 0, 'channel': 300, 'destination': 'release-desk',
        'idempotency': '0', 'payload': [
            {'field': 130, 'value': {'type_id': 106, 'variant': officer}},
            {'field': 131, 'value': {'type_id': 106, 'variant': first}}]}]
    return {'class': cls, 'reason': reason, 'post': fields(post), 'outbox': delivery}


def read_table(packet):
    tab = packet['decision_table']
    assert tab['count'] == 384 and not tab['rows_omitted']
    assert packet['inputs']['construction'] == 'full-domain'
    digest, result = bytes(32), {}
    for row in tab['rows']:
        digest = sha256(digest + (row + '\n').encode()).digest()
        left, right = row.split(' | ')
        key = tuple(map(int, left.split()))
        assert key not in result
        parts = right.split()
        if parts[0] == 'refused':
            refusal = tab['refusals'][int(parts[1])]
            assert refusal['class'] == 'law'
            value = {'class': 'refused', 'law': refusal['law']}
        else:
            cls, reason, post, outbox = parts
            value = {'class': cls, 'reason': None if reason == '-' else int(reason),
                     'post': tab['post_states'][int(post)]['fields'],
                     'outbox': tab['outboxes'][int(outbox)]['deliveries']}
        result[key] = value
    assert digest.hex() == tab['rows_digest']['sha256']
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true', help='Write deterministic derived artifacts')
    args = parser.parse_args()
    packet_bytes = (ROOT/'evidence/contract-review.json').read_bytes()
    packet = json.loads(packet_bytes)
    for key, path in [('project_sha256', 'project.zeno'), ('rules_sha256', 'v2/policy.json'),
                      ('examples_sha256', 'tests/decision-examples.txt')]:
        assert sha256((ROOT/'contract'/path).read_bytes()).hexdigest() == packet['sources'][key]
        assert (ROOT/'contract'/path).read_bytes() == (ROOT/'app'/path).read_bytes()
    actual = read_table(packet)
    domain = set(product((150, 151, 152), OFFICERS, OFFICERS, COMMANDS, OFFICERS))
    assert actual.keys() == domain
    for key, outcome in actual.items():
        assert outcome == model(key[:3], *key[3:]), (key, outcome)

    # Explore the actual exported transition graph from genuine genesis.
    todo, seen, edges, emitted = deque([GENESIS]), {GENESIS}, [], 0
    while todo:
        s = todo.popleft()
        assert invariant(s)
        for command, officer in product(COMMANDS, OFFICERS):
            row = actual[(*s, command, officer)]
            assert row['class'] != 'refused', (s, command, officer)
            nxt = s if row['class'] == 'Reject' else tuple(f['value']['variant'] for f in row['post'])
            assert invariant(nxt)
            emits = len(row['outbox'])
            # A one-use credit proves by induction that each finite history
            # from genesis emits <= 1 release. This check covers all 112 edges.
            assert emits + int(nxt[0] == 150) <= int(s[0] == 150)
            if row['class'] == 'Reject':
                assert nxt == s and not emits
            if emits:
                assert s[0] == 150 and nxt[0] == 151 and nxt[1] != nxt[2]
            emitted += emits
            edges.append({'state': list(s), 'command': command, 'officer': officer,
                          'class': row['class'], 'next': list(nxt), 'releases': emits})
            if nxt not in seen:
                seen.add(nxt)
                todo.append(nxt)
    assert len(seen) == 14 and len(edges) == 112 and emitted == 6
    # UI uses actual Authority answers, not the independently written oracle.
    view = {'schema': 'two-key-release/demo-table/1', 'framework_commit': PIN,
            'review_sha256': sha256(packet_bytes).hexdigest(),
            'genesis': list(GENESIS), 'rows': [
                {'input': list(k), **v} for k, v in sorted(actual.items())]}
    evidence = {'schema': 'two-key-release/finite-check/1', 'framework_commit': PIN,
                'review_sha256': sha256(packet_bytes).hexdigest(), 'typed_inputs': len(domain),
                'matching_decisions': len(actual),
                'outcomes': dict(sorted(Counter(v['class'] for v in actual.values()).items())),
                'reachable_states': [list(s) for s in sorted(seen)],
                'reachable_edges': len(edges), 'release_edges': emitted,
                'release_credit_check': 'all reachable edges: releases + credit(next) <= credit(pre)',
                'limits': ['AI-generated oracle; no human approval inferred',
                           'Finite policy agreement; not a verified compiler or UI',
                           'Identity, external delivery, host and proof-tool trust remain separate'],
                'edges': edges}
    outputs = {'decision-table.json': view, 'evidence/finite-check.json': evidence}
    for path, value in outputs.items():
        text = json.dumps(value, indent=2, sort_keys=True) + '\n'
        if args.write:
            (ROOT/path).write_text(text)
        else:
            assert (ROOT/path).read_text() == text, f'Stale {path}'
    print('384 exact policy comparisons; 14 reachable states; 112 edges; release credit preserved.')


if __name__ == '__main__':
    main()
