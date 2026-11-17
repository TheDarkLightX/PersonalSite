// Numerical preview only. The retained left/right references record each recipe.
export function evaluatePress(left, right) {
  if (!Number.isFinite(left) || !Number.isFinite(right)) return {error:'Choose two saved, finite answers.'};
  if (right <= 0) return {error:'The right input must be positive because the button takes its logarithm.'};
  const exponential = Math.exp(left);
  if (!Number.isFinite(exponential) || exponential === 0) return {error:'This calculation exceeds the preview’s numerical range. Its mathematical recipe may still be valid. Try another pair or reset.'};
  const logarithm = Math.log(right);
  const value = exponential - logarithm;
  if (!Number.isFinite(value) || Math.abs(value) <= 1e-10 * Math.max(exponential, Math.abs(logarithm))) return {error:'These nearly equal values cancel too closely for this preview to resolve reliably. No answer was saved. This does not prove the exact answer is zero.'};
  return {value, roundedToOne:value === 1};
}

export function initialNotebook() { return [{value:2, left:null, right:null}]; }

export function appendPress(notebook, leftId, rightId) {
  if (!Number.isInteger(leftId) || !Number.isInteger(rightId) || !notebook[leftId] || !notebook[rightId]) return {error:'Choose inputs from the notebook.'};
  if (notebook.length >= 25) return {error:'This preview holds 24 presses. Reset to explore another recipe; the mathematics has no such fixed limit.'};
  const answer=evaluatePress(notebook[leftId].value,notebook[rightId].value);
  if (answer.error) return answer;
  return {...answer, notebook:[...notebook,{value:answer.value,left:leftId,right:rightId}]};
}
