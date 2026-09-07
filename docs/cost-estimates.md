# Cost estimate refresh: September 6, 2026

The Value page refreshes the June 2026 **conventional rebuild-cost sensitivity**
for the same three public repositories: MPRD, ZenoDEX, and Formal Methods
Philosophy. Other portfolio projects and unpublished work are outside the scope.
It does not estimate my market value, an actual project quote,
measured savings, or equivalent human engineering years.

## Source of truth

- [Pinned commits and wage inputs](../data/cost-model-inputs.json)
- [Computed snapshot, per-repository results and sensitivities](../data/cost-estimates.json)
- [Git-object collector](../tools/collect_cost_estimates.py)
- [Static page renderer](../tools/render_cost_estimates.py)
- [Original June dataset](../data/portfolio-metrics.json), preserved unchanged

The public default-branch commits were checked against GitHub on September 6,
2026. Their full commit and tree hashes are in the input file. The collector reads
those Git objects directly, so later commits, dirty files, the staging area and
untracked files do not alter a replay. The dated snapshot has no changing run
timestamp. Its file manifest can be regenerated and checked against `manifest_sha256`.

## Measurement and calculation

The refresh retains `SOURCE_EXT`, `is_publish_headline_file`, and the publication
path exclusions from the June collector. It counts nonblank lines in selected
source/proof files. Comments, tests and examples are included. This is **not
physical SLOC**, which would exclude comments. It is not an authorship measure.
Tests and proofs are included in the file footprint once, without extra charges.
Exact duplicate files are reported but retained for comparison with June.
The filters exclude known vendor, generated, data, internal, and specified
derived-runtime paths. They do not prove the absence of all copied or generated
content. No semantic deduplication or contribution audit was performed.

Let K = selected nonblank lines / 1,000. The legacy scenarios are:

- Lower: person-months = 2.4 × K^1.05; cost = person-months / 12 × $135,980 × 1.50.
- Higher: person-months = 3.0 × K^1.12; cost = person-months / 12 × $214,670 × 1.38.

The coefficients are Basic COCOMO organic and semidetached parameters, documented
in the [SLOCCount author's guide](https://dwheeler.com/sloccount/sloccount.html).
We apply them to a nonblank-line proxy to preserve the earlier calculation. The
equations have not been calibrated for these repositories, modern AI-assisted
development, formal proofs, or mixed research artifacts. This is an extrapolation,
not a validated prediction or confidence interval.

The [BLS Occupational Outlook Handbook](https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm)
reports May 2025 software-developer annual wages of $135,980 at the median and a
$214,670 threshold for the highest 10 percent. The page was modified August 27,
2026 and checked September 6, 2026. The two labor multipliers remain the site's
June assumptions; they are not BLS estimates of employer overhead. No inflation
forecast is applied. External audit, legal, deployment and operating costs are
not separately estimated.

The headline pools all three source sizes before exponentiation, matching the
June method. The page also shows per-repository scenarios and their sum because
pooling raises the nonlinear result. Size sensitivities at 25%, 50%, and 100% are
arbitrary assumptions, not measured AI productivity discounts. The original June
market-cap and contributor-account comparisons are historical and are not
represented as refreshed inputs to this cost estimate.

## Reproduce

Use Python 3.11+ and Git. Obtain each public repository at the exact commit in
`data/cost-model-inputs.json`; a bare repository is sufficient. For example:

```sh
git clone --bare https://github.com/TheDarkLightX/MPRD.git /tmp/cost-MPRD.git
git clone --bare https://github.com/TheDarkLightX/ZenoDEX.git /tmp/cost-ZenoDEX.git
git clone --bare https://github.com/TheDarkLightX/Formal_Methods_Philosophy.git /tmp/cost-Formal.git
python3 tools/collect_cost_estimates.py \
  --repo MPRD=/tmp/cost-MPRD.git \
  --repo ZenoDEX=/tmp/cost-ZenoDEX.git \
  --repo Formal_Methods_Philosophy=/tmp/cost-Formal.git \
  --manifest /tmp/cost-file-manifest.json \
  --check
python3 tools/render_cost_estimates.py --check
python3 -m unittest discover -s tools -p 'test_cost_estimates.py'
```

To refresh later, first update the dated public commit/tree hashes and sourced
wage assumptions in the input file. Run the collector without `--check`, then
run the renderer without `--check`. Review the scope and source exclusions before
publishing, and verify the rendered values against the saved JSON. The historical
June snapshot is retained for comparison and should not be overwritten by a
new run of the older collector.
