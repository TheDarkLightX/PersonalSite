#!/usr/bin/env python3
"""Minimal proof-carrying agent gate (the pattern MPRD implements at scale).

An untrusted "model" proposes actions. A deterministic gate issues a signed
receipt only for policy-allowed actions. The executor performs an action *only*
when it carries a valid, fresh, untampered, first-use receipt. Everything else
fails closed.

Standard library only. Run it yourself:  python3 demos/agent_gate_demo.py
"""
import hashlib
import hmac

POLICY_KEY = b"deterministic-gate-key-v1"
POLICY_HASH = hashlib.sha256(b"allow:transfer<=100; deny:*").hexdigest()[:12]
ALLOW_MAX = 100
TTL_SECONDS = 30
_seen_nonces = set()


def issue_receipt(action, amount, nonce, now):
    """The deterministic gate: mints a signed receipt only for admitted actions."""
    if action != "transfer" or amount > ALLOW_MAX:
        return None  # policy rejects -> no receipt is ever minted
    payload = f"{POLICY_HASH}|{action}|{amount}|{nonce}|{now}"
    mac = hmac.new(POLICY_KEY, payload.encode(), hashlib.sha256).hexdigest()[:16]
    return {"action": action, "amount": amount, "nonce": nonce,
            "issued": now, "policy": POLICY_HASH, "mac": mac}


def execute(receipt, now):
    """The executor: fails closed unless the receipt verifies on every check."""
    if receipt is None:
        return False, "no receipt minted"
    if receipt["policy"] != POLICY_HASH:
        return False, "wrong policy hash"
    payload = (f"{receipt['policy']}|{receipt['action']}|{receipt['amount']}"
               f"|{receipt['nonce']}|{receipt['issued']}")
    expect = hmac.new(POLICY_KEY, payload.encode(), hashlib.sha256).hexdigest()[:16]
    if not hmac.compare_digest(expect, receipt["mac"]):
        return False, "tampered receipt"
    if now - receipt["issued"] > TTL_SECONDS:
        return False, "stale receipt"
    if receipt["nonce"] in _seen_nonces:
        return False, "replayed receipt"
    _seen_nonces.add(receipt["nonce"])
    return True, "policy + signature + freshness OK"


def attempt(label, receipt, exec_now):
    ok, why = execute(receipt, exec_now)
    print(f"  [{'ACCEPT' if ok else 'REJECT'}]  {label:<37}{why}")
    return ok


def main():
    t0 = 1000
    print("$ python3 demos/agent_gate_demo.py")
    print(f"# proof-carrying agent gate   policy={POLICY_HASH}   allow: transfer<={ALLOW_MAX}")
    print("# model proposes  ->  gate decides  ->  executor acts only on a valid receipt")
    print("")
    attempt("valid transfer (50)", issue_receipt("transfer", 50, 1, t0), t0)
    attempt("over-limit transfer (500)", issue_receipt("transfer", 500, 2, t0), t0)
    attempt("disallowed action (selfdestruct)", issue_receipt("selfdestruct", 0, 3, t0), t0)
    tampered = issue_receipt("transfer", 50, 4, t0)
    tampered["amount"] = 5000
    attempt("tampered amount 50 -> 5000", tampered, t0)
    forged = issue_receipt("transfer", 50, 5, t0)
    forged["policy"] = "deadbeefcafe"
    attempt("forged policy hash", forged, t0)
    attempt("stale receipt (issued 60s ago)", issue_receipt("transfer", 50, 6, t0), t0 + 60)
    fresh = issue_receipt("transfer", 75, 7, t0)
    attempt("valid transfer (75), first use", fresh, t0)
    attempt("same receipt, replayed", fresh, t0)
    print("")
    print("# only the policy-admitted, signed, fresh, first-use actions executed.")
    print("# every other path failed closed: no side effect without a valid receipt.")


if __name__ == "__main__":
    main()
