#!/usr/bin/env python3
"""Deterministic settlement with a replayable certificate (the pattern ZenoDEX implements).

A tiny integer-only constant-product pool settles a batch of swaps in a canonical
order, then emits a settlement certificate (a hash of inputs + outputs + final state).
Re-running from a clean state reproduces the certificate; any tampering changes it.
No floating point is used, so results are exact and bit-reproducible.

Standard library only. Run it yourself:  python3 demos/zenodex_settlement_demo.py
"""
import hashlib

RX0, RY0 = 1_000_000, 1_000_000  # initial pool reserves (integer units)


def settle(swaps):
    """Canonical-order, integer-only settlement. Returns (outputs, reserves, certificate)."""
    rx, ry = RX0, RY0
    outputs = []
    for sid, dx in sorted(swaps):                 # canonical order = sort by id
        dy = (dx * ry) // (rx + dx)               # constant product, integer floor
        rx, ry = rx + dx, ry - dy
        outputs.append((sid, dx, dy))
    blob = repr((sorted(swaps), outputs, (rx, ry))).encode()
    cert = hashlib.sha256(blob).hexdigest()
    return outputs, (rx, ry), cert


def main():
    batch = [("s3", 2000), ("s1", 1000), ("s2", 500)]   # arrives unordered on purpose
    outputs, (rx, ry), cert = settle(batch)

    print("$ python3 demos/zenodex_settlement_demo.py")
    print(f"# deterministic batch settlement   pool X={RX0:,} Y={RY0:,}   integer-only AMM")
    print("# canonical order  ->  exact integer math  ->  replayable certificate")
    print("")
    for sid, dx, dy in outputs:
        print(f"  swap {sid}   +{dx:>4} X  ->  {dy:>4} Y     (exact integer floor)")
    print(f"  final reserves   X={rx:,}   Y={ry:,}")
    print(f"  certificate      sha256={cert[:24]}...")
    print("")

    # replay from a clean state with the inputs reordered again
    _, _, cert_replay = settle(list(reversed(batch)))
    print(f"  replay (reordered inputs)        {'MATCHES ' if cert_replay == cert else 'DIFFERS '}"
          f"-> {'assurance holds' if cert_replay == cert else 'NONDETERMINISM'}")

    # tamper a single order amount
    tampered = [("s2", 600) if sid == "s2" else (sid, dx) for sid, dx in batch]
    _, _, cert_tampered = settle(tampered)
    print(f"  tamper one order (s2: 500->600)  {'DIFFERS ' if cert_tampered != cert else 'MATCHES '}"
          f"-> {'tamper detected' if cert_tampered != cert else 'MISSED'}")
    print("  integer math is exact: no floating-point drift, bit-reproducible certificate")


if __name__ == "__main__":
    main()
