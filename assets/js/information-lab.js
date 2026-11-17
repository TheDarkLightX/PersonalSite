(function () {
  'use strict';
  const masks = [3, 5, 15];
  const names = ['A', 'B', 'C'];
  function solve(start) {
    if (!Number.isInteger(start) || start < 0 || start > 15) throw new RangeError('Four lights required');
    const count = start.toString(2).split('1').length - 1;
    const reachable = count % 2 === 1;
    if (!reachable) return { count, reachable, correction: null, buttons: null };
    const correction = start ^ 1;
    for (let choice = 0; choice < 8; choice++) {
      let effect = 0;
      const buttons = [];
      masks.forEach((mask, i) => { if (choice & (1 << i)) { effect ^= mask; buttons.push(names[i]); } });
      if (effect === correction) return { count, reachable, correction, buttons };
    }
    throw new Error('Missing reachable correction');
  }
  // Export the same pure function for the independent UI checks under Node.
  if (typeof module !== 'undefined' && module.exports) module.exports = { solve };
  if (typeof document === 'undefined') return;
  const lab = document.getElementById('light-lab');
  if (!lab) return;
  let state = 2;
  const reread = document.getElementById('reread');
  const instruction = document.getElementById('instruction');
  const apply = document.getElementById('apply-correction');
  function render(announce) {
    const result = solve(state);
    const ordinals = ['Fourth', 'Third', 'Second', 'First'];
    lab.querySelectorAll('[data-bit]').forEach(button => {
      const bit = Number(button.dataset.bit);
      const on = Boolean(state & (1 << bit));
      button.setAttribute('aria-pressed', String(on));
      button.setAttribute('aria-label', `${ordinals[bit]} light, ${on ? 'on' : 'off'}`);
      button.firstElementChild.textContent = on ? '1' : '0';
    });
    document.getElementById('can-reach').textContent = result.reachable ? 'YES' : 'NO';
    document.getElementById('parity-count').textContent = `${result.count} ${result.count === 1 ? 'light' : 'lights'} on; ${result.reachable ? 'odd' : 'even'}.`;
    instruction.textContent = !result.reachable ? 'No correction exists with these buttons.'
      : !reread.checked ? 'YES alone cannot choose a correction.'
      : result.buttons.length ? `Press ${result.buttons.join(' + ')}. The original pattern tells us which lights differ from the goal.`
      : 'Do nothing. The original pattern is already the goal.';
    apply.disabled = !reread.checked || !result.reachable || result.correction === 0;
    if (announce) document.getElementById('lab-announcement').textContent = `Pattern ${state.toString(2).padStart(4, '0')}. ${result.reachable ? 'Reachable.' : 'Unreachable.'} ${instruction.textContent}`;
  }
  lab.querySelectorAll('[data-bit]').forEach(b => b.addEventListener('click', () => { state ^= 1 << Number(b.dataset.bit); render(true); }));
  lab.querySelectorAll('[data-move]').forEach(b => b.addEventListener('click', () => { state ^= Number(b.dataset.move); render(true); }));
  lab.querySelectorAll('[data-start]').forEach(b => b.addEventListener('click', () => { state = Number(b.dataset.start); render(true); }));
  reread.addEventListener('change', () => render(true));
  apply.addEventListener('click', () => { const result = solve(state); if (reread.checked && result.reachable) state ^= result.correction; render(true); });
  render(false);
}());
