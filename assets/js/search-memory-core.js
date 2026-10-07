(function (root) {
  'use strict';
  const SIZE = 32;
  const GOAL = 23;
  const WORKERS = Object.freeze([1, 2, 4, 8]);
  function draw(seed) {
    let x = seed >>> 0;
    x ^= x << 13; x ^= x >>> 17; x ^= x << 5;
    return x >>> 0;
  }
  function create(seed = 42) {
    if (!Number.isInteger(seed) || seed < 0 || seed > 65535) throw new RangeError('Seed must be 0–65535.');
    const initial = seed || 0x9e3779b9;
    let rng = initial;
    const order = Array.from({length: SIZE}, (_, i) => i);
    for (let i = SIZE - 1; i > 0; i--) {
      rng = draw(rng);
      const j = Math.floor(rng / 4294967296 * (i + 1));
      [order[i], order[j]] = [order[j], order[i]];
    }
    return {order, rng: initial, rounds: 0, memory: lane(), repeated: lane()};
  }
  function lane() { return {attempts: [], visited: [], found: false, rounds: 0}; }
  function advance(previous, proposed) {
    if (previous.found) return previous;
    const attempts = [...previous.attempts, ...proposed];
    return {attempts, visited: [...new Set(attempts)], found: proposed.includes(GOAL), rounds: previous.rounds + 1};
  }
  function step(state, workers) {
    if (!WORKERS.includes(workers)) throw new RangeError('Use 1, 2, 4 or 8 workers.');
    if (state.memory.found && state.repeated.found) return state;
    let rng = state.rng;
    const proposed = [];
    if (!state.repeated.found) {
      for (let i = 0; i < workers; i++) {
        rng = draw(rng);
        proposed.push(Math.floor(rng / 4294967296 * SIZE));
      }
    }
    return {
      ...state, rng, rounds: state.rounds + 1,
      memory: advance(state.memory, state.order.slice(state.memory.attempts.length, state.memory.attempts.length + workers)),
      repeated: advance(state.repeated, proposed)
    };
  }
  function rounds(n, k) {
    if (!Number.isSafeInteger(n) || n < 0 || !WORKERS.includes(k)) throw new RangeError('Invalid workload or worker count.');
    return Math.ceil(n / k);
  }
  const api = Object.freeze({SIZE, GOAL, WORKERS, create, step, rounds});
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.SearchMemory = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
