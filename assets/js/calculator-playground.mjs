import {appendPress, evaluatePress, initialNotebook} from './calculator-core.mjs';
import {expDigits} from './calculator-visuals-core.mjs';

// The notebook: tap a box, tap a saved number, press. Each saved entry keeps references to its two inputs.
const root = document.getElementById('calc');
const figure = root && root.closest('.calculator-playground');
if (root) {
  try {
    initCalculator();
  } catch (error) {
    figure.classList.add('viz-failed');
    console.error(error);
  }
}

function initCalculator() {
  let notebook = initialNotebook();
  const slots = {left: 0, right: 0};
  let active = 'left';
  let lastAdded = -1;
  const tape = document.getElementById('calc-tape');
  const status = document.getElementById('calc-status');
  const pressButton = document.getElementById('calc-press');
  const slotButtons = [...root.querySelectorAll('.calc-slot')];
  const part = name => root.querySelector(`[data-part="${name}"]`);
  const display = n => Number(n.toPrecision(9)).toString();
  const short = n => Number(n.toPrecision(6)).toString();
  const name = i => (i === 0 ? 'Start' : `Answer ${i}`);
  const sideWord = side => (side === 'left' ? 'left' : 'right');

  function setPart(key, text, isError = false) {
    const node = part(key);
    node.textContent = text;
    node.parentElement.classList.toggle('is-error', isError);
  }

  function preview() {
    const a = notebook[slots.left].value;
    const b = notebook[slots.right].value;
    const grown = Math.exp(a);
    if (Number.isFinite(grown) && grown > 0) setPart('exp', `≈ ${short(grown)}`);
    else if (a > 0) setPart('exp', `a ${expDigits(a).toLocaleString('en-US')}-digit number: too big for this preview`, true);
    else setPart('exp', 'too small for this preview', true);
    if (b > 0) setPart('log', `≈ ${short(Math.log(b))}`);
    else setPart('log', 'not allowed: ln needs a positive number', true);
    const answer = evaluatePress(a, b);
    if (answer.error) setPart('result', 'no answer this time', true);
    else setPart('result', `≈ ${short(answer.value)}`);
  }

  function render() {
    for (const button of slotButtons) {
      const side = button.dataset.slot;
      const index = slots[side];
      button.setAttribute('aria-pressed', String(side === active));
      button.querySelector('.slot-value').textContent = index ? `≈ ${short(notebook[index].value)}` : '2';
      button.querySelector('.slot-src').textContent = name(index);
      button.setAttribute('aria-label', `${sideWord(side)} box: ${name(index)}${index ? `, approximately ${short(notebook[index].value)}` : ', 2'}${side === active ? '. Selected: tapping a saved number fills this box' : ''}`);
    }
    tape.replaceChildren();
    notebook.forEach((item, i) => {
      const li = document.createElement('li');
      if (i === lastAdded) li.classList.add('is-new');
      const chip = document.createElement('button');
      chip.type = 'button';
      chip.className = `nb-chip${i === 0 ? ' is-start' : ''}${i === slots.left || i === slots.right ? ' is-in-slot' : ''}`;
      chip.dataset.index = String(i);
      chip.setAttribute('aria-label', `Put ${name(i)}${i ? `, approximately ${display(item.value)},` : ', 2,'} in the ${sideWord(active)} box`);
      const label = document.createElement('span'); label.className = 'nb-name'; label.textContent = name(i);
      const value = document.createElement('span'); value.className = 'nb-value'; value.textContent = i ? `≈ ${display(item.value)}` : '2';
      const recipe = document.createElement('span'); recipe.className = 'nb-recipe';
      recipe.textContent = i ? `Left: ${name(item.left)} · Right: ${name(item.right)}` : 'The only number supplied at the start.';
      chip.append(label, value, recipe);
      li.append(chip);
      tape.append(li);
    });
    preview();
  }

  for (const button of slotButtons) {
    button.addEventListener('click', () => { active = button.dataset.slot; render(); button.focus(); });
  }
  tape.addEventListener('click', event => {
    const chip = event.target.closest('.nb-chip');
    if (!chip) return;
    const index = Number(chip.dataset.index);
    slots[active] = index;
    const filled = active;
    if (active === 'left') active = 'right';
    lastAdded = -1;
    render();
    status.dataset.kind = '';
    status.textContent = `${name(index)} is in the ${sideWord(filled)} box.`;
    const again = tape.querySelector(`[data-index="${index}"]`);
    if (again) again.focus();
  });
  pressButton.addEventListener('click', () => {
    const answer = appendPress(notebook, slots.left, slots.right);
    if (answer.error) { status.textContent = answer.error; status.dataset.kind = 'error'; return; }
    notebook = answer.notebook;
    lastAdded = notebook.length - 1;
    slots.right = lastAdded;
    active = 'left';
    render();
    status.dataset.kind = 'success';
    status.textContent = answer.roundedToOne
      ? 'The rounded display reads 1. This is not proof of exact equality. The recipe is saved for inspection.'
      : `${name(lastAdded)} saved: approximately ${display(answer.value)}. The right box now holds this answer; tap a saved number to change either box.`;
  });
  document.getElementById('calc-reset').addEventListener('click', () => {
    notebook = initialNotebook(); slots.left = 0; slots.right = 0; active = 'left'; lastAdded = -1;
    render();
    status.dataset.kind = '';
    status.textContent = 'Notebook reset. Start with 2 in both boxes.';
  });
  render();
}
