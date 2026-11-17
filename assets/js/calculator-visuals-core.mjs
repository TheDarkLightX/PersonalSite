// Pure helpers for the essay's figures. Browser arithmetic is rounded: these are previews, not proofs.

// One press of the button. The right input must be positive.
export const press = (a, b) => (b > 0 ? Math.exp(a) - Math.log(b) : NaN);

// The four-press recipe applied directly to c: U=F(c,c), V=F(U,c), W=F(c,V), Next=F(W,c).
export function fourPress(c) {
  if (!(c > 0)) return NaN;
  const u = press(c, c);
  const v = press(u, c);
  const w = press(c, v);
  return press(w, c);
}

// Gap above 1 after each round, starting from 2 (round 0 is the preliminary press F(2, 2)).
// Copied from the 100-digit values in proofs/positive-seeds/visual-data.json.
export const ROUND_GAPS = [5.695908918370705, 3.7944121876699053, 2.2269610754476603, 1.0554202247371207,
  0.3361752662466457, 0.05798775095970137, 0.005170726703754054, 0.00035248066824050206, 2.331216186518522e-05];

// Width of the visible stretch of number line: the smallest power of ten that holds the gap with room to spare.
export function zoomWidth(gap) {
  return Number(`1e${Math.ceil(Math.log10(gap / 0.9))}`); // parse the decimal power consistently for tick formatting
}

// Decimal places needed to label ticks one tenth of the width apart.
export function tickDecimals(width) {
  return Math.max(0, -Math.round(Math.log10(width / 10)));
}

// Written instructions after n rounds, counting the preliminary press.
export const copiedCount = n => 2 * 5 ** n - 1;   // copy every earlier recipe: m(n+1) = 5 m(n) + 4
export const savedCount = n => 1 + 4 * n;         // store each answer once: four new instructions per round

// Four-answer patterns for the XOR/NOT example, written as four-character strings of 0 and 1.
export const ones = p => [...p].filter(d => d === '1').length;
export const notPattern = p => [...p].map(d => (d === '1' ? '0' : '1')).join('');
export const xorPattern = (p, q) => [...p].map((d, i) => (d === q[i] ? '0' : '1')).join('');
export const PARITY_START = ['0011', '0101', '0000', '1111'];

export function parityClosure(start = PARITY_START) {
  const made = new Set(start);
  let grew = true;
  while (grew) {
    grew = false;
    for (const p of [...made]) {
      for (const q of [...made, null]) {
        const r = q === null ? notPattern(p) : xorPattern(p, q);
        if (!made.has(r)) { made.add(r); grew = true; }
      }
    }
  }
  return made;
}

// Approximate number of decimal digits in e^a, for explaining numbers too large to display.
export const expDigits = a => Math.floor(a * Math.LOG10E) + 1;
