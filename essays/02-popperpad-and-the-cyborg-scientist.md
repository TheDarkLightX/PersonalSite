# PopperPad and the Cyborg Scientist

*When answers become cheap, deciding what is worth testing, and preserving the evidence, becomes more valuable.*

Imagine a scientist beginning the day with a question she wants to test.

She describes a hypothesis to an AI research partner. The agent searches papers
across fields, translates unfamiliar notation, writes code, proposes a
simulation, calls a theorem prover, and finds three results that appear to
support the claim.

It also finds a counterexample.

The counterexample reveals a flaw in the hypothesis. One assumption in the original
hypothesis was too broad. The scientist narrows the claim, reruns the
experiment, and asks another agent to reproduce the result from a clean
environment. A verifier checks the formal fragment. A replay harness checks the
empirical artifact. The failed version, corrected version, recipes, logs,
contexts, and attestations remain connected in an append-only graph.

The agents helped her read, write code, and run checks.

She directed the investigation.

She chose the question. She decided which assumptions mattered. She determined
whether the model's translation preserved the meaning of the claim. She chose
what evidence was relevant, what risk justified another experiment, and what
result was responsible to publish.

I am building PopperPad for this kind of scientist: someone who uses agents to investigate more questions while retaining judgment and responsibility.

<figure>
  <object type="image/svg+xml" data="../assets/essays/cyborg-scientist.svg" role="img" aria-label="A human scientist sets direction, AI agents search broadly, formal and empirical verifiers filter results, and PopperPad preserves the accepted evidence and refutations.">
    The cyborg scientist directs agent search, verifier checks, and append-only
    scientific memory.
  </object>
  <figcaption>The human selects meaning and direction; agents search; verifiers decide scoped checks; PopperPad remembers.</figcaption>
</figure>

## Judgment is the scarce input

When I guide a research system, I choose the question, the methods, and the evidence needed to assess the result.

My role begins when I decide what is worth investigating.

OpenAI's recent writing also emphasizes human judgment. In April, Sam Altman wrote that
AI "will give people more capability and agency."[^altman-principles] In June,
Altman and Jakub Pachocki wrote:

> "As AI systems become more capable, the human role becomes more important."

Their explanation names direction, tradeoffs, judgment, values, taste, care,
and responsibility.[^openai-plan]

PopperPad gives that division of labor a technical shape.

An AI system is unusually good at existential work: propose a candidate, search
a large space, find an example, translate a representation, generate a test,
try another proof path. A verifier is unusually good at a bounded universal
question: does this candidate satisfy the declared rule in this declared
context? A human remains responsible for the open-world questions the verifier
cannot settle: Is this the right claim? Is the context honest? Is the model
missing a stakeholder? Does the evidence justify action outside the formal
boundary? Is the question worth asking?

The roles are different:

```text
Human principal:  chooses ends, context, tradeoffs, publication, responsibility
AI agents:        propose, search, translate, simulate, minimize, reproduce
Verifiers:        check declared predicates over declared artifacts
PopperPad:        preserve claims, evidence, lineage, disputes, and replay
```

Agents can take on more tasks while a person retains control over the objective, interpretation, and consequential actions.

That boundary follows the line between syntax and semantics.

An agent manipulates syntax: it arranges symbols, transforms representations,
searches a space, generates candidates, and checks whether a form satisfies a
rule. These are operations over structure. They do not require the agent to
know what the symbols mean in the world.

A human supplies semantics: meaning, intent, reference, and purpose. An agent
can write a Given/When/Then story, but the human decides which behavior matters,
who the user is, and what experience the system serves. The syntactic
scaffolding is the easy part. The semantic question, what is this for and who
is it for, is the part that cannot be delegated without also delegating
responsibility.

An agent can use an interface, read inputs, and produce outputs. I design the system around the person directing it: what they want to accomplish, what they need to understand, and which decisions they must control.

The ultimate concern behind that priority is human happiness. I think that
concern can be described by the utilitarian calculus: arrangements are better
when they produce more wellbeing for more people, and worse when they produce
less. At the local level of a single user sitting at a single interface, a
platform can and should attempt to create an experience that produces
satisfaction and happiness in that user. User satisfaction is a utilitarian
target, and it is one a piece of software can legitimately aim at.

What no single app can do is control the global state of the world. A protocol
cannot maximize world happiness, distribute wellbeing across populations, or
resolve the conflicts between safety, freedom, efficiency, and distribution
that play out across millions of people and institutions. The utilitarian
calculus explains why I choose to keep humans at the center of the design. It
does not claim that one platform computes a global utility term. The local
experience is mine to shape; the global equilibrium is not.

PopperPad encodes that priority. A knowledge patch carries syntactic form: a
claim, a recipe, evidence, a proof or counterexample. Its semantic value,
whether this is the right claim, whether it matters, whether it is responsible
to publish, remains with the human principal who set the context and accepts
the consequence.

## Scientific memory for humans and agents

PopperPad is a ledger that works offline and records hypotheses, recipes, evidence, counterexamples, artifacts, and relationships between claims. Attempts to refute a claim are part of the research record.[^popperpad-readme]

> PopperPad records each claim, how it was checked, the supporting and conflicting evidence, and the context of the result. The check or experiment supplies the evidence for the claim.

Objects are content-addressed. Events are append-only. A newer result can
supersede or narrow an older one without erasing the path that led there.
The recorded verifier evidence determines whether a claim is marked supported, falsified, or disputed.

As AI produces more hypotheses, summaries, experiments, and proof sketches, I need better ways to choose what to test, trace its sources, reproduce the results, and remember what failed.

More claims create more work for independent checking.

PopperPad's proposed market would pay for these contributions:

| Work product | What an agent or cyborg contributes | What must be checked |
|---|---|---|
| Proof | A certificate for a scoped formal claim | Accepted verifier, exact claim and context binding |
| Counterexample | An input or trace that breaks a claim | Reproduction under the declared recipe |
| Reproduction | Independent replay of a result | Environment, artifacts, outputs, and signature |
| Boundary discovery | A narrower claim that survives after failure | Counterexample to the old scope and evidence for the new |
| Recipe maintenance | A working check after tools or dependencies change | Semantics preserved across the update |
| Artifact preservation | Durable availability of evidence bundles | Content hash and retrieval challenge |
| Curation | Useful duplicate, refutation, and lineage relationships | Useful links that preserve the recorded evidence and status |

A **knowledge patch** contains a claim,
context, recipe, evidence, artifacts, signatures, and a proof, replay, or
counterexample that changes what a careful reader should believe.

That patch can be produced by a human, an agent, or a team. Its eligibility for payment depends on the evidence and the declared task rules.

## A market that buys criticism

New findings often attract more attention than attempts to reproduce them.

A dramatic claim can attract attention before anyone has reproduced it. A correction may receive less attention, even when it reveals a failure under a different compiler or in a different population.

I want PopperPad to make careful criticism worth doing.

It can create open work orders for:

- the smallest counterexample to a formal claim;
- an independent reproduction on a specified platform;
- a proof for a bounded theorem;
- a portability repair for a dead recipe;
- a retrieval challenge for an evidence archive;
- a sharper boundary around an overbroad result.

Payment follows the evidence checks and challenge period:

```text
declared task
→ submitted evidence
→ verifier-accepted result
→ challenge window
→ settlement
```

Never:

```text
payment
→ claim becomes true
```

The repository expresses the incentive test for an autonomous worker as
\(EV(\text{task}) = \Pr(\text{success})\cdot \text{reward} -\text{cost}
-\Pr(\text{slash})\cdot \text{bond}\). An agent attempts PopperPad work when
that expected value exceeds its best alternative use of compute, time,
capital, and expertise.[^popperpad-game]

The market would pay for research tasks whose results meet the declared checks.

## What the fee math says

My capacity model funds rewards from fees earned through actual use.

The model starts only after real use produces real fees. Let \(F\) be realized
gross fees, \(\theta\) the share allocated to epistemic tasks, and \(u\) the
share actually settled. Then \(R=F\theta u\) is the settled reward pool. If
the average verified task pays \(r\), then \(N=\frac{F\theta u}{r}\) is the
number of paid task settlements.

Here is a hypothetical scenario for inspecting the calculation:

```text
realized annual fees             $1,000,000
task allocation θ                       60%
settlement utilization u                85%
settled reward pool R              $510,000
average verified payout r              $500
paid task settlements N               1,020
```

That could mean 1,020 proof, refutation, reproduction, maintenance,
preservation, and curation settlements in some mixture. It does not mean 1,020
people. One operator might manage many agents. Reproductions that need considerable human attention might distribute work more broadly. Until payouts exist, neither the
human share nor the concentration is known.

Current realized fees are zero in the model. Current modeled reward capacity is
therefore zero.

The calculation shows what the system could fund if fees were earned.

## How to measure whether the opportunity is real

A platform can inflate "tasks created" by subdividing work. It can inflate
"contributors" with addresses. It can call an agent retry a new job. PopperPad
needs measurements that resist those incentives.

I would report:

1. **Settled epistemic reward value.** How much was actually paid for verified
   work?
2. **Unique verified settlements.** How many non-duplicate knowledge patches
   passed the declared rule?
3. **Verifier coverage.** What share of payout value is backed by replayable
   verifier-accepted evidence?
4. **Reproduction depth.** How many important results have independent replay that checks the stated context?
5. **Claims improved after refutation.** How often did a counterexample help define a narrower claim that survived testing?
6. **Payout concentration.** What shares went to the top one and top ten
   recipients, and what is the inverse-Herfindahl effective recipient count?
7. **Share paid for open tasks.** What share of payout value came from tasks with
   public discovery, machine-readable inputs, explicit eligibility, declared
   verification, and predeclared payout rules?

These measures help assess the funding, verification, and distribution of research tasks. Judging scientific importance and effects on wellbeing requires further evidence.

## Responsibility requires control over the boundary

The boundary is the line between what an agent may do on its own and what
requires the principal's decision. Inside the boundary, the agent searches,
proposes, translates, and checks. At the boundary, the principal sets the
objective, accepts the context, inspects the evidence, and can veto the
irreversible. Responsibility tracks that line: a person who cannot control the
boundary cannot be held accountable for what crosses it.

The person directing the system needs practical control over its consequential decisions.

A person can be nominally present while the system makes every consequential
choice, presents one default, hides alternatives, and makes reversal expensive.
Conversely, a person can retain meaningful control without approving every
tool call.

The relevant question is whether an accountable principal:

- sets the research objective;
- chooses or accepts the claim context;
- can inspect the evidence lineage;
- controls which verifier and trust policy count locally;
- can veto publication or an irreversible external effect;
- can export the pad and continue without the platform operator.

I call the value-weighted share of consequential paths with those properties
**control coverage**. It measures the stated controls. Their practical effect depends on how the system is used.

These controls also matter when agents help develop new AI systems.

As agents take on more implementation, I expect research judgment to remain valuable: choosing what to build, defining the requirements, designing checks, recognizing when a model solves the wrong problem, and taking responsibility for deployment.

PopperPad is infrastructure for that role.

## What I am contributing

I built storage that identifies objects by content hashes, a history that retains earlier records, recipes for repeating checks, evidence capture, and connections to formal tools. The project also derives claim status from the graph and includes designs for structured work orders.

The proposed research and payment process is:

```text
Question → Claim → Check → Evidence → Challenge → Memory → Reward
```

This process lets agents contribute while people direct the investigation. It preserves errors and corrections so the next scientist can inspect how a result was reached and which tests it survived.

PopperPad is still a public alpha. The repository explicitly warns that recipe
execution is not an operating-system sandbox and automated bounty settlement
is not yet a production security boundary.[^popperpad-readme] Those limits determine what the current release can safely support.

The scientist needs a record she can question and check.

I want to make errors easier to find and reproduce, pay for useful corrections, and preserve what the investigation teaches us.

---

**Metadata**

- **Slug:** `popperpad-cyborg-scientist`
- **Description:** PopperPad turns proofs, counterexamples, reproductions, and
  scientific maintenance into checkable work for humans and agents, while
  keeping direction and responsibility with people.
- **Topics:** PopperPad, science, AI agents, falsification, human judgment
- **Primary CTA:** Inspect PopperPad on GitHub
- **Secondary CTA:** Read the falsification-market design

[^altman-principles]: Sam Altman, "[Our principles](https://openai.com/index/our-principles/)," OpenAI, April 26, 2026.
[^openai-plan]: Sam Altman and Jakub Pachocki, "[Built to benefit everyone: our plan](https://openai.com/index/built-to-benefit-everyone-our-plan/)," OpenAI, June 8, 2026.
[^popperpad-readme]: Dana Edwards, "[PopperPad](https://github.com/TheDarkLightX/PopperPad)," public alpha repository and README.
[^popperpad-game]: Dana Edwards, "[Algorithmic Game Theory Decentralization](https://github.com/TheDarkLightX/PopperPad/blob/main/docs/algorithmic-game-theory-decentralization.md)," PopperPad design draft.
