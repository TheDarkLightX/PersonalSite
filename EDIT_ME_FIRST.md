# Edit me first

This prototype is intentionally opinionated. Personalize a few items before treating it as the final public site.

## Decide before publishing

- Add a preferred email, LinkedIn, and CV link if those should be public.
- Keep ESSO and ZAG labeled as private unless public demo extracts are published.
- Add a real headshot if it increases trust. The current local image is the GitHub avatar.
- Decide whether the employer brief should stay public or serve as an interview/application packet.

## Keep these ideas

- The homepage should stay organized around reviewer evidence.
- Every selected project should have a reviewer path.
- Every ambitious claim should have scope, evidence, assumptions, and limitations.
- AI usage should be framed as "untrusted proposer, verified outputs only."

## Recommended next content files to create in flagship repositories

- `REVIEWER_GUIDE.md`
- `CLAIMS.md`
- `THREAT_MODEL.md`
- `LIMITATIONS.md`
- `AI_USAGE.md`

## Recommended next public repo

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
