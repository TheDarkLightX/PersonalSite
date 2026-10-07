(function () {
  'use strict';
  const core = window.SearchMemory;
  const lab = document.querySelector('[data-search-lab]');
  if (!lab || !core) return;
  const workers = lab.querySelector('[data-workers]');
  const seed = lab.querySelector('[data-seed]');
  const run = lab.querySelector('[data-run]');
  const step = lab.querySelector('[data-step]');
  const status = lab.querySelector('[data-status]');
  let state = core.create();
  let timer = null;
  const svgNS = 'http://www.w3.org/2000/svg';
  function element(tag, attrs) {
    const el = document.createElementNS(svgNS, tag);
    Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, value));
    return el;
  }
  function tree(svg, lane) {
    svg.replaceChildren();
    const visited = new Set(lane.visited);
    const covers = (d, i, leaf) => Math.floor(leaf / (2 ** (5 - d))) === i;
    for (let depth = 0; depth <= 5; depth++) {
      const count = 2 ** depth;
      for (let i = 0; i < count; i++) {
        const x = 8 + (i + 0.5) * 344 / count;
        const y = 20 + depth * 33;
        const found = lane.found && covers(depth, i, core.GOAL);
        const seen = [...visited].some(leaf => covers(depth, i, leaf));
        const kind = found ? 'found' : seen ? 'visited' : 'unseen';
        if (depth) {
          const parentX = 8 + (Math.floor(i / 2) + 0.5) * 344 / (count / 2);
          svg.append(element('line', {x1: parentX, y1: y - 33, x2: x, y2: y, class: kind}));
        }
        const node = element('circle', {cx: x, cy: y, r: depth === 5 ? 3.5 : 2.5, class: kind});
        const title = element('title', {});
        title.textContent = depth === 5 ? `Route ${i + 1}: ${found ? 'goal found' : seen ? 'checked' : 'unexplored'}` : `Junction at depth ${depth}`;
        node.append(title); svg.append(node);
        if (depth === 0 || (depth === 5 && found)) {
          const label = element('text', {x, y: depth === 0 ? y - 8 : y + 17, 'text-anchor': 'middle'});
          label.textContent = depth === 0 ? 'START' : 'GOAL'; svg.append(label);
        }
      }
    }
  }
  function render() {
    for (const name of ['memory', 'repeated']) {
      const lane = state[name];
      const panel = lab.querySelector(`[data-lane="${name}"]`);
      tree(panel.querySelector('svg'), lane);
      panel.querySelector('[data-count]').textContent = `${lane.attempts.length} checks · ${lane.visited.length} distinct · ${lane.attempts.length - lane.visited.length} repeats`;
      panel.querySelector('[data-result]').textContent = lane.found ? `Goal found in ${lane.rounds} rounds` : `${lane.rounds} rounds completed`;
    }
    const done = state.memory.found && state.repeated.found;
    const exhausted = state.rounds >= 200;
    const invalid = !seed.value || !seed.validity.valid;
    step.disabled = done || exhausted || invalid || timer !== null;
    run.disabled = done || exhausted || invalid;
    run.textContent = timer === null ? 'Run comparison' : 'Pause';
    lab.querySelector('[data-bound]').textContent = core.rounds(core.SIZE, Number(workers.value));
    status.textContent = invalid ? 'Enter a whole seed from 0 to 65535 to continue.' : done ? 'Both searches found the goal. Reset or change the seed to compare another run.' : exhausted ? 'The 200-round demo budget is exhausted. This is not proof that a route has no solution.' : `Round ${state.rounds}. Each active search can check ${workers.value} routes per round.`;
  }
  function stop() { if (timer !== null) clearInterval(timer); timer = null; }
  function tick() {
    state = core.step(state, Number(workers.value));
    if ((state.memory.found && state.repeated.found) || state.rounds >= 200) stop();
    render();
  }
  function reset() {
    stop();
    const value = Number(seed.value);
    if (!seed.value || !Number.isInteger(value) || value < 0 || value > 65535) {
      seed.setCustomValidity('Enter a whole number from 0 to 65535.');
      seed.reportValidity(); render(); return;
    }
    seed.setCustomValidity(''); state = core.create(value); render();
  }
  step.addEventListener('click', tick);
  run.addEventListener('click', () => {
    if (timer !== null) { stop(); render(); return; }
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
      while (!(state.memory.found && state.repeated.found) && state.rounds < 200) state = core.step(state, Number(workers.value));
      render();
    } else { timer = setInterval(tick, 450); render(); }
  });
  lab.querySelector('[data-reset]').addEventListener('click', reset);
  workers.addEventListener('change', reset);
  seed.addEventListener('input', () => { stop(); seed.setCustomValidity(''); render(); });
  seed.addEventListener('change', reset);
  document.addEventListener('visibilitychange', () => { if (document.hidden) { stop(); render(); } });
  render();
  lab.querySelectorAll('button, select, input').forEach(el => { if (!el.matches('[data-step], [data-run]')) el.disabled = false; });
  lab.querySelector('[data-needs-js]').hidden = true;
})();
