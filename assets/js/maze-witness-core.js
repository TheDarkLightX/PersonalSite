(function (root) {
  'use strict';
  const rows = Object.freeze([
    '#############',
    '#S..#.......#',
    '###.#.###.#.#',
    '#...#...#.#.#',
    '#.#####.#.#.#',
    '#.........#G#',
    '#############'
  ]);
  const start = Object.freeze([1, 1]);
  const goal = Object.freeze([11, 5]);
  const freezeRoute = path => Object.freeze(path.map(p => Object.freeze(p)));
  const valid = freezeRoute([[1,1],[2,1],[3,1],[3,2],[3,3],[2,3],[1,3],[1,4],[1,5],[2,5],[3,5],[4,5],[5,5],[6,5],[7,5],[7,4],[7,3],[6,3],[5,3],[5,2],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[11,1],[11,2],[11,3],[11,4],[11,5]]);
  const routes = Object.freeze({
    valid,
    detour: freezeRoute([[1,1],[2,1],...valid]),
    wall: freezeRoute([[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[11,1],[11,2],[11,3],[11,4],[11,5]])
  });
  const same = (a,b) => a[0] === b[0] && a[1] === b[1];
  const open = p => Array.isArray(p) && p.length === 2 && p.every(Number.isInteger) && p[1] >= 0 && p[1] < rows.length && p[0] >= 0 && p[0] < rows[0].length && rows[p[1]][p[0]] !== '#';

  function checkRoute(path) {
    const fail = (code,index,reason) => ({accepted:false,code,index,reason});
    if (!Array.isArray(path) || !path.length) return fail('empty',0,'No trajectory was supplied.');
    for (let i=0; i<path.length; i++) {
      const p = path[i];
      if (!Array.isArray(p) || p.length !== 2 || !p.every(Number.isInteger)) return fail('coordinate',i,'The trajectory contains an invalid coordinate.');
      if (!open(p)) return fail('blocked',i,`Proposed step ${i} enters a wall or leaves the finite maze.`);
      if (i===0 && !same(p,start)) return fail('start',i,'The trajectory does not begin at Start.');
      if (i>0 && Math.abs(p[0]-path[i-1][0])+Math.abs(p[1]-path[i-1][1])!==1) return fail('move',i,'The trajectory contains a jump or diagonal move.');
    }
    if (!same(path[path.length-1],goal)) return fail('goal',path.length-1,'The trajectory does not reach Goal.');
    return {accepted:true,code:'accepted',index:path.length-1,reason:`All ${path.length-1} moves are legal and the trajectory reaches Goal.`};
  }

  function enumerateReachable() {
    const queue = [start];
    const seen = new Set([start.join(',')]);
    for (let head=0; head<queue.length; head++) {
      const [x,y] = queue[head];
      for (const next of [[x+1,y],[x,y+1],[x-1,y],[x,y-1]]) {
        if (open(next) && !seen.has(next.join(','))) {
          seen.add(next.join(','));
          queue.push(next);
        }
      }
    }
    return queue;
  }
  const api = Object.freeze({rows,start,goal,routes,checkRoute,enumerateReachable});
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.MazeWitness = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
