# Project media

Drop per-project screenshots and recordings here. One folder per project slug:

- `mprd/`
- `zenodex/`
- `formal-methods-philosophy/`

Filenames the site looks for (all optional — the site degrades gracefully without them):

```text
cover.png    16:9 homepage card thumbnail (~1280x720, <=150KB). Appears automatically.
poster.png   Poster frame for a case-study demo video (<=200KB).
demo.webm    Looping muted screen capture (<=10-15s, 720p). Add demo.mp4 as an H.264 fallback.
shot-01.png  Optional gallery screenshots / proof output.
```

Performance budget: always keep the 16:9 aspect ratio (the layout reserves the box, so there is no
layout shift), prefer muted looping `<video>` over GIF, and keep each demo clip under a few MB.

See `../../EDIT_ME_FIRST.md` for the exact HTML snippet to swap a "coming soon" placeholder for a
real video.
