#!/usr/bin/env python3
"""Bounded exhaustive proof search with counterexamples (the Formal Methods Philosophy idea).

Testing can show the presence of bugs; exhaustive search over a bounded domain can show
their absence *in that domain* -- or hand back a concrete counterexample that exposes a
missing assumption. This is the loop the tutorials and labs teach: claim -> search ->
counterexample -> tighten the claim.

Standard library only. Run it yourself:  python3 demos/bounded_check_demo.py
"""
BOUND = 256  # x, y range over [0, BOUND)


def check(predicate, admissible=lambda x, y: True):
    """Exhaustively evaluate predicate over the bounded grid. Returns (checked, counterexample)."""
    checked = 0
    for x in range(BOUND):
        for y in range(BOUND):
            if not admissible(x, y):
                continue
            checked += 1
            if not predicate(x, y):
                return checked, (x, y)
    return checked, None


def report(claim, predicate, admissible=lambda x, y: True):
    n, cex = check(predicate, admissible)
    if cex is None:
        print(f"  [HOLDS]   {claim}")
        print(f"            checked {n:,} cases, no counterexample (bounded proof)")
    else:
        x, y = cex
        print(f"  [FAILS]   {claim}")
        print(f"            counterexample x={x}, y={y}  (found after {n:,} cases)")
    return cex


def main():
    print("$ python3 demos/bounded_check_demo.py")
    print(f"# bounded exhaustive proof search   domain: x,y in [0,{BOUND})   {BOUND*BOUND:,} cases")
    print("")
    report("claim 1: XOR is involutive   (x ^ y) ^ y == x",
           lambda x, y: ((x ^ y) ^ y) == x)
    print("")
    cex = report("claim 2: modular add never wraps below   (x + y) % 256 >= x",
                 lambda x, y: (x + y) % 256 >= x)
    if cex:
        x, y = cex
        print(f"            testing missed it; the search exposed the missing assumption:")
        print(f"            ({x} + {y}) % 256 = {(x + y) % 256}, which is < {x}  (silent overflow)")
    print("")
    report("claim 3 (repaired, assume x + y < 256):   (x + y) % 256 >= x",
           lambda x, y: (x + y) % 256 >= x,
           admissible=lambda x, y: x + y < 256)
    print("")
    print("# a passing test proves nothing universal; a bounded search proves it, or finds the")
    print("# counterexample that tells you which assumption your claim was missing.")


if __name__ == "__main__":
    main()
