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

## Site Mechanics (added in the redesign)

- No theme flash on load: a tiny inline script in each page `<head>` sets light/dark from
  `localStorage` or the OS preference before the stylesheet loads. The visible control is the
  sun/moon button, which also updates the `theme-color` meta.
- Navigation collapses to a hamburger under 900px (`data-nav-toggle` toggles `#primary-nav`).
- `script.js` also runs scroll-spy (active nav link), motion-safe scroll-reveal, and
  visibility-gated looping demo videos. All motion respects `prefers-reduced-motion`.

## Project Media

Drop files into `assets/projects/<slug>/` (slugs: `mprd`, `zenodex`, `formal-methods-philosophy`):

```text
cover.png    16:9 homepage card thumbnail (~1280x720, <=150KB). Shows automatically.
poster.png   Poster frame for a case-study demo video (<=200KB).
demo.webm    Looping muted screen capture (<=10-15s, 720p). Add demo.mp4 as fallback.
shot-01.png  Optional gallery screenshots / proof output.
```

Until a `cover.png` exists, the homepage card shows a gradient placeholder (the `<img>` removes
itself on a 404). To turn a case-study "coming soon" box into a real clip, replace the
`<div class="card-media">...</div>` inside that `.media-figure` with:

```html
<video data-autoplay muted loop playsinline preload="none" poster="../assets/projects/<slug>/poster.png" width="1280" height="720" aria-label="short description">
  <source src="../assets/projects/<slug>/demo.webm" type="video/webm" />
  <source src="../assets/projects/<slug>/demo.mp4" type="video/mp4" />
</video>
```

## Before You Publish

- [x] Public email set to `p33rl3ss1@gmail.com` (the `mailto:` in `index.html`). Change it there if
      you ever move to a domain address.
- [ ] Optionally add a downloadable CV PDF. The site is the canonical CV either way.
- [ ] Re-run `tools/collect_portfolio_metrics.py` before publishing so figures and market comparables
      are current; market caps and exploit-loss totals move.
- [ ] Keep every quantitative claim sourced and dated. Dollar figures are replacement-cost /
      conventional build-cost estimates and category benchmarks, not valuations. Do not restate them
      as market value.
- [ ] Add real project recordings/screenshots per the convention above.
