# Dana Edwards Personal Site

My personal site, hosted with GitHub Pages at:

```text
https://www.danaedwards.info/
```

I am an engineer, philosopher, and futurist. This site brings together my projects, writing, research methods, and capabilities with AI and other tools.

## Files

```text
index.html                          Main homepage
404.html                            GitHub Pages fallback page
robots.txt                          Search crawler policy
sitemap.xml                         Canonical public URLs
CNAME                               GitHub Pages custom domain
.nojekyll                           Disable Jekyll processing
style.css                           Design system and responsive styling
script.js                           Theme, mobile nav, scroll-spy, reveal, media autoplay, year
assets/mark.svg                     Site mark
assets/dana-github-avatar.png       Local GitHub avatar asset
case-studies/mprd.html              MPRD case study page
case-studies/zenodex.html           ZenoDEX case study page
case-studies/research-kernel.html   Research Kernel MCP case study page
value.html                          Current value, curated capabilities, outcomes, and evidence paths
data/cost-model-inputs.json          Dated public commits, wages, and cost-scenario assumptions
data/cost-estimates.json             Current three-repository cost sensitivity and comparison
tools/collect_cost_estimates.py      Replays the cost snapshot from pinned Git objects
tools/render_cost_estimates.py       Renders the Value cost section from the computed snapshot
docs/cost-estimates.md               Cost methodology, limitations, and replay instructions
assets/blender/                     Original maze-checker and workflow-scaling illustrations
writing.html                        Tutorial and interactive lab index
network.html                        Professional network: people I work with, communities I contribute to
ideas.html                          Somewhat original ideas I helped popularize, with lineages
metrics.html                        Redirect stub to value.html (legacy)
data/portfolio-metrics.json         Historical footprint and effort-model data (dated snapshot)
tools/collect_portfolio_metrics.py  Historical collector and shared footprint exclusions
assets/projects/<slug>/             Project screenshots (app.webp; see EDIT_ME_FIRST.md)
EDIT_ME_FIRST.md                    Content maintenance checklist
```

## Run Locally

Open `index.html` directly in a browser, or run a local static server:

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

## Publish

GitHub Pages should use:

```text
Source: Deploy from a branch
Branch: main
Folder: / (root)
Custom domain: www.danaedwards.info
```

The root `CNAME` file must contain:

```text
www.danaedwards.info
```

## Content Rules

- Keep the homepage organized around reviewer evidence.
- Every selected project should have a reviewer path.
- Every ambitious claim should have scope, evidence, assumptions, and limitations.
- Keep unpublished tools out of the public portfolio unless a reviewer-safe public extract exists.
- AI usage should be framed as untrusted proposer, verified outputs only.
