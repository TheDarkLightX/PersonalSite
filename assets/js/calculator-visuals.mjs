import {
  fourPress, ROUND_GAPS, zoomWidth, tickDecimals, copiedCount, savedCount,
  ones, notPattern, xorPattern, parityClosure,
} from './calculator-visuals-core.mjs';

// Keep each static figure visible until its interactive replacement initializes.
const NS = 'http://www.w3.org/2000/svg';
const reducedMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
const commas = n => n.toLocaleString('en-US');
const themeListeners = [];
new MutationObserver(() => themeListeners.forEach(fn => fn()))
  .observe(document.documentElement, {attributes: true, attributeFilter: ['data-theme']});

function svgEl(tag, attrs = {}, parent, text) {
  const node = document.createElementNS(NS, tag);
  for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
  if (text !== undefined) node.textContent = text;
  if (parent) parent.append(node);
  return node;
}

function setup(id, init) {
  const figure = document.getElementById(id);
  if (!figure) return;
  try {
    init(figure);
    figure.classList.add('viz-ready');
  } catch (error) { figure.classList.add('viz-failed'); console.error(error); }
}

function onWidthChange(element, callback) {
  let width = 0;
  const check = () => {
    const next = Math.round(element.getBoundingClientRect().width);
    if (next && next !== width) { width = next; callback(); }
  };
  if ('ResizeObserver' in window) new ResizeObserver(check).observe(element);
  else addEventListener('resize', check);
}

/* ---------- Zoom: watch the four-press recipe approach 1 ---------- */
setup('zoom-figure', figure => {
  const stage = figure.querySelector('.zoom-stage');
  const readout = figure.querySelector('.zoom-readout');
  const stepsBox = figure.querySelector('.zoom-steps');
  const prev = figure.querySelector('[data-zoom="prev"]');
  const next = figure.querySelector('[data-zoom="next"]');
  const play = figure.querySelector('[data-zoom="play"]');
  const last = ROUND_GAPS.length - 1;
  let round = 0;
  let view = {gap: ROUND_GAPS[0], width: zoomWidth(ROUND_GAPS[0])};
  let frame = 0;
  let timer = 0;
  const svg = svgEl('svg', {'aria-hidden': 'true'});
  stage.append(svg);

  const stepButtons = ROUND_GAPS.map((_, i) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = String(i);
    button.setAttribute('aria-label', `Round ${i}`);
    button.addEventListener('click', () => { stop(); go(i); });
    stepsBox.append(button);
    return button;
  });

  function draw(gap, width) {
    const W = Math.max(280, Math.round(stage.getBoundingClientRect().width));
    const H = 150;
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
    svg.setAttribute('height', H);
    svg.replaceChildren();
    const x1 = Math.round(Math.min(72, W * 0.14));
    const right = W - 16;
    const span = right - x1;
    const X = g => x1 + (g / width) * span;
    const axisY = 100;
    svgEl('line', {class: 'z-axis', x1: 4, x2: W - 2, y1: axisY, y2: axisY}, svg);

    // Ticks at round decimal steps; labels thinned so they never collide.
    const spacing = Number(`1e${Math.ceil(Math.log10(width * 0.999999))}`) / 10;
    const decimals = tickDecimals(spacing * 10);
    const pxPerTick = spacing / width * span;
    const labelPx = (decimals + 2) * 7.2 + 10;
    const every = [1, 2, 5, 10, 20].find(m => m * pxPerTick >= labelPx) || 50;
    const count = Math.floor(width * 1.02 / spacing);
    for (let k = 0; k <= count; k++) {
      const x = X(k * spacing);
      if (x > W - 2) break;
      svgEl('line', {class: 'z-tick', x1: x, x2: x, y1: axisY, y2: axisY + (k % every === 0 ? 7 : 4)}, svg);
      if (k > 0 && k % every === 0 && x < W - 20) {
        svgEl('text', {class: 'z-tick-label', x, y: axisY + 21, 'text-anchor': 'middle'}, svg, (1 + k * spacing).toFixed(decimals));
      }
    }

    // Target 1.
    svgEl('line', {class: 'z-target', x1, x2: x1, y1: 44, y2: axisY + 8}, svg);
    svgEl('text', {class: 'z-target-label', x: x1, y: axisY + 21, 'text-anchor': 'middle'}, svg, '1');
    svgEl('text', {class: 'z-target-label', x: x1, y: 37, 'text-anchor': 'middle'}, svg, 'target');

    // Earlier rounds still on screen.
    const dotX = X(gap);
    const used = [dotX];
    for (let r = round - 1; r >= 0; r--) {
      const x = X(ROUND_GAPS[r]);
      if (x > W - 4) continue;
      svgEl('circle', {class: 'z-trail', cx: x, cy: axisY, r: 4.5}, svg);
      if (used.every(u => Math.abs(u - x) > 16)) {
        svgEl('text', {class: 'z-trail-label', x, y: axisY - 11, 'text-anchor': 'middle'}, svg, String(r));
        used.push(x);
      }
    }

    // The gap, as a bracket above the line.
    const bracketY = 64;
    svgEl('line', {class: 'z-gap', x1, x2: dotX, y1: bracketY, y2: bracketY}, svg);
    svgEl('line', {class: 'z-gap', x1: dotX, x2: dotX, y1: bracketY - 5, y2: axisY - 9}, svg);
    svgEl('line', {class: 'z-gap', x1, x2: x1, y1: bracketY - 5, y2: bracketY + 5}, svg);
    const gapText = `gap ${formatGap(gap)}`;
    const textW = gapText.length * 7.4;
    const mid = Math.max(x1 + 8 + textW / 2, Math.min(right - textW / 2, (x1 + dotX) / 2));
    svgEl('text', {class: 'z-gap-label', x: mid, y: bracketY - 9, 'text-anchor': 'middle'}, svg, gapText);
    svgEl('circle', {class: 'z-dot', cx: dotX, cy: axisY, r: 8}, svg);
    svgEl('text', {class: 'z-zoom-label', x: right, y: 16, 'text-anchor': 'end'}, svg,
      `zoom ×${commas(Math.max(1, Math.round(10 / width)))}`);
  }

  function formatGap(gap) {
    return gap >= 1 ? gap.toFixed(3) : gap.toPrecision(3);
  }

  function updateReadout() {
    const gap = ROUND_GAPS[round];
    const kept = round === 0
      ? 'After the preliminary press: 2 in both boxes.'
      : `This round kept ${(gap / ROUND_GAPS[round - 1] * 100).toFixed(1)}% of the gap.`;
    readout.innerHTML = `<p class="zr-round">Round ${round}</p>`
      + `<p class="zr-item"><span>Saved answer</span><strong>${(1 + gap).toFixed(9)}</strong></p>`
      + `<p class="zr-item"><span>Gap above 1</span><strong>${gap.toFixed(9)}</strong></p>`
      + `<p class="zr-kept">${kept}</p>`;
    stepButtons.forEach((button, i) => {
      if (i === round) button.setAttribute('aria-current', 'step'); else button.removeAttribute('aria-current');
    });
    prev.disabled = round === 0;
    next.disabled = round === last;
  }

  function go(target) {
    target = Math.max(0, Math.min(last, target));
    const from = {...view};
    const to = {gap: ROUND_GAPS[target], width: zoomWidth(ROUND_GAPS[target])};
    round = target;
    updateReadout();
    cancelAnimationFrame(frame);
    if (reducedMotion()) { view = to; draw(to.gap, to.width); return; }
    const start = performance.now();
    const duration = 750;
    const lg = [Math.log(from.gap), Math.log(to.gap)];
    const lw = [Math.log(from.width), Math.log(to.width)];
    const step = now => {
      const t = Math.min(1, (now - start) / duration);
      const e = t < 0.5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2;
      view = {gap: Math.exp(lg[0] + (lg[1] - lg[0]) * e), width: Math.exp(lw[0] + (lw[1] - lw[0]) * e)};
      if (t >= 1) view = to;
      draw(view.gap, view.width);
      if (t < 1) frame = requestAnimationFrame(step);
    };
    frame = requestAnimationFrame(step);
  }

  function stop() {
    clearInterval(timer);
    timer = 0;
    play.setAttribute('aria-pressed', 'false');
    play.textContent = 'Play all rounds';
  }

  prev.addEventListener('click', () => { stop(); go(round - 1); });
  next.addEventListener('click', () => { stop(); go(round + 1); });
  play.addEventListener('click', () => {
    if (timer) { stop(); return; }
    if (round === last) go(0);
    play.setAttribute('aria-pressed', 'true');
    play.textContent = 'Pause';
    timer = setInterval(() => { if (round >= last) stop(); else go(round + 1); }, 1400);
  });
  onWidthChange(stage, () => draw(view.gap, view.width));
  updateReadout();
  draw(view.gap, view.width);
  // Play through once when the figure first comes into view, unless the reader prefers less motion.
  if ('IntersectionObserver' in window && !reducedMotion()) {
    const watcher = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) {
        watcher.disconnect();
        if (!timer && round === 0) setTimeout(() => { if (!timer && round === 0) play.click(); }, 600);
      }
    }, {threshold: 0.6});
    watcher.observe(figure);
  }
});

/* ---------- Pile: copied versus saved instructions, drawn to scale ---------- */
setup('pile-figure', figure => {
  const input = figure.querySelector('#pile-round');
  const output = figure.querySelector('#pile-round-out');
  const savedEl = figure.querySelector('#pile-saved');
  const copiedEl = figure.querySelector('#pile-copied');
  const ratioEl = figure.querySelector('#pile-ratio');
  const canvas = figure.querySelector('#pile-canvas');
  const ctx = canvas.getContext('2d');

  function render() {
    const n = Number(input.value);
    const copied = copiedCount(n);
    const saved = savedCount(n);
    output.textContent = String(n);
    savedEl.textContent = commas(saved);
    copiedEl.textContent = commas(copied);
    const ratio = copied / saved;
    ratioEl.textContent = n === 0
      ? 'Both begin with the one preliminary press.'
      : `Copying writes ${ratio < 10 ? ratio.toFixed(1) : commas(Math.round(ratio))} times as many instructions.`;
    canvas.setAttribute('aria-label', `After ${n} ${n === 1 ? 'round' : 'rounds'}: ${commas(saved)} saved instructions and ${commas(copied)} copied instructions, drawn as equal squares.`);
    draw(copied, saved);
  }

  function draw(copied, saved) {
    const styles = getComputedStyle(figure);
    const teal = styles.getPropertyValue('--ce-teal').trim();
    const rust = styles.getPropertyValue('--ce-rust').trim();
    const muted = styles.getPropertyValue('--muted').trim();
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    const W = canvas.clientWidth;
    const H = canvas.clientHeight;
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    const labelH = 20;
    const sep = 16;
    // One square size for every round: the largest that still fits round 6, so growth is drawn to scale.
    const most = [copiedCount(6), savedCount(6)];
    let p = 12;
    for (; p > 1; p--) {
      const cols = Math.floor(W / p);
      if ((Math.ceil(most[0] / cols) + Math.ceil(most[1] / cols)) * p + 2 * labelH + sep <= H) break;
    }
    const cols = Math.floor(W / p);
    const gap = p >= 7 ? 2 : p >= 3 ? 1 : 0;
    const size = p - gap;
    ctx.font = `12px ${getComputedStyle(document.body).fontFamily}`;
    ctx.textBaseline = 'top';
    ctx.fillStyle = muted;
    ctx.fillText(`Save answers: ${commas(saved)}`, 0, 0);
    let y = labelH;
    ctx.fillStyle = teal;
    for (let i = 0; i < saved; i++) ctx.fillRect((i % cols) * p, y + Math.floor(i / cols) * p, size, size);
    if (p <= 4) {
      ctx.fillStyle = teal;
      ctx.fillText(`← all ${saved} of them`, Math.min(saved, cols) * p + 8, y + p / 2 - 7);
    }
    y += Math.ceil(saved / cols) * p + sep;
    ctx.fillStyle = muted;
    ctx.fillText(`Copy it out: ${commas(copied)}`, 0, y);
    y += labelH;
    ctx.fillStyle = rust;
    if (gap === 0) {
      const fullRows = Math.floor(copied / cols);
      ctx.fillRect(0, y, cols * p, fullRows * p);
      ctx.fillRect(0, y + fullRows * p, (copied % cols) * p, p);
    } else {
      for (let i = 0; i < copied; i++) ctx.fillRect((i % cols) * p, y + Math.floor(i / cols) * p, size, size);
    }
  }

  input.addEventListener('input', render);
  onWidthChange(canvas, render);
  themeListeners.push(render);
  render();
});

/* ---------- Crossing: slide the starting number through the sign change ---------- */
setup('crossing-figure', figure => {
  const stage = figure.querySelector('.cross-stage');
  const input = figure.querySelector('#cross-c');
  const output = figure.querySelector('#cross-c-out');
  const readout = figure.querySelector('.cross-readout');
  const [xmin, xmax, ymin, ymax] = [0.8, 0.95, 0.9965, 1.009];
  const root = 0.8656409355716507; // 100-digit root, rounded; see proofs/positive-seeds/visual-data.json
  const samples = Array.from({length: 301}, (_, i) => {
    const c = xmin + (xmax - xmin) * i / 300;
    return [c, fourPress(c)];
  });
  const svg = svgEl('svg', {'aria-hidden': 'true'});
  stage.append(svg);
  let geometry = null;
  let marker = null;

  function draw() {
    const W = Math.max(280, Math.round(stage.getBoundingClientRect().width));
    const narrow = W < 520;
    const H = narrow ? 260 : 300;
    const m = {l: narrow ? 50 : 58, r: 12, t: 22, b: 42};
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
    svg.setAttribute('height', H);
    svg.replaceChildren();
    const X = c => m.l + (c - xmin) / (xmax - xmin) * (W - m.l - m.r);
    const Y = v => m.t + (ymax - v) / (ymax - ymin) * (H - m.t - m.b);
    geometry = {X, Y, m, W, H};
    const pts = list => list.map(([c, v]) => `${X(c).toFixed(1)},${Y(v).toFixed(1)}`).join(' ');
    svgEl('rect', {class: 'x-band', x: X(0.85), y: m.t, width: X(0.9) - X(0.85), height: H - m.t - m.b}, svg);
    svgEl('text', {class: 'x-region', x: (X(0.85) + X(0.9)) / 2, y: m.t - 7, 'text-anchor': 'middle'}, svg, 'sign changes in here');
    for (const v of [0.998, 1, 1.002, 1.004, 1.006, 1.008]) {
      svgEl('line', {class: 'x-grid', x1: m.l, x2: W - m.r, y1: Y(v), y2: Y(v)}, svg);
      svgEl('text', {class: 'x-tick-label', x: m.l - 7, y: Y(v) + 4, 'text-anchor': 'end'}, svg, v.toFixed(3));
    }
    const above = samples.filter(([c]) => c <= root);
    const below = samples.filter(([c]) => c >= root);
    svgEl('polygon', {class: 'x-above', points: `${X(xmin)},${Y(1)} ${pts(above)} ${X(root)},${Y(1)}`}, svg);
    svgEl('polygon', {class: 'x-below', points: `${X(root)},${Y(1)} ${pts(below)} ${X(xmax)},${Y(1)}`}, svg);
    svgEl('line', {class: 'x-target', x1: m.l, x2: W - m.r, y1: Y(1), y2: Y(1)}, svg);
    svgEl('polyline', {class: 'x-curve', points: pts(samples)}, svg);
    svgEl('text', {class: 'x-region', x: X(0.803), y: Y(1.0005), 'text-anchor': 'start'}, svg, narrow ? 'above 1' : 'answer above 1');
    svgEl('text', {class: 'x-region', x: X(0.947), y: Y(0.9985), 'text-anchor': 'end'}, svg, narrow ? 'below 1' : 'answer below 1');
    svgEl('line', {class: 'x-axis', x1: m.l, x2: W - m.r, y1: H - m.b, y2: H - m.b}, svg);
    for (const c of [0.8, 0.85, 0.9, 0.95]) {
      svgEl('line', {class: 'x-axis', x1: X(c), x2: X(c), y1: H - m.b, y2: H - m.b + 5}, svg);
      svgEl('text', {class: 'x-tick-label', x: X(c), y: H - m.b + 18, 'text-anchor': c === 0.8 ? 'start' : c === 0.95 ? 'end' : 'middle'}, svg, c.toFixed(2));
    }
    svgEl('text', {class: 'x-axis-title', x: (m.l + W - m.r) / 2, y: H - 4, 'text-anchor': 'middle'}, svg, 'starting number');
    marker = {
      guide: svgEl('line', {class: 'x-guide'}, svg),
      dot: svgEl('circle', {class: 'x-marker', r: 7}, svg),
    };
    update();
  }

  function update() {
    const c = Number(input.value);
    const v = fourPress(c);
    output.textContent = c.toFixed(4);
    if (geometry && marker) {
      const {X, Y, H, m} = geometry;
      const y = Y(Math.max(ymin, Math.min(ymax, v)));
      marker.guide.setAttribute('x1', X(c)); marker.guide.setAttribute('x2', X(c));
      marker.guide.setAttribute('y1', y); marker.guide.setAttribute('y2', H - m.b);
      marker.dot.setAttribute('cx', X(c)); marker.dot.setAttribute('cy', y);
    }
    const d = v - 1;
    const start = `Starting at <strong>${c.toFixed(4)}</strong>, four presses give <strong>${v.toFixed(6)}</strong>`;
    if (Math.abs(d) < 5e-7) {
      readout.innerHTML = `${start}. The rounded display reads 1. This does not establish exact equality.`;
    } else {
      const side = d > 0 ? '<span class="is-above">above 1</span>' : '<span class="is-below">below 1</span>';
      const near = Math.abs(d) < 1e-5 ? ' Very close: the answer is above 1 at 0.8656 and below 1 at 0.8657, so the exact crossing lies between them.' : '';
      readout.innerHTML = `${start}: ${side} by ${Math.abs(d).toFixed(6)}.${near}`;
    }
  }

  function fromPointer(event) {
    if (!geometry) return;
    const box = svg.getBoundingClientRect();
    const x = (event.clientX - box.left) * (geometry.W / box.width);
    const c = xmin + (x - geometry.m.l) / (geometry.W - geometry.m.l - geometry.m.r) * (xmax - xmin);
    input.value = String(Math.max(xmin, Math.min(xmax, Math.round(c * 1e4) / 1e4)));
    update();
  }
  svg.addEventListener('pointerdown', event => { svg.setPointerCapture(event.pointerId); fromPointer(event); });
  svg.addEventListener('pointermove', event => { if (svg.hasPointerCapture(event.pointerId)) fromPointer(event); });
  input.addEventListener('input', update);
  onWidthChange(stage, draw);
  draw();
});

/* ---------- AND puzzle: every move keeps an even number of ones ---------- */
setup('parity-lab-figure', figure => {
  const shelf = figure.querySelector('.lab-shelf');
  const status = figure.querySelector('.lab-status');
  const notButton = figure.querySelector('[data-lab="not"]');
  const xorButton = figure.querySelector('[data-lab="xor"]');
  const START = [['0011', 'first input'], ['0101', 'second input'], ['0000', 'constant 0'], ['1111', 'constant 1']];
  const reachable = parityClosure().size;
  let items = [];
  let selected = [];
  let fresh = -1;

  const patternEl = bits => {
    const span = document.createElement('span');
    span.className = 'pattern';
    span.setAttribute('aria-hidden', 'true');
    for (const digit of bits) {
      const cell = document.createElement('i');
      if (digit === '1') cell.className = 'on';
      span.append(cell);
    }
    return span;
  };
  const countText = bits => { const k = ones(bits); return `${k} ${k === 1 ? 'one' : 'ones'} · ${k % 2 ? 'odd' : 'even'}`; };
  const goal = figure.querySelector('[data-goal]');
  const goalCode = document.createElement('code');
  goalCode.textContent = '0001';
  goal.append(patternEl('0001'), goalCode);

  function render() {
    shelf.replaceChildren();
    items.forEach((item, i) => {
      const li = document.createElement('li');
      if (i === fresh) li.classList.add('is-new');
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'lab-item';
      button.dataset.index = String(i);
      button.setAttribute('aria-pressed', String(selected.includes(i)));
      button.setAttribute('aria-label', `${item.bits}: ${countText(item.bits)}; ${item.label}`);
      const bits = document.createElement('span'); bits.className = 'lab-bits'; bits.textContent = item.bits;
      const count = document.createElement('span'); count.className = 'lab-count'; count.textContent = countText(item.bits);
      const name = document.createElement('span'); name.className = 'lab-name'; name.textContent = item.label;
      button.append(patternEl(item.bits), bits, count, name);
      li.append(button);
      shelf.append(li);
    });
    notButton.disabled = selected.length !== 1;
    xorButton.disabled = selected.length !== 2;
  }

  function say(text, done = false) {
    status.textContent = text;
    status.classList.toggle('is-done', done);
  }

  function add(bits, label, message) {
    selected = [];
    if (items.some(item => item.bits === bits)) {
      fresh = -1; render();
      say(`${message} You already have ${bits}.`, items.length === reachable);
      return;
    }
    items.push({bits, label});
    fresh = items.length - 1;
    render();
    if (items.length === reachable) {
      say(`${message} That makes ${reachable} patterns, and any NOT or XOR of them gives one you already have. They are exactly the patterns with an even number of ones. AND, with one 1, is not among them, so no recipe with these tools can make it.`, true);
    } else {
      say(`${message} New pattern added: ${items.length} so far.`);
    }
  }

  shelf.addEventListener('click', event => {
    const button = event.target.closest('.lab-item');
    if (!button) return;
    const i = Number(button.dataset.index);
    if (selected.includes(i)) selected = selected.filter(j => j !== i);
    else { selected.push(i); if (selected.length > 2) selected.shift(); }
    fresh = -1;
    render();
    shelf.querySelector(`[data-index="${i}"]`).focus();
  });
  notButton.addEventListener('click', () => {
    const p = items[selected[0]].bits;
    const r = notPattern(p);
    add(r, `NOT ${p}`, `NOT ${p} = ${r}. Flipping all four positions turns ${ones(p)} ${ones(p) === 1 ? 'one' : 'ones'} into 4 − ${ones(p)} = ${ones(r)}. Still even.`);
  });
  xorButton.addEventListener('click', () => {
    const [p, q] = selected.map(i => items[i].bits);
    const r = xorPattern(p, q);
    const both = [...p].filter((digit, i) => digit === '1' && q[i] === '1').length;
    const how = both
      ? `${both === 1 ? 'One position had' : `${both} positions had`} a 1 in both, so ${2 * both} ones cancelled: ${ones(p)} + ${ones(q)} − ${2 * both} = ${ones(r)}.`
      : `No position had a 1 in both, so nothing cancelled: ${ones(p)} + ${ones(q)} = ${ones(r)}.`;
    add(r, `${p} XOR ${q}`, `${p} XOR ${q} = ${r}. ${how} Still even.`);
  });
  figure.querySelector('[data-lab="reset"]').addEventListener('click', reset);

  function reset() {
    items = START.map(([bits, label]) => ({bits, label}));
    selected = [];
    fresh = -1;
    render();
    say('Select one pattern for NOT, or two for XOR.');
  }
  reset();
});

/* ---------- Side rail: where am I in the eight questions? ---------- */
(function rail() {
  const map = document.querySelector('.essay-map');
  const parts = [...document.querySelectorAll('.essay-part')];
  const notes = document.querySelector('.essay-notes');
  if (!map || !parts.length) return;
  const nav = document.createElement('nav');
  nav.className = 'essay-rail';
  nav.setAttribute('aria-hidden', 'true');
  const title = document.createElement('p');
  title.textContent = 'In this essay';
  const list = document.createElement('ol');
  const links = [...map.querySelectorAll('a')].map(source => {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = source.getAttribute('href');
    a.tabIndex = -1;
    const n = document.createElement('span'); n.textContent = source.querySelector('.map-n').textContent;
    const q = document.createElement('span'); q.textContent = source.querySelector('.map-q').textContent;
    a.append(n, q);
    li.append(a);
    list.append(li);
    return a;
  });
  nav.append(title, list);
  document.body.append(nav);
  let queued = false;
  const update = () => {
    queued = false;
    const line = innerHeight * 0.35;
    let current = -1;
    parts.forEach((part, i) => { if (part.getBoundingClientRect().top <= line) current = i; });
    links.forEach((a, i) => a.classList.toggle('is-current', i === current));
    const pastMap = map.getBoundingClientRect().bottom < 0;
    const beforeNotes = !notes || notes.getBoundingClientRect().top > innerHeight * 0.6;
    nav.classList.toggle('is-visible', pastMap && beforeNotes);
  };
  const schedule = () => { if (!queued) { queued = true; requestAnimationFrame(update); } };
  addEventListener('scroll', schedule, {passive: true});
  addEventListener('resize', schedule);
  update();
})();
