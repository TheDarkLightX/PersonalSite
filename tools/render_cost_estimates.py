#!/usr/bin/env python3
"""Render the cost section from the saved, replayable cost snapshot."""
import argparse
import datetime as dt
import html
import json
from pathlib import Path

START = "    <!-- cost-estimates:start -->"
END = "    <!-- cost-estimates:end -->"


def money(value):
    return f"${value / 1_000_000:,.1f}M"


def cost_range(scenarios):
    return f"{money(scenarios['low']['cost_usd'])}–{money(scenarios['high']['cost_usd'])}"


def render(data):
    inputs = data['inputs']
    wages = inputs['wages']
    date = dt.date.fromisoformat(data['as_of']).strftime('%B %d, %Y').replace(' 0', ' ')
    rows = []
    for repo in data['repositories']:
        name = html.escape(repo['name'].replace('_', ' '))
        url = html.escape(repo['url'] + '/tree/' + repo['commit'], quote=True)
        rows.append(f'              <tr><th scope="row"><a href="{url}">{name}</a><small>{repo["commit"][:12]}</small></th><td>{repo["selected_nonblank_lines"]:,}</td><td>{cost_range(repo["scenarios"])}</td></tr>')
    sensitivity = ''.join(f'<li><strong>{row["input_fraction"]:.0%} of the counted size:</strong> {cost_range(row["scenarios"])}</li>' for row in data['size_sensitivity'])
    pooled = cost_range(data['pooled_scenarios'])
    summed = data['sum_of_repository_scenarios_usd']
    prior = data['baseline']
    return f'''{START}
    <section class="section" id="cost-estimates" aria-labelledby="cost-heading">
      <div class="container">
        <div class="section-heading">
          <p class="eyebrow">Cost model · Updated {date}</p>
          <h2 id="cost-heading">What would conventional development cost?</h2>
          <p>A refreshed version of the earlier code-volume model, covering MPRD, ZenoDEX, and Formal Methods Philosophy. Other portfolio projects and unpublished work are outside this estimate.</p>
        </div>
        <div class="cost-summary">
          <p class="eyebrow">Legacy pooled model · USD</p>
          <p class="cost-range">{pooled}</p>
          <p>Illustrative conventional rebuild-cost scenarios. These are model outputs, not a quote, measured savings, or my market value. The range is not a confidence interval.</p>
        </div>
        <p>The latest public commits contain <strong>{data['selected_nonblank_lines']:,} selected nonblank lines</strong> across {data['selected_files']:,} files, up {prior['line_change_percent']:.1f}% from {prior['selected_nonblank_lines']:,} in June. The count includes comments, tests, proofs, and examples within selected source files; it is a size proxy rather than physical source lines of code or verified authorship.</p>
        <p class="cost-scroll-hint">Scroll the table horizontally to see each estimate.</p>
        <div class="cost-table-wrap" role="region" aria-label="Repository cost scenarios; scroll horizontally on small screens" tabindex="0">
          <table class="cost-table">
            <caption>Per-repository cost scenarios</caption>
            <thead><tr><th scope="col">Repository / pinned commit</th><th scope="col">Nonblank lines</th><th scope="col">Cost scenarios</th></tr></thead>
            <tbody>
{chr(10).join(rows)}
            </tbody>
            <tfoot><tr><th scope="row">Sum of separate estimates</th><td>{data['selected_nonblank_lines']:,}</td><td>{money(summed['low'])}–{money(summed['high'])}</td></tr></tfoot>
          </table>
        </div>
        <p class="value-note">The headline retains the earlier method of pooling all three repositories before applying the formula. That produces a larger number than adding three separate estimates because effort scales nonlinearly. The original June pooled result was {money(prior['low_cost_usd'])}–{money(prior['high_cost_usd'])} under the older wage inputs.</p>
        <details class="cost-assumptions">
          <summary>Assumptions, sensitivity, and what the estimate can establish</summary>
          <h3>Inputs and calculation</h3>
          <p>Let K be selected nonblank lines divided by 1,000. The retained Basic COCOMO equations produce person-months: 2.4 × K<sup>1.05</sup> for the lower scenario and 3.0 × K<sup>1.12</sup> for the higher scenario. Cost equals person-months ÷ 12 × annual wage × labor multiplier. <a href="{html.escape(inputs['model_source'], quote=True)}">Formula reference</a>.</p>
          <p>The <a href="{html.escape(wages['source'], quote=True)}">BLS May 2025 wage data</a>, checked {date}, supplies ${wages['median_annual_usd']:,} at the median and ${wages['p90_annual_usd']:,} at the 90th-percentile threshold. The respective labor multipliers remain 1.50 and 1.38, giving assumed annual labor costs of ${wages['median_annual_usd'] * inputs['scenarios']['low']['labor_multiplier']:,.0f} and ${wages['p90_annual_usd'] * inputs['scenarios']['high']['labor_multiplier']:,.0f}. These multipliers are assumptions, not measured employer costs. No inflation forecast is added.</p>
          <h3>How much the size assumption matters</h3>
          <ul>{sensitivity}</ul>
          <p>The smaller-size cases are arbitrary sensitivity checks. They are not measured AI productivity discounts or estimates of how much work a rebuild would actually require.</p>
          <h3>Limits of this model</h3>
          <p>These older equations are extrapolated from a nonblank-line proxy and have not been calibrated for my repositories, AI-assisted development, formal proofs, or research artifacts. They do not establish equivalent human engineering years, production readiness, or the cost of reproducing the same functionality with a different design.</p>
          <p>The collector retains the June source extensions and path exclusions for comparability. Known vendor, generated, data, internal, and specified derived-runtime paths are excluded; path filters cannot establish that every third-party or generated file is absent. Exact duplicate files remain in this comparison and are reported in the data. There is no semantic deduplication or authorship audit. Tests and proofs are counted within the footprint, without adding a second labor charge.</p>
          <p>External audits, legal fees, deployment, and ongoing operations are not separately priced. A useful project quote would require a defined scope, acceptance criteria, a reuse plan, and measured delivery rates.</p>
        </details>
        <div class="card-actions"><a href="data/cost-estimates.json">Dated estimates and source commits</a><a href="data/cost-model-inputs.json">Wages and assumptions</a><a href="https://github.com/TheDarkLightX/PersonalSite/blob/main/docs/cost-estimates.md">Method and replay instructions</a></div>
      </div>
    </section>
{END}'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=Path('data/cost-estimates.json'))
    parser.add_argument('--page', type=Path, default=Path('value.html'))
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    page = args.page.read_text()
    if page.count(START) != 1 or page.count(END) != 1:
        raise SystemExit('Expected exactly one cost section marker pair')
    before, rest = page.split(START)
    current, after = rest.split(END)
    updated = before + render(json.loads(args.data.read_text())) + after
    if args.check:
        if updated != page:
            raise SystemExit('Rendered cost section differs from the saved data')
        print('Rendered cost section matches saved data')
    else:
        args.page.write_text(updated)
        print(f'Updated {args.page}')


if __name__ == '__main__':
    main()
