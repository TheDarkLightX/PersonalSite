# Building the Cyborg Economy

*How people and AI agents could create and share new economic opportunities.*

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

This suggests that people can use AI to take on tasks across existing job boundaries.

I use "cyborg" to describe a person who extends their thinking through AI and other tools. I called this process "cyborgization" in 2015, drawing on the theory that tools can become part of how we think.[^cyborgization] Today I use those tools in my own research and creative work.

In my workflow, I set the direction and use agents to help carry it out. Agents propose ideas, search, translate, and execute tasks. I choose the objective, judge the results, and remain responsible for the decisions.

A cyborg operator may do the work of a former team. A cyborg scientist may
direct a swarm of search, coding, simulation, and verification agents. An
autonomous agent may complete an entire machine-readable task while a human
principal chooses the objective and remains responsible for the external
effect.

Each completed task can leave behind useful tools, evidence, and knowledge for the next one. I want to test how much this helps one person accomplish as the tools improve.

I wrote this essay with AI assistance. I use the same process for this site and for the mathematics, code, and illustrations it presents.

I want to investigate this question:

> Can we make more paid tasks publicly available, with clear requirements, a way to check completion, and funding for the payout?

<figure>
  <object type="image/svg+xml" data="../assets/essays/cyborg-opportunity-loop.svg" role="img" aria-label="A loop from useful activity to realized fees, open tasks, human and agent work, verified results, and renewed activity.">
    The cyborg opportunity loop connects useful activity, realized fees, open
    tasks, work by people and agents, verification, and renewed activity.
  </object>
  <figcaption>Paid opportunity is a loop only after useful activity produces real fees and verified work returns value.</figcaption>
</figure>

## What the fee model can tell us

It is easy to market an AI platform with a large number.

Start with a giant market. Assume a share of that market moves through the
platform. Multiply by a fee. Divide by an annual salary. Announce "jobs
created."

The arithmetic can be correct while the conclusion is fiction.

One person may run thousands of agents. One company generating proofs may supply most of a network's computation. A reproduction or curation task may require
hours of irreducibly human attention. The same reward pool could be distributed
among ten full-time specialists, thousands of occasional contributors, one
highly automated operator, or machines whose ultimate ownership is difficult
to observe.

To estimate how many people earn income, I would also need evidence about who receives the payouts.

My model estimates the money available for rewards and the number of task settlements it could fund.

Let:

- \(F\) be realized gross fees;
- \(\theta\) be the fraction allocated to task or provider rewards;
- \(u\) be the fraction of that allocation actually settled;
- \(r\) be the average payout per verified task.

Then \(R=F\theta u\) is the settled reward pool, and \(N=\frac{R}{r}\) is the
number of paid task settlements the pool can support.

These equations estimate reward capacity and task settlements. Measuring people, jobs, livelihoods, adoption, wellbeing, or income distribution requires additional evidence.

This distinction matters because task count is easy to manipulate. A $510,000
pool can support 1,020 settlements at $500 each or 51,000 settlements at $10
each. The number of task records increases fiftyfold. The reward value does not
change.

The primary economic metric is therefore **settled reward value**. Paid task
count is a secondary operational metric that must remain paired with average
payout, uniqueness, validity, and usefulness.

## What my public systems could fund

My repositories explore several ways to fund useful tasks. PopperPad can
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

You can check the calculation from the stated assumptions:

> If actual use produces the assumed fees and the stated share is paid out, the reward pool can fund the calculated number of tasks.

Change the assumptions and repeat the calculation to see how the result changes.

## Jevons after intelligence becomes cheap

Cheaper computation could make more tasks worth attempting and increase the demand for them.

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

Whether this happens depends on how demand responds to lower costs.

AI may make one legal analysis cheaper without creating enough new demand to
replace the old labor. It may make a million previously uneconomic scientific
checks affordable. It may generate enormous machine activity with little
reward reaching independent people. It may lower costs while a few platforms
capture most of the surplus.

Jevons helps explain how efficiency can increase demand. The distribution of the gains depends on ownership, access, and the rules for payment.

I would measure that distribution alongside total activity.

## Open to whom?

I use "open task" for work that people and agents can discover and assess through a public interface.

That requires:

1. it can be discovered without a private introduction;
2. its inputs and required outputs are machine-readable;
3. eligibility is permissionless or its restrictions are explicit;
4. the completion test is declared before work begins;
5. the payout rule is declared before work begins;
6. a valid result can be verified without trusting the submitter;
7. duplicate work, challenges, and settlement are handled by visible rules.

People and agents can use that interface to find tasks, estimate the costs and potential rewards, attempt the work, and submit evidence. Their ability to participate and profit still depends on compute, capital, identity, expertise, geography, regulation, and timing.

PopperPad's design draft makes this explicit with a machine-readable work-order
object and a universal agent loop: find a bounty, fetch the evidence bundle,
run or improve the check, submit a proof or counterexample, survive the
challenge window, and receive a payout if the declared verifier accepts the
result.[^popperpad-game]

Payment follows a result accepted by the declared verifier. The evidence and verification rules determine the status of the claim.

I use this order throughout my projects: check the evidence, then determine whether the result qualifies for payment.

## What I contribute

AI makes code abundant. Abundance reduces the signaling value of code volume.
Lines written, hours saved, and even replacement cost remain useful accounting
figures, but they no longer capture the main contribution.

The value I aim to create is architectural:

- turn an aspiration into a machine-readable task;
- turn a task into a predeclared acceptance condition;
- turn an AI output into an untrusted proposal;
- turn verification into a deterministic boundary;
- allocate a share of fees to a reward pool with checked accounting;
- turn the reward pool into open, measurable opportunity;
- preserve the evidence so someone else can replay the claim.

This is what I mean by building the cyborg economy.

I design for the people using the software. A protocol can aim at local user happiness: an interface that produces satisfaction in the
person sitting in front of it is a legitimate utilitarian target. What no
single app can do is control the global state of the world. A protocol cannot
guarantee liberty, democratic institutions, capitalism, privacy, safety, or a
fair distribution of AI wealth across populations. Those values conflict at the
margins, and reasonable people choose different tradeoffs. Safety, for example,
can be increased through controls that reduce freedom and exit.

The platform contract should be smaller:

> Publish the task. Expose the rule. Verify the result. Account for the money.

I want advanced AI to give more people the means to act on their own goals. I want humans
with AI assistants to create new industries, discover new facts, participate
in markets, and protect what they value.

Whether these systems achieve that goal remains a question for evidence and experience.

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
others. Develop your own capabilities, then use them to create opportunities for others.

> Use the tools available to you to create useful tasks, develop new industries, and protect what you value.

Some opportunities will be tiny. Some will be automated almost completely.
Some will demand human judgment precisely because judgment has become the
scarce input. Some will fail. A few may become industries.

My aim is practical:

> I build systems where actual use can fund useful tasks, with public payment rules and checks for completion. I publish the calculations so people can inspect the assumptions.

I want to give people and their agents more ways to participate in creating wealth.

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
