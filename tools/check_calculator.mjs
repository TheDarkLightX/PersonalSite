import assert from 'node:assert/strict';
import {evaluatePress, initialNotebook, appendPress} from '../assets/js/calculator-core.mjs';
const initial=initialNotebook();
const first=appendPress(initial,0,0);
assert.ok(Math.abs(first.value-6.695908918370705)<1e-14);
assert.equal(initial.length,1); // Reuse does not consume or mutate the source notebook.
assert.equal(first.notebook.length,2);
const second=appendPress(first.notebook,0,1);
assert.ok(Math.abs(second.value-(Math.exp(2)-Math.log(first.value)))<1e-14);
assert.deepEqual(second.notebook[2],{value:second.value,left:0,right:1});
assert.notEqual(second.value,appendPress(first.notebook,1,0).value); // Operand order matters.
assert.ok(appendPress(initial,1,0).error); // A number not yet made cannot be introduced.
assert.ok(evaluatePress(2,0).error);
assert.ok(evaluatePress(2,-1).error);
assert.ok(evaluatePress(1000,2).error);
assert.ok(evaluatePress(-1000,2).error);
assert.ok(evaluatePress(0,Math.E).error); // Rounded cancellation must not produce a false exact zero.
assert.equal(evaluatePress(0,1).roundedToOne,true);
assert.ok(evaluatePress(0,Math.exp(2)).value<0); // Negative outputs remain allowed on the left.
assert.equal(evaluatePress(-1,2).error,undefined);
assert.equal(initialNotebook()[0].value,2);
console.log('Calculator checks passed: saved references, reuse, operand order, domain, numerical limits, and exactness warning.');
