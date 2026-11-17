#!/usr/bin/env python3
"""Independent tuple-based replay of the four-light information example.

Python 3, standard library only. No ZAL or search implementation is imported.
The finite check complements InformationBudget.lean; it is not a Lean proof.
"""
from itertools import product, combinations
import json


def flip(state, move):
    return tuple(a != b for a, b in zip(state, move))


def closure(start, moves):
    seen = {start: ()}
    todo = [start]
    for state in todo:
        for i, move in enumerate(moves):
            nxt = flip(state, move)
            if nxt not in seen:
                seen[nxt] = seen[state] + (i,)
                todo.append(nxt)
    return seen


def replay():
    states = list(product((False, True), repeat=4))
    moves = ((False, False, True, True), (False, True, False, True),
             (True, True, True, True))
    goal = (False, False, False, True)
    zeros = (False,) * 4
    corrections = closure(zeros, moves)
    assert len(corrections) == 8
    answers = {s: {h for h in corrections if flip(s, h) == goal} for s in states}
    for s in states:
        assert bool(answers[s]) == (goal in closure(s, moves))
        assert bool(answers[s]) == (sum(s) % 2 == 1)

    # All 16 choices of included lights, 2 offsets, 2 output labelings.
    tested, accepted = 0, []
    for coefficients in product((0, 1), repeat=4):
        for offset, reverse in product((0, 1), repeat=2):
            tested += 1
            values = [((sum(a * b for a, b in zip(coefficients, s)) + offset) % 2) ^ reverse
                      for s in states]
            if values == [bool(answers[s]) for s in states]:
                accepted.append(dict(coefficients=coefficients, offset=offset, reverse=reverse))
    assert tested == 64 and len(accepted) == 2
    assert all(a['coefficients'] == (1, 1, 1, 1) for a in accepted)

    # Nine representatives have pairwise incompatible answer sets.
    # Two solvable cases cannot share a label, nor can a solvable and empty case.
    solvable = [s for s in states if answers[s]]
    representatives = [zeros] + solvable
    for a, b in combinations(representatives, 2):
        assert answers[a] != answers[b]
        assert not (answers[a] & answers[b])
        # A common move sequence can reach the goal from at most one.
        witness = next(iter(answers[a] or answers[b]))
        assert (flip(a, witness) == goal) != (flip(b, witness) == goal)
    assert len(representatives) == 9
    # Keeping the original input restores a correction on every solvable case.
    for s in solvable:
        h = flip(s, goal)
        assert h in corrections and flip(s, h) == goal

    # A broken decoder that always returns 'do nothing' has a concrete failure.
    bad_start = (False, False, True, False)
    assert answers[goal] == {zeros}
    assert bool(answers[bad_start]) and flip(bad_start, zeros) != goal
    return {
        'inputs': len(states), 'allowed_net_corrections': len(corrections),
        'candidate_pairs': tested, 'accepted': accepted,
        'decision_labels': 2, 'correction_labels_without_original_input': 9,
        'incompatible_pairs': 36,
        'rows': [dict(pattern=''.join(str(int(b)) for b in s),
                      reachable=bool(answers[s]),
                      correction=(next(''.join(str(int(b)) for b in h) for h in answers[s])
                                  if answers[s] else None),
                      buttons=list(closure(s, moves)[goal]) if answers[s] else None)
                 for s in states]
    }


if __name__ == '__main__':
    print(json.dumps(replay(), indent=2))
