# Dana Edwards Personal Site

Static resume portfolio for Dana Edwards, hosted with GitHub Pages at:

```text
https://www.danaedwards.info/
```

The site presents public work around formal methods, AI assurance, proof-carrying execution, deterministic policy gates, and replayable verification evidence.

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
value.html                          Quantitative value case (rarity, costly signals, cost estimates)
writing.html                        Tutorial and lab index (61 tutorials, 12 interactive labs)
metrics.html                        Redirect stub to value.html (legacy)
data/portfolio-metrics.json         Generated metrics consumed by value.html
tools/collect_portfolio_metrics.py  Regenerates portfolio-metrics.json from the public repos
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
