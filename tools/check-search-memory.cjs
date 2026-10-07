'use strict';
const assert = require('node:assert/strict');
const core = require('../assets/js/search-memory-core.js');

// Cover every public seed and worker count: permutation, no mutation, complete
// bounded coverage, no duplicate allocations, and the goal is really checked.
let campaigns = 0;
for (let seed = 0; seed <= 65535; seed++) {
  const initial = core.create(seed);
  assert.equal(new Set(initial.order).size, core.SIZE);
  assert.ok(initial.order.every(x => Number.isInteger(x) && x >= 0 && x < core.SIZE));
  for (const workers of core.WORKERS) {
    let state = initial;
    for (let r = 0; r < core.rounds(core.SIZE, workers) && !state.memory.found; r++) {
      const before = JSON.stringify(state);
      const next = core.step(state, workers);
      assert.equal(JSON.stringify(state), before);
      assert.equal(next.memory.attempts.length - state.memory.attempts.length, workers);
      state = next;
    }
    assert.equal(state.memory.found, true);
    assert.ok(state.memory.attempts.includes(core.GOAL));
    assert.equal(new Set(state.memory.attempts).size, state.memory.attempts.length);
    assert.ok(state.memory.rounds <= core.rounds(core.SIZE, workers));
    assert.equal(state.repeated.found, state.repeated.attempts.includes(core.GOAL));
    campaigns++;
  }
}
for (const k of core.WORKERS) {
  assert.equal(core.rounds(0, k), 0);
  for (let n = 0; n <= 129; n++) {
    const r = core.rounds(n, k);
    assert.ok(r * k >= n);
    if (r > 0) assert.ok((r - 1) * k < n);
  }
}
// No guarantee that coordinated search wins each run: retain this countercase.
let lucky = core.create(42);
while (!lucky.memory.found || !lucky.repeated.found) lucky = core.step(lucky, 4);
assert.ok(lucky.repeated.rounds < lucky.memory.rounds);
const done = JSON.stringify(lucky);
assert.equal(JSON.stringify(core.step(lucky, 4)), done);

// Assumption countercontrols, independent of the UI's scheduler.
const universe = Array.from({length: core.SIZE}, (_, i) => i);
const good = x => x === core.GOAL;
const sound = universe.filter(x => x !== 2 && x !== 9);
assert.deepEqual(sound.filter(good), universe.filter(good));
const unsound = universe.filter(x => x !== core.GOAL);
assert.equal(unsound.some(good), false);
assert.equal(Array(10000).fill(0).some(good), false);
for (const bad of [-1, 0.5, 65536, NaN, Infinity]) assert.throws(() => core.create(bad), RangeError);
for (const bad of [0, -1, 3, 1.5, NaN]) assert.throws(() => core.step(core.create(), bad), RangeError);
console.log(`PASS: ${campaigns} finite campaigns; coverage, unique assignments, immutability, edge cases, and assumption countercontrols.`);
