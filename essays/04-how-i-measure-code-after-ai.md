# How I Measure Code After AI

*Lines of code are becoming cheap. The valuable question is what new agency, evidence, and opportunity the system makes possible.*

"How much code did you write?" was never a good measure of software.

It is becoming an absurd one.

An AI system can generate thousands of lines before lunch. It can port a
library, scaffold a service, write tests, produce documentation, and imitate the
surface architecture of a mature product. The number is real. The implied value
is not.

Time saved is better. Replacement cost is useful. Revenue is essential when it
exists. Yet all three can miss the reason I build a particular system.

PopperPad is valuable if it makes a scientific claim easier to falsify,
reproduce, and remember. ZenoDEX is valuable if it gives more actors a
checkable way to participate in exchange, solving, proving, and verification.
PulseTensor is valuable if funded inference can settle through visible rules to
providers and challengers.

Those contributions are not captured by code volume.

They can still be measured.

My proposal is an **agency ledger**: a small vector of public measurements
showing what opportunity the system funds, what decisions remain under an
accountable principal, what results are verifiable, how easily a participant
can enter or exit, and how concentrated the outcome becomes.

Not one score.

A ledger.

> I have been offered the single score my whole career. Lines, commits,
> tickets closed, story points burned. Every one of them was a way to avoid
> asking what the code actually let someone do.

<figure>
  <object type="image/svg+xml" data="../assets/essays/agency-ledger.svg" role="img" aria-label="A multidimensional ledger reports opportunity, verifier coverage, principal control, openness, portability, and concentration separately, without collapsing them into one score.">
    A six-dimensional agency ledger keeps opportunity, verification, control,
    openness, portability, and concentration as separate measurements.
  </object>
  <figcaption>A system can improve one dimension while weakening another. The ledger keeps the tradeoff visible.</figcaption>
</figure>

## Why a single impact score would be dishonest

I have a personal philosophy. It is broadly concerned with human flourishing,
popular access to power, and the practical ability to pursue a life one has
reason to value.

That philosophy should not be compiled into a universal platform score.

There is no neutral weight telling us how much privacy to trade for fraud
detection, how much safety to trade for exit, or how much efficiency to trade
for redundancy. A government could maximize one definition of safety through
maximum control. A protocol could maximize permissionless access while
externalizing risks onto people least able to bear them.

If I multiplied all of those variables into "82.4 agency points," the precision
would be theatrical.

The measurements should remain separate so a user, reviewer, community, or
governance process can apply its own values.

This is consistent with the architecture running through my work:

```text
Model proposes.
Verifier decides a scoped claim.
People decide what the claim is for.
```

Formal methods can prove that an integer invariant holds. They cannot prove
that a society selected the right objective.

> I will not pretend to have a number I do not have. I will give you six
> numbers that together tell the truth, and let you weigh them with your own
> values.

## Dimension one: paid opportunity

The first dimension is economic and intentionally simple.

Let:

- \(F\) be realized fees;
- \(\theta\) be the share allocated to task or provider rewards;
- \(u\) be the share actually settled;
- \(r\) be the average payout per valid task.

Then \(R=F\theta u\) is the settled reward value, and \(N=\frac{R}{r}\) is the
number of paid task settlements. Report both.

Never report \(N\) without \(R\), because the same pool can be divided into an
arbitrarily large number of tiny records. Never divide \(R\) by a salary and
call the result people. One human may run thousands of agents. One agent may
serve many human principals. The operator count is not in the equation.

For current planning, my public-project scenarios at $1 million in realized
fees are:

| Project | Settled reward value | Paid settlements | Primary work surface |
|---|---:|---:|---|
| PopperPad | $510,000 | 1,020 at $500 | Proof, refutation, reproduction, maintenance, preservation |
| ZenoDEX / ZRPF | $360,000 | 360 at $1,000 | Solving, routing, proving, challenging, verification |
| PulseTensor | $910,100 | 9,101 at $100 | Inference mining, batch proposing, challenging |

These are conditional translations, not current results. Current modeled
realized fees are zero. Parameters are illustrative except where a repository
explicitly defines them.

The statement is therefore:

> I have designed codebases whose fee surfaces can be translated into
> auditable reward capacity if and when real use produces fees.

That is stronger than a speculative employment number because the claim can be
recomputed and later compared with reality.

## Dimension two: verifier coverage

AI makes proposals cheap. Verification becomes the scarce boundary.

For task settlement, I would measure:

\[
\text{VerifierCoverage}
=
\frac{
\text{payout value backed by replayable verifier-accepted evidence}
}{
\text{total settled task payout value}
}
\]

The numerator is value-weighted. A platform should not claim 99% coverage by
verifying thousands of one-cent tasks while one large payout remains
discretionary.

"Verifier" is contextual. Lean may decide whether a proof term checks. A
deterministic replay may decide whether a transaction produces a committed
state. A benchmark harness may decide whether an output meets a stated
threshold. A verifier cannot decide whether a theorem is important, an
experiment is ethical, or a policy is legitimate.

The metric says: *the declared check ran and accepted this evidence under this
context.*

Nothing more.

## Dimension three: principal-control coverage

Human-in-the-loop is a placement, not a power relationship.

A person can click "approve" after a system has hidden every meaningful
alternative. Another system can automate ten thousand reversible microsteps
while preserving a person's veto over the irreversible boundary.

The second system may provide more control with fewer approvals.

For each consequential workflow path \(j\), assign a transparent value or risk
weight \(v_j\). Let \(control_j=1\) only if an accountable principal:

1. sets or accepts the objective;
2. can inspect the evidence relevant to the boundary;
3. can veto the irreversible external effect.

Then:

\[
\text{PrincipalControlCoverage}
=
\frac{\sum_j v_j\,control_j}{\sum_j v_j}
\]

The weighting policy must be published. The result measures an architecture
property, not human wellbeing.

For the cyborg scientist, the relevant boundaries include claim scope,
research context, trust policy, publication, and high-impact action. For a
DEX participant, they include signing, custody, risk limits, governance
delegation, and exit. For an autonomous service, they include spending limits,
identity use, and irreversible communication.

The design goal is keeping the principal in control of what matters, not
interrupting the agent continuously.

## Dimension four: machine-readable openness

A GitHub issue is visible to a person. An open task market should also be
legible to an agent.

I would count a task as machine-readable and open only when it has:

- public discovery or a documented open feed;
- canonical input references;
- a typed required output;
- explicit eligibility constraints;
- a completion rule declared before work begins;
- a payout rule declared before work begins;
- duplicate and challenge handling;
- a settlement reference.

Then report:

\[
\text{OpenTaskValueShare}
=
\frac{
\text{payout value from tasks meeting those conditions}
}{
\text{total task payout value}
}
\]

This metric is stricter than "anyone can participate." Some tasks require a
bond, specialized hardware, licensed data, capital, or jurisdictional
eligibility. Those constraints should be machine-readable too.

The aim is legibility, not a false promise of universal profit.

## Dimension five: exit and portability

Agency includes the ability to say no and continue elsewhere.

Dan Larimer's writing on freedom repeatedly returns to dependence on a single
provider and the practical importance of exit, redundancy, and local
control.[^larimer-freedom] That question can be turned into a software
measurement.

For stateful systems:

\[
\text{PortableStateCoverage}
=
\frac{
\text{value-weighted user state exportable in a documented independent format}
}{
\text{total value-weighted user state}
}
\]

For PopperPad, content-addressed local objects and an offline-first pad make
portability part of the base architecture. For a DEX, self-custody and public
state are necessary but not sufficient; frontend diversity, bridge dependence,
oracle dependence, and governance keys still matter. For an agent platform,
prompts, memory, identities, tool policies, and evidence should not become a
private format that traps the principal.

Portability creates a credible threat of exit.

That threat disciplines power even when most users stay.

## Dimension six: concentration

An open protocol can produce a concentrated economy.

Report distribution after settlement:

- top-one payout share;
- top-ten payout share;
- concentration of liquidity, stake, solving, proving, validation, and
  infrastructure;
- inverse-Herfindahl effective recipients:

\[
E_{\text{effective}}=\frac{1}{\sum_i s_i^2}
\]

where \(s_i\) is recipient \(i\)'s payout share.

One hundred equal recipients produce an effective count of 100. If one receives
80% and the other 99 recipients split the rest, the effective count is about
1.56.

Addresses are not automatically independent people, so the label must remain
"effective recipients" unless identity evidence supports something stronger.

Concentration is not always a defect. Specialized proof systems may have large
economies of scale. Emergency governance may be deliberately narrow. The
ledger does not decide the acceptable threshold.

It makes the shape visible.

## What this says about my projects

The same codebase can contribute along several dimensions.

### PopperPad

- **Opportunity:** machine-readable work orders for proofs, counterexamples,
  reproductions, boundary discovery, maintenance, storage, and curation.
- **Verification:** scoped results derived from replayable evidence rather than
  token voting or author assertion.
- **Control:** local trust policy and human choice over the question, context,
  and consequential use.
- **Exit:** offline-first, content-addressed pads that can be mirrored and
  replayed.
- **World-improving mechanism:** make errors cheaper to discover, correct
  results easier to reproduce, and scientific memory harder to erase.

### ZenoDEX

- **Opportunity:** solver, router, proof-miner, challenger, reporter, watcher,
  and verification work funded from visible fee rails.
- **Verification:** integer-exact settlement, certificate checks, formal
  surfaces, and public replay.
- **Control:** explicit signing, custody, risk, fee, and governance boundaries.
- **Exit:** on-chain assets and state reduce one class of intermediary
  dependence, while remaining bridge, oracle, and frontend dependencies must
  be measured.
- **World-improving mechanism:** make direct participation in an automated
  capital economy more technically possible.

### PulseTensor

- **Opportunity:** miner, validator, batch proposer, and challenger roles around
  funded inference.
- **Verification:** challenge windows, bonded batch roots, and fail-closed
  settlement policy.
- **Control:** timelocked, cancellable fee-policy changes snapshotted at batch
  commit.
- **Economic boundary:** usage fees fund providers and development rather than
  assuming a grant.
- **World-improving mechanism:** distribute parts of inference production and
  checking across an inspectable protocol.

None of these bullets proves adoption or broad welfare.

They show the pathway by which a working system could produce an observable
contribution.

## The value I bring

My portfolio crosses engineering, formal methods, mechanism design, political
philosophy, and economic modeling because the interesting failures happen at
their boundaries.

A mathematically correct settlement rule can support a destructive incentive.
A well-intentioned market can pay unverifiable output. A capable model can
optimize the wrong claim. A decentralized protocol can concentrate in
practice. A "safe" system can remove meaningful user control. A thousand
generated features can leave no one better able to act.

The work I bring is to make those boundaries explicit:

1. state the ambitious reason for building;
2. reduce it to a mechanism the software can enforce;
3. define the evidence that would support the mechanism's claim;
4. make AI-generated output an untrusted proposal;
5. make verification and settlement replayable;
6. model how real fees become paid task capacity;
7. report the dimensions that the mechanism does not solve.

That is more than efficient code generation.

It is institutional engineering at software scale.

> The interesting failures are never inside one discipline. They live in the
> gap between a correct proof and a destructive market, between a safe system
> and a controlled user. I build in those gaps.

## A line I can defend

Here is the value proposition I want a reviewer to leave with:

> I build proof-carrying systems for the cyborg economy: people set
> direction, agents perform scalable work, deterministic gates decide what
> counts, and transparent fee rules can turn verified output into open paid
> opportunity.

Every clause has evidence:

- public repositories;
- formal specifications and proofs;
- replayable tests and receipts;
- machine-readable work objects;
- explicit implementation-status boundaries;
- a Julia model independently cross-checked in Python;
- Lean proofs of the core fee algebra;
- scenario workbooks that do not pretend tasks are people.

The world-improving claim is equally bounded.

I cannot guarantee that advanced AI distributes wealth, preserves liberty, or
produces a safe and free society. I can build more systems in which a person
with an AI assistant can formulate a task, attempt useful work, verify a
result, participate in a market, retain decision rights, and leave with their
evidence or assets.

Those are capabilities.

Capabilities enlarge the space in which people can pursue their own ends.

That is the contribution I know how to measure, and the one I intend to keep
building.

> Measure what lets people act, not what lets you report. The first builds
> capability. The second builds a slide.

---

**Metadata**

- **Slug:** `how-i-measure-code-after-ai`
- **Description:** A portfolio framework for measuring software by paid
  opportunity, verifier coverage, principal control, openness, portability,
  and concentration, not lines of code.
- **Topics:** software value, AI engineering, human agency, formal methods,
  portfolio
- **Primary CTA:** Review the public evidence
- **Secondary CTA:** Download the economic model

[^larimer-freedom]: Daniel Larimer, "[How to Find Freedom in an Unfree World](https://bytemaster.medium.com/how-to-find-freedom-in-a-unfree-world-59a416a0e8e0)," February 4, 2019.
