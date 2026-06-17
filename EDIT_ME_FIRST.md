# Content Maintenance Checklist

Use this before making the site more public or sending it to reviewers.

## Public Profile

- Add a preferred email, LinkedIn, and CV link only if those should be public.
- Keep unpublished tools out of the public portfolio unless a reviewer-safe public extract exists.
- Replace the GitHub avatar with a headshot if that improves trust.
- Decide whether the employer brief should stay public or serve as an interview/application packet.

## Claim Hygiene

- Keep the homepage organized around reviewer evidence.
- Give every selected project a reviewer path.
- Scope every ambitious claim with evidence, assumptions, and limitations.
- Frame AI usage as untrusted proposer, verified outputs only.

## Recommended Next Public Repo

Create:

```text
proof-carrying-agent-gate
```

Small invariant:

```text
No side effect occurs unless the proposed action has a valid policy receipt.
```

Minimal cases:

- valid action -> accepted
- no receipt -> rejected
- tampered receipt -> rejected
- wrong policy hash -> rejected
- replayed receipt -> rejected
