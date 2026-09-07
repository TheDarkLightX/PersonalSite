# How I Measure Code After AI

*Lines of code are becoming cheap. The valuable question is what new agency, evidence, and opportunity the system makes possible.*

I measure software by what it helps people do.

AI makes the limits of counting lines especially clear.

AI can generate code, tests, and documentation quickly. To assess the result, I need to know whether it works, how it was checked, and who can use it.

I also track time saved, estimated replacement cost, and revenue when it exists. To assess the wider benefits, I need to ask what each system is meant to accomplish.

PopperPad is valuable if it makes a scientific claim easier to falsify,
reproduce, and remember. ZenoDEX is valuable if it gives more actors a
checkable way to participate in exchange, solving, proving, and verification.
PulseTensor is valuable if funded inference can settle through visible rules to
providers and challengers.

Each contribution needs a measurement that reflects its purpose.

My proposal is an **agency ledger**: a set of public measurements
showing what opportunity the system funds, what decisions remain under an
accountable principal, what results are verifiable, how easily a participant
can enter or exit, and how concentrated the outcome becomes.

> My main question is what the code lets someone do. Counts of lines, commits, and completed tickets can provide context, but they tell me little about that on their own.

<figure>
  <object type="image/svg+xml" data="../assets/essays/agency-ledger.svg" role="img" aria-label="A multidimensional ledger reports opportunity, verifier coverage, principal control, openness, portability, and concentration separately, without collapsing them into one score.">
    A six-dimensional agency ledger keeps opportunity, verification, control,
    openness, portability, and concentration as separate measurements.
  </object>
  <figcaption>A system can improve one dimension while weakening another. The ledger keeps the tradeoff visible.</figcaption>
</figure>

## Choosing how much each measure counts

I have a personal philosophy. It is broadly concerned with human flourishing,
popular access to power, and the practical ability to pursue a life one has
reason to value.

People using the platform should be able to judge the measurements according to their own values.

There is no neutral weight telling us how much privacy to trade for fraud
detection, how much safety to trade for exit, or how much efficiency to trade
for redundancy. A government could maximize one definition of safety through
maximum control. A protocol could maximize permissionless access while
externalizing risks onto people least able to bear them.

Combining those variables into one score would require choices about how much each should count. Those choices need an explanation.

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

> I report six measurements, explain how each was calculated, and let you decide how much weight to give them.

## Dimension one: paid opportunity

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

| Project | Settled reward value | Paid settlements | Main tasks |
|---|---:|---:|---|
| PopperPad | $510,000 | 1,020 at $500 | Proof, refutation, reproduction, maintenance, preservation |
| ZenoDEX / ZRPF | $360,000 | 360 at $1,000 | Solving, routing, proving, challenging, verification |
| PulseTensor | $910,100 | 9,101 at $100 | Inference mining, batch proposing, challenging |

These are conditional translations, not current results. Current modeled
realized fees are zero. Parameters are illustrative except where a repository
explicitly defines them.

> I have designed systems whose fees could fund rewards for useful tasks. The calculations show what those rewards could be if actual use produces the assumed fees.

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

## Dimension three: control coverage

Human control depends on which decisions a person can understand, change, or stop.

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

The weighting policy must be published. The result measures the specified controls. Measuring effects on wellbeing requires further evidence.

For the cyborg scientist, the relevant boundaries include claim scope,
research context, trust policy, publication, and high-impact action. For a
DEX participant, they include signing, custody, risk limits, governance
delegation, and exit. For an autonomous service, they include spending limits,
identity use, and irreversible communication.

The design should preserve the person's control over consequential actions while allowing routine steps to run automatically.

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

Clear task rules help people and agents assess eligibility, costs, and possible rewards.

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

PopperPad stores objects locally, identifies them by content hashes, and works offline, which helps make the research record portable. For a DEX, self-custody and public
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

It shows how concentrated the payouts are.

## What this says about my projects

The same codebase can contribute along several dimensions.

### PopperPad

- **Opportunity:** machine-readable work orders for proofs, counterexamples,
  reproductions, boundary discovery, maintenance, storage, and curation.
- **Verification:** results whose stated scope is supported by evidence that can be replayed.
- **Control:** local trust policy and human choice over the question, context,
  and consequential use.
- **Exit:** pads that work offline, identify objects by content hashes, and can be copied and replayed.
- **Intended benefit:** make errors cheaper to discover, correct
  results easier to reproduce, and scientific memory harder to erase.

### ZenoDEX

- **Opportunity:** solver, router, proof-miner, challenger, reporter, watcher,
  and verification work funded from public fee rules.
- **Verification:** integer-exact settlement, certificate checks, formal checks, and public replay.
- **Control:** explicit signing, custody, risk, fee, and governance boundaries.
- **Exit:** on-chain assets and state reduce one class of intermediary
  dependence, while remaining bridge, oracle, and frontend dependencies must
  be measured.
- **Intended benefit:** make direct participation in an automated
  capital economy more technically possible.

### PulseTensor

- **Opportunity:** miner, validator, batch proposer, and challenger roles around
  funded inference.
- **Verification:** challenge windows, bonded batch roots, and fail-closed
  settlement policy.
- **Control:** timelocked, cancellable fee-policy changes snapshotted at batch
  commit.
- **Economic boundary:** usage fees provide the funding for providers and development.
- **Intended benefit:** distribute parts of inference production and
  checking across an inspectable protocol.

Adoption and effects on wellbeing still need to be measured.

These are the contributions I would look for as the systems develop.

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

I use software to make rules, responsibilities, and consequences explicit.

The design includes the institutions and incentives around the code.

> I study how technical choices affect incentives and user control. A correct calculation can still reward harmful behavior, and a security measure can still restrict a user. Those interactions shape what I build.

## What I build

My projects bring together people, agents, verification, and rules for payment.

> I build systems that let people and AI agents research, create, and participate in markets. Checkers enforce specified rules, and fees from actual use can fund tasks with clear payment terms.

The supporting material includes:

- public repositories;
- formal specifications and proofs;
- replayable tests and receipts;
- machine-readable work objects;
- records of what is implemented and what remains to be done;
- a Julia model independently cross-checked in Python;
- Lean proofs of the core fee algebra;
- scenario workbooks that calculate task settlements and state the limits of those estimates.

I would also assess what people can do with these systems.

I want a person with an AI assistant to be able to formulate a task, attempt useful work, verify a result, participate in a market, control consequential decisions, and leave with their evidence or assets. The wider effects on wealth, liberty, and safety will require evidence beyond the software itself.

These capabilities give people more ways to pursue their own goals.

That is the contribution I know how to measure, and the one I intend to keep
building.

> Measure what people can do with the system, and show how you checked it.

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
