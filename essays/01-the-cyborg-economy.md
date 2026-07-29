# The Cyborg Economy Is Not a Labor Forecast

*What I am building, what it can measure, and why "opportunity" is a more honest unit than "jobs created."*

A job is a bundle of tasks held together by an organization.

The bundle has a title, a manager, a salary, a schedule, a benefits package,
and a long list of assumptions inherited from the industrial economy. Someone
decided that these particular tasks belong together, that one person should
perform most of them, and that the bundle should persist for months or years.

AI loosens that bundle.

A scientist can use an agent to search literature outside her specialty. A
small-business owner can perform analysis that once required a separate
department. A developer can move from idea to tested implementation without
handing every intermediate task to another occupation. OpenAI's July 2026
analysis of more than 800,000 U.S. ChatGPT messages calls this **task
crossover**: 43.5% of occupation-specific messages concerned work associated
with another occupation.[^openai-crossover]

That is not proof that jobs disappear. It is evidence that the boundary around
the job is already becoming porous.

The economic actor emerging through that boundary is a cyborg, not the
science-fiction body of chrome and wires but a person whose mind is extended
into the machine through AI. I named this trajectory "cyborgization" in 2015,
drawing on extended-mind theory: cognition is not sealed inside the skull but
partly carried by the tools a person thinks through.[^cyborgization] What I
described then as a forecast is now the default condition of knowledge work.

Today a cyborg is typically an augmented human with a fleet of agents. The
human is the pilot. The AI is the copilot. The human has extended mind and will
into the machine, and the machine extends reach without supplying its own will.
I define an agent in this context as a force multiplier of human will and
intelligence, not an autonomous decision-maker. The agent proposes, searches,
translates, and executes; the principal chooses, judges, and remains
responsible.

A cyborg operator may do the work of a former team. A cyborg scientist may
direct a swarm of search, coding, simulation, and verification agents. An
autonomous agent may complete an entire machine-readable task while a human
principal chooses the objective and remains responsible for the external
effect.

This is the "force multiplier productivity flywheel": each task a cyborg
completes feeds back into faster, broader capability for the next, so a single
human can do in hours or days what once took dozens of people months of labor.
The job market is not returning to the shape that made those teams necessary.

This essay, and the site carrying it, is a product of that flywheel. I am
writing it with AI copilots as a cyborg, and the math, code, and illustrations
it references were produced the same way.

The question for my work is not, "How many old jobs can we preserve?"

It is:

> Can we create more open surfaces where a useful result has a visible
> specification, a checkable completion rule, and a funded payout?

<figure>
  <object type="image/svg+xml" data="../assets/essays/cyborg-opportunity-loop.svg" role="img" aria-label="A loop from useful activity to realized fees, open tasks, human and agent work, verified results, and renewed activity.">
    The cyborg opportunity loop connects useful activity, realized fees, open
    tasks, human-agent work, verification, and renewed activity.
  </object>
  <figcaption>Paid opportunity is a loop only after useful activity produces real fees and verified work returns value.</figcaption>
</figure>

## The claim I refuse to make

It is easy to market an AI platform with a large number.

Start with a giant market. Assume a share of that market moves through the
platform. Multiply by a fee. Divide by an annual salary. Announce "jobs
created."

The arithmetic can be correct while the conclusion is fiction.

One person may run thousands of agents. One proof-mining company may supply
most of a network's computation. A reproduction or curation task may require
hours of irreducibly human attention. The same reward pool could be distributed
among ten full-time specialists, thousands of occasional contributors, one
highly automated operator, or machines whose ultimate ownership is difficult
to observe.

Fees do not contain a human-count variable.

That is why I use a narrower model.

Let:

- \(F\) be realized gross fees;
- \(\theta\) be the fraction allocated to task or provider rewards;
- \(u\) be the fraction of that allocation actually settled;
- \(r\) be the average payout per verified task.

Then \(R=F\theta u\) is the settled reward pool, and \(N=\frac{R}{r}\) is the
number of paid task settlements the pool can support.

Those equations identify economic capacity. They do not identify people,
jobs, livelihoods, adoption, welfare, or income distribution.

This distinction matters because task count is easy to manipulate. A $510,000
pool can support 1,020 settlements at $500 each or 51,000 settlements at $10
each. The number of task records increases fiftyfold. The reward value does not
change.

The primary economic metric is therefore **settled reward value**. Paid task
count is a secondary operational metric that must remain paired with average
payout, uniqueness, validity, and usefulness.

## What my public systems could fund

My repositories contain several different economic machines. PopperPad can
publish proof, counterexample, reproduction, maintenance, preservation, and
curation work. ZenoDEX can expose solving, routing, proving, challenging, and
verification roles around an exchange. PulseTensor can coordinate inference
miners, batch proposers, and challengers.

The table below standardizes them at the same hypothetical input: **$1 million
in realized gross fees**.

| Public project | Settled reward pool | Paid task settlements | What the row means |
|---|---:|---:|---|
| PopperPad | $510,000 | 1,020 at $500 | 60% allocation and 85% settlement utilization |
| ZenoDEX / ZRPF | $360,000 | 360 at $1,000 | 40% allocation and 90% settlement utilization |
| PulseTensor | $910,100 | 9,101 at $100 | 95.8% proposer-plus-miner share and 95% utilization |

These are **conditional scenarios**, not current revenue, launch parameters, or
forecasts. The current realized-fee input is zero, so the current modeled
settled pool is zero. PulseTensor's 95.8% provider share is grounded in its
published tokenomics; the other displayed allocations, utilization rates, and
payouts are editable assumptions.[^popperpad][^zenodex][^pulsetensor]

That honesty makes the model more useful, not less. It gives readers a
reproducible translation:

> If the system produces this much fee-bearing activity, and if this visible
> share is routed and settled, then this much paid opportunity follows.

Anyone can replace the assumptions. No one has to accept a story about the
future to check the multiplication.

## Jevons after intelligence becomes cheap

The strongest argument for a larger task economy rests on cheaper cognition
expanding the set of things worth attempting, not on every current job
surviving.

William Stanley Jevons observed in 1865 that a more efficient steam engine did
not necessarily reduce coal use. Greater efficiency reduced the effective cost
of useful work, which made more uses economical. If demand responded strongly
enough, total resource use increased.[^jevons]

The same mechanism may apply to machine intelligence.

Let \(g\) be the compute required per task and let task demand have absolute
price elasticity \(\varepsilon\). Under a simple constant-elasticity model,
aggregate compute use is proportional to \(g^{1-\varepsilon}\). When
efficiency improves, \(g\) falls. If \(\varepsilon>1\), demand expands by more
than the efficiency gain and total compute use rises. That is the strict Jevons
case.

<figure>
  <object type="image/svg+xml" data="../assets/essays/jevons-task-expansion.svg" role="img" aria-label="As compute per task falls, the number of affordable tasks expands; total compute rises only when demand elasticity exceeds one.">
    A Jevons diagram showing lower compute per task, more affordable tasks, and
    the elasticity condition for total compute to rise.
  </object>
  <figcaption>Efficiency expands the feasible task frontier. Whether total resource use rises depends on demand elasticity.</figcaption>
</figure>

This is a condition, not a prophecy.

AI may make one legal analysis cheaper without creating enough new demand to
replace the old labor. It may make a million previously uneconomic scientific
checks affordable. It may generate enormous machine activity with little
reward reaching independent people. It may lower costs while a few platforms
capture most of the surplus.

Jevons tells us why "efficiency means fewer tasks" is incomplete. It does not
tell us who receives the gains.

That distribution problem has to be designed and measured separately.

## Open to whom?

"Open task" can become another empty phrase unless the interface is concrete.

For my purposes, a task is meaningfully open when:

1. it can be discovered without a private introduction;
2. its inputs and required outputs are machine-readable;
3. eligibility is permissionless or its restrictions are explicit;
4. the completion test is declared before work begins;
5. the payout rule is declared before work begins;
6. a valid result can be verified without trusting the submitter;
7. duplicate work, challenges, and settlement are handled by visible rules.

That structure is useful to a human, an autonomous agent, or a human-agent
team. It does not mean everyone can profit. Compute, capital, identity,
expertise, geography, regulation, and timing still constrain participation.
But the opportunity surface is legible enough for an agent to scan, estimate
expected value, attempt the work, and submit evidence.

PopperPad's design draft makes this explicit with a machine-readable work-order
object and a universal agent loop: find a bounty, fetch the evidence bundle,
run or improve the check, submit a proof or counterexample, survive the
challenge window, and receive a payout if the declared verifier accepts the
result.[^popperpad-game]

The platform does not vote a claim true because someone paid. It pays after a
verifier-accepted epistemic result.

That reversal, **evidence before payment, not payment before truth**, is the
design pattern running through my portfolio.

## My value is not "more code"

AI makes code abundant. Abundance reduces the signaling value of code volume.
Lines written, hours saved, and even replacement cost remain useful accounting
figures, but they no longer capture the main contribution.

The value I aim to create is architectural:

- turn an aspiration into a machine-readable task;
- turn a task into a predeclared acceptance condition;
- turn an AI output into an untrusted proposal;
- turn verification into a deterministic boundary;
- turn fee-bearing use into a conserved reward pool;
- turn the reward pool into open, measurable opportunity;
- preserve the evidence so someone else can replay the claim.

This is what I mean by building the cyborg economy.

I am not trying to encode my philosophy into every user's software. A protocol
can aim at local user happiness: an interface that produces satisfaction in the
person sitting in front of it is a legitimate utilitarian target. What no
single app can do is control the global state of the world. A protocol cannot
guarantee liberty, democratic institutions, capitalism, privacy, safety, or a
fair distribution of AI wealth across populations. Those values conflict at the
margins, and reasonable people choose different tradeoffs. Safety, for example,
can be increased through controls that reduce freedom and exit.

The platform contract should be smaller:

> Publish the task. Expose the rule. Verify the result. Account for the money.

My political reason for building that infrastructure is personal. I want a
future in which advanced AI increases the number of people capable of acting,
not only the capacity of the institutions already in control. I want humans
with AI assistants to create new industries, discover new facts, participate
in markets, and protect what they value.

That motivation does not make the outcome inevitable.

It makes the work worth attempting.

## No one is coming

My first job was referral marketing. Later I earned from blogging, crypto
mining, liquidity provision, and yield farming. None of those income streams
looked like a permanent occupation before its enabling network existed.

Bitcoin defined a reward rule without predicting the future population of
miners, pools, data centers, firms, or human operators. Industrial organization
formed around the opportunity. Proof of work expanded into other proof systems,
staking, routing, liquidity provision, and forms of protocol work that were
difficult to name in advance.

The post-AGI economy may be similarly generative.

The airplane safety rule applies: secure your own oxygen mask before helping
others. Use the productivity flywheel to build your own capability first, then
use that capability to create opportunity for others.

> No one is coming. Use the productivity as a force multiplier to create new
> industries, new tasks, and new ways to protect what you value.

Some opportunities will be tiny. Some will be automated almost completely.
Some will demand human judgment precisely because judgment has become the
scarce input. Some will fail. A few may become industries.

The honest claim is not "I created a million jobs."

It is:

> I build systems that can turn real use into transparent, verifiable, paid
> opportunity, and I publish the math required to tell capacity from hype.

That is how I intend to contribute to a better world: not by promising the
distribution of a wealth that does not yet exist, but by building more ways for
people and their agents to participate in creating it.

---

**Metadata**

- **Slug:** `the-cyborg-economy`
- **Description:** A rigorous case for measuring AI-era economic opportunity
  through fee-funded reward pools and verified tasks, not speculative jobs.
- **Topics:** AI economics, agents, task markets, human agency, mechanism design
- **Primary CTA:** Explore PopperPad
- **Secondary CTA:** Open the fee-funded task-economy model

[^openai-crossover]: OpenAI, "[How AI is expanding what people do at work](https://openai.com/index/how-ai-is-expanding-what-people-do-at-work/)," July 27, 2026.
[^cyborgization]: Dana Edwards and Alexander J. Karran, "[Cyborgization: A Possible Solution to Errors in Human Decision Making?](https://transpolitica.org/2015/07/07/cyborgization-a-possible-solution-to-errors-in-human-decision-making/)," Transpolitica, July 7, 2015.
[^popperpad]: Dana Edwards, "[PopperPad](https://github.com/TheDarkLightX/PopperPad)," public alpha repository.
[^zenodex]: Dana Edwards, "[ZenoDEX](https://github.com/TheDarkLightX/ZenoDEX)," public-testnet candidate repository.
[^pulsetensor]: Dana Edwards, "[PulseTensor tokenomics](https://github.com/TheDarkLightX/PulseTensor/blob/main/docs/tokenomics.md)," game-theoretic draft.
[^jevons]: William Stanley Jevons, *The Coal Question* (1865), [source note and scan](https://energyhistory.yale.edu/w-stanley-jevons-the-coal-question-1865/), Yale Energy History.
[^popperpad-game]: Dana Edwards, "[Algorithmic Game Theory Decentralization](https://github.com/TheDarkLightX/PopperPad/blob/main/docs/algorithmic-game-theory-decentralization.md)," PopperPad design draft.
