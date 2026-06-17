# Dana Edwards Personal Website Prototype

This is a no-build static portfolio prototype for Dana Edwards. It is an Evidence first portfolio and CV booster around:

> Proof-carrying, fail-closed systems for AI-mediated action, deterministic policy, formal models, tests, and replayable execution evidence.

GitHub profile: <https://github.com/TheDarkLightX/>

## Files

```text
index.html                          Main homepage
style.css                           Design system and responsive styling
script.js                           Theme toggle and current year
assets/mark.svg                     Generated SVG mark
assets/dana-github-avatar.png       Local GitHub avatar asset
case-studies/mprd.html              MPRD case study page
case-studies/zenodex.html           ZenoDEX case study page
packets/employer-brief.html         General employer reviewer brief
EDIT_ME_FIRST.md                    Personalization checklist
```

## GitHub SSH checks used

Repository access was checked with SSH-style GitHub remotes:

```bash
ssh -T -o BatchMode=yes git@github.com
git ls-remote git@github.com:TheDarkLightX/MPRD.git
git ls-remote git@github.com:TheDarkLightX/ZenoDEX.git
git ls-remote git@github.com:TheDarkLightX/Formal_Methods_Philosophy.git
```

## Run locally

Open `index.html` directly in a browser, or run a tiny local server:

```bash
cd personal_site_prototype
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

## Host for free

### Option 1: GitHub Pages

1. Create a repo, for example `personal-site`.
2. Copy these files into the repo root.
3. Commit and push.
4. In GitHub, go to Settings -> Pages.
5. Choose deploy from branch, usually `main` and `/root`.
6. Later, point a domain to GitHub Pages if desired.

### Option 2: Cloudflare Pages

1. Create a GitHub repo with these files.
2. Connect the repo to Cloudflare Pages.
3. Use no build command.
4. Use `/` as the output directory.

### Option 3: Netlify

1. Drag and drop the folder into Netlify.
2. No build command needed.

## Design intent

This site is designed to make Dana's work legible to serious reviewers:

- homepage = identity and selected evidence
- case studies = what to inspect, claim scope, and limits
- employer brief = general reviewer path for hiring teams
- writing roadmap = public technical identity

## Publishing checklist

Before publishing:

- Add preferred email, LinkedIn, and CV links if Dana wants them public.
- Add screenshots or diagrams if useful.
- Keep ESSO and ZAG labeled as private unless public demo extracts are published.
- Add `CLAIMS.md`, `REVIEWER_GUIDE.md`, and `AI_USAGE.md` to flagship repos.
- Build the tiny `proof-carrying-agent-gate` demo and link it from the homepage.
