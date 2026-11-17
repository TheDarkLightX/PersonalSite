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

// Figure helpers: the four-press recipe, zoom levels, instruction counts, and the parity invariant.
import * as viz from '../assets/js/calculator-visuals-core.mjs';
const transformed = b => { const q = Math.exp(-Math.exp(b)), l = Math.log(b); return b - l + b * b * l * q / (1 - b * l * q); };
for (let c = 0.8; c <= 0.95; c += 0.005) assert.ok(Math.abs(viz.fourPress(c) - transformed(c)) < 1e-12);
assert.ok(viz.fourPress(0.85) > 1 && viz.fourPress(0.9) < 1); // The sign change behind the crossing figure.
assert.ok(Math.abs(viz.fourPress(0.8656409355716507) - 1) < 1e-12);
assert.ok(Number.isNaN(viz.fourPress(0)) && Number.isNaN(viz.fourPress(-1)));
let b = Math.exp(2) - Math.log(2);
viz.ROUND_GAPS.forEach((gap, n) => { assert.ok(Math.abs(b - 1 - gap) < 1e-12 * Math.max(1, gap / 1e-6)); assert.ok(gap > 0); b = transformed(b); });
assert.deepEqual(viz.ROUND_GAPS.map(viz.zoomWidth), [10, 10, 10, 10, 1, 0.1, 0.01, 0.001, 0.0001]);
viz.ROUND_GAPS.forEach(gap => { const w = viz.zoomWidth(gap); assert.ok(gap <= 0.9 * w && gap > 0.009 * w); });
assert.deepEqual([10, 1, 0.1, 0.0001].map(viz.tickDecimals), [0, 1, 2, 5]);
assert.deepEqual([0, 1, 2, 6, 8].map(viz.copiedCount), [1, 9, 49, 31249, 781249]);
assert.deepEqual([0, 1, 6, 8].map(viz.savedCount), [1, 5, 25, 33]);
const closure = viz.parityClosure();
assert.deepEqual([...closure].sort(), ['0000', '0011', '0101', '0110', '1001', '1010', '1100', '1111']);
assert.ok(!closure.has('0001') && [...closure].every(p => viz.ones(p) % 2 === 0));
assert.equal(viz.xorPattern('0011', '0101'), '0110');
assert.equal(viz.notPattern('0011'), '1100');
assert.equal(viz.expDigits(807.187499226), 351);
console.log('Figure checks passed: four-press recipe, round gaps, zoom levels, instruction counts, parity closure.');
