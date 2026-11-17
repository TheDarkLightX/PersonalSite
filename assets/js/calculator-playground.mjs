import {appendPress, initialNotebook} from './calculator-core.mjs';

const form=document.getElementById('calculator-form');
if (form) {
  let notebook=initialNotebook();
  const left=document.getElementById('calc-left');
  const right=document.getElementById('calc-right');
  const tape=document.getElementById('calc-tape');
  const status=document.getElementById('calc-status');
  const display=n=>Number(n.toPrecision(9)).toString();
  const name=i=>i===0?'Start':`Answer ${i}`;
  function render() {
    const l=left.value||'0', r=right.value||'0';
    left.replaceChildren();right.replaceChildren();tape.replaceChildren();
    notebook.forEach((item,i)=>{
      const label=`${name(i)}: ${i?'≈ ':''}${display(item.value)}`;
      for (const select of [left,right]) { const o=document.createElement('option');o.value=String(i);o.textContent=label;select.append(o); }
      const li=document.createElement('li');
      const value=document.createElement('strong');value.textContent=label;li.append(value);
      const recipe=document.createElement('span');
      recipe.textContent=i?`Left: ${name(item.left)} · Right: ${name(item.right)}`:'The only number supplied at the start.';
      li.append(recipe);tape.append(li);
    });
    left.value=l;right.value=r;
  }
  form.addEventListener('submit',event=>{
    event.preventDefault();
    const answer=appendPress(notebook,Number(left.value),Number(right.value));
    if (answer.error) {status.textContent=answer.error;status.dataset.kind='error';return;}
    notebook=answer.notebook;render();
    right.value=String(notebook.length-1);
    status.dataset.kind='success';
    status.textContent=answer.roundedToOne?'The rounded display reads 1. This is not proof of exact equality. The recipe is saved for inspection.':`${name(notebook.length-1)} saved: approximately ${display(answer.value)}. The next right input is set to this answer; you can change either input.`;
  });
  document.getElementById('calc-reset').addEventListener('click',()=>{
    notebook=initialNotebook();left.value='0';right.value='0';render();
    status.dataset.kind='';status.textContent='Notebook reset. Start with 2 in both boxes.';
  });
  render();
  form.hidden=false;
  document.getElementById('calculator-fallback').hidden=true;
}
