"""Rebuild the film's two finite ZAL models with integrations/zal on PYTHONPATH."""
import json
from itertools import combinations
from pathlib import Path

from zal_notation import builtin, core, semantics

STRAND = "AGCGUU"
ALLOWED = {"AU", "UA", "GC", "CG", "GU", "UG"}
PAIRS = tuple((i, j) for i, j in combinations(range(1, len(STRAND) + 1), 2)
              if STRAND[i - 1] + STRAND[j - 1] in ALLOWED)
PAPER = ("((()))", "(()())", "([())]", "(()[)]")


def intersects(a, b):
    i, j = a
    k, l = b
    return i < k < j < l or k < i < l < j


def event(pair):
    return "-".join(map(str, pair))


def state(pairs):
    return "+".join(map(event, pairs)) or "empty"


def decode(brackets):
    starts = {"(": [], "[": []}
    pairs = []
    for i, symbol in enumerate(brackets, 1):
        if symbol in starts:
            starts[symbol].append(i)
        else:
            pairs.append((starts[{")": "(", "]": "["}[symbol]].pop(), i))
    return tuple(sorted(pairs))


def build(allow_crossing):
    legal = {()}
    edges = []
    for n in range(1, len(STRAND) // 2 + 1):
        for pairs in combinations(PAIRS, n):
            if len({p for edge in pairs for p in edge}) < 2 * n:
                continue
            if not allow_crossing and any(intersects(a, b) for a, b in combinations(pairs, 2)):
                continue
            legal.add(pairs)
            parent, child, label = state(pairs[:-1]), state(pairs), event(pairs[-1])
            edges.append({"id": child, "tag": "transition", "source": [parent, "out"],
                          "target": [child, "in"], "fields": {"event": label, "outcome": "pair"}})
    best = max(map(len, legal))
    winners = {pairs for pairs in legal if len(pairs) == best}
    nodes = [{"id": state(pairs), "tag": "start" if not pairs else
              "accepting" if pairs in winners else "state", "fields": {"name": state(pairs)}}
             for pairs in sorted(legal)]
    grammar = builtin.fsm_grammar()
    model = builtin.model(grammar, {"nodes": nodes, "edges": edges})
    table = semantics.fsm_check(grammar, model)
    assert table["structural_valid"] and table["initial_valid"] and table["deterministic"]
    # Each fold has a single canonical event order. Replay each compatible fold,
    # including those refused by the nesting restriction.
    replay = {}
    for n in range(4):
        for pairs in combinations(PAIRS, n):
            if len({p for edge in pairs for p in edge}) != 2 * n:
                continue
            trace = semantics.fsm_trace(grammar, model, list(map(event, pairs)))
            assert (trace["status"] == "completed") == (pairs in legal)
            if pairs in legal:
                assert trace["final_state"] == state(pairs)
            replay[state(pairs)] = trace["status"]
    return {"crossings": allow_crossing, "maxScore": best, "winnerCount": len(winners),
            "winners": sorted(winners), "model": model, "modelDigest": core.digest(model),
            "replay": replay}


def main():
    narrow, wide = build(False), build(True)
    paper = [decode(text) for text in PAPER]
    assert narrow["maxScore"] == wide["maxScore"] == 3
    assert set(narrow["winners"]) == set(paper[:2])
    assert set(wide["winners"]) == set(paper)
    result = {"sequence": STRAND, "scope": "Compatible matchings on these six positions, one point per pair. Comparison of optimal folds with Appendix A, not a general RNA energy model.",
              "paper": "https://www.bioinf.uni-leipzig.de/~choener/pdfs/rie-hoe-2016.pdf#page=34",
              "examples": [{"brackets": s, "pairs": pairs} for s, pairs in zip(PAPER, paper)],
              "nested": narrow, "extended": wide}
    Path(__file__).with_name("model.json").write_text(json.dumps(result, separators=(",", ":")) + "\n")
    print("Replayed", len(wide["replay"]), "compatible folds in both models.",
          narrow["winnerCount"], "and", wide["winnerCount"], "winners, three points each.")


if __name__ == "__main__":
    main()
