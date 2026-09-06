// Replay: node tools/check-maze-witness.cjs
const assert = require('node:assert/strict');
const maze = require('../assets/js/maze-witness-core.js');
assert.equal(maze.checkRoute(maze.routes.valid).accepted,true);
assert.equal(maze.checkRoute(maze.routes.detour).accepted,true);
assert.equal(maze.routes.detour.length-maze.routes.valid.length,2);
assert.equal(maze.checkRoute(maze.routes.wall).code,'blocked');
assert.equal(maze.checkRoute(maze.routes.wall).index,3);
assert.equal(maze.checkRoute([]).code,'empty');
assert.equal(maze.checkRoute([[1,1],[3,1]]).code,'move');
assert.equal(maze.checkRoute([[1,1],[2,2]]).accepted,false);
assert.equal(maze.checkRoute([[2,1],[3,1]]).code,'start');
assert.equal(maze.checkRoute([[1,1],[2,1]]).code,'goal');
assert.equal(maze.checkRoute([[1,1],[-1,1]]).code,'blocked');
assert.equal(maze.checkRoute([[1,1],[1.5,1]]).code,'coordinate');
assert.equal(maze.checkRoute(null).accepted,false);
// Revisiting a position is legal: acceptance is about validity, not optimality.
assert.equal(maze.checkRoute([[1,1],[2,1],...maze.routes.valid]).accepted,true);
const reached=maze.enumerateReachable();
assert.equal(reached.length,36);
assert.equal(new Set(reached.map(p=>p.join(','))).size,36);
// Independent coverage check against every walkable cell in this particular maze.
const expected=[];
maze.rows.forEach((row,y)=>[...row].forEach((cell,x)=>{if(cell!=='#') expected.push(`${x},${y}`);}));
assert.deepEqual(reached.map(p=>p.join(',')).sort(),expected.sort());
console.log('Maze witness checks passed: valid paths, invalid moves, boundaries, loops, and complete reachable-position coverage.');
