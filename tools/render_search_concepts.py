#!/usr/bin/env python3
"""Render exact essay diagrams from explicit graphs; validate before writing.

Run from any directory: python3 tools/render_search_concepts.py
SVGs have no external dependencies. Checks are executable, not Lean proofs.
"""
from collections import deque
from html import escape
from pathlib import Path
import json
import random

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/essays'
BG, INK, MUTED = '#faf9f5', '#242b2b', '#58615e'
GREEN, AMBER, LIGHT = '#086451', '#965800', '#e4e7e1'


def edge(a, b):
    return tuple(sorted((a, b)))


def maze(w, h, seed):
    rng = random.Random(seed)
    cells = {(x, y) for y in range(h) for x in range(w)}
    edges, seen, stack = set(), {(0, 0)}, [(0, 0)]
    while stack:
        x, y = stack[-1]
        options = [(x+dx, y+dy) for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]
                   if (x+dx, y+dy) in cells - seen]
        if options:
            nxt = rng.choice(options)
            edges.add(edge(stack[-1], nxt))
            seen.add(nxt)
            stack.append(nxt)
        else:
            stack.pop()
    return cells, edges


def adjacency(cells, edges):
    adj = {c: [] for c in cells}
    for a, b in sorted(edges):
        assert abs(a[0]-b[0]) + abs(a[1]-b[1]) == 1
        adj[a].append(b)
        adj[b].append(a)
    return adj


def explore(adj, start):
    prev, queue = {start: None}, deque([start])
    while queue:
        v = queue.popleft()
        for n in adj[v]:
            if n not in prev:
                prev[n] = v
                queue.append(n)
    return prev


def route(prev, goal):
    result = []
    while goal is not None:
        result.append(goal)
        goal = prev[goal]
    return result[::-1]


def check_route(path, edges):
    assert path and all(edge(a, b) in edges for a, b in zip(path, path[1:]))


class SVG:
    def __init__(self, width, height, title, desc):
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
                      f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>',
                      f'<rect width="{width}" height="{height}" fill="{BG}"/>',
                      '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10Z" fill="#58615e"/></marker></defs>']

    def text(self, x, y, text, size=22, color=INK, weight=400, anchor='start'):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(text)}</text>')

    def line(self, x1, y1, x2, y2, color=INK, width=3, dash=None):
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')

    def path(self, d, color=MUTED, width=2.5, arrow=False):
        self.parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"' + (' marker-end="url(#arrow)"' if arrow else '') + '/>')

    def rect(self, x, y, w, h, fill=BG, stroke=LIGHT, radius=0):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

    def circle(self, x, y, r, fill, stroke=BG, sw=2):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def save(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('\n'.join(self.parts + ['</svg>']) + '\n')


def draw_maze(svg, w, h, edges, origin, size, trails=(), graph=False, fills=None,
              start=(0, 0), goal=None, cross=None, dot=None, junction=None):
    ox, oy = origin
    center = lambda p: (ox+(p[0]+.5)*size, oy+(p[1]+.5)*size)
    if fills:
        for c in fills:
            svg.rect(ox+c[0]*size+3, oy+c[1]*size+3, size-6, size-6, '#e2eee8', '#e2eee8')
    if graph:
        for a, b in sorted(edges):
            svg.line(*center(a), *center(b), color='#bbc3bd', width=4)
        for y in range(h):
            for x in range(w):
                svg.circle(*center((x, y)), 4, MUTED, MUTED)
    else:
        # Draw each wall once. An edge is present iff the separating wall is absent.
        svg.rect(ox, oy, w*size, h*size, 'none', INK)
        for y in range(h):
            for x in range(w):
                if x+1 < w and edge((x,y), (x+1,y)) not in edges:
                    svg.line(ox+(x+1)*size, oy+y*size, ox+(x+1)*size, oy+(y+1)*size)
                if y+1 < h and edge((x,y), (x,y+1)) not in edges:
                    svg.line(ox+x*size, oy+(y+1)*size, ox+(x+1)*size, oy+(y+1)*size)
    for path, color, dashed in trails:
        check_route(path, edges)
        points = ' '.join(f'{x:.2f},{y:.2f}' for x, y in map(center, path))
        svg.parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="{max(3,size*.075):.2f}" stroke-linejoin="round" stroke-linecap="round"' + (f' stroke-dasharray="{size*.08:.2f} {size*.13:.2f}"' if dashed else '') + '/>')
    if junction:
        svg.circle(*center(junction), size*.12, BG, INK, 2)
    if cross:
        cx, cy = center(cross)
        svg.circle(cx, cy, size*.19, BG, BG)
        for sign in [-1, 1]:
            svg.line(cx-size*.12, cy-sign*size*.12, cx+size*.12, cy+sign*size*.12, AMBER, 3.5)
    if dot:
        svg.circle(*center(dot), size*.11, GREEN)
    sx, sy = center(start)
    svg.circle(sx, sy, size*.21, INK)
    svg.text(sx, sy+size*.08, 'S', size*.24, BG, 700, 'middle')
    if goal is not None:
        gx, gy = center(goal)
        svg.rect(gx-size*.23, gy-size*.25, size*.46, size*.5, BG, BG)
        svg.line(gx-size*.12, gy+size*.2, gx-size*.12, gy-size*.21, INK, 2.5)
        svg.parts.append(f'<path d="M{gx-size*.12},{gy-size*.21} h{size*.36} l{-size*.07},{size*.12} l{size*.07},{size*.12} h{-size*.36} Z" fill="{GREEN}"/>')


cells, edges = maze(7, 5, 6)
adj = adjacency(cells, edges)
start, goal = (0, 0), (6, 4)
prev = explore(adj, start)
solution = route(prev, goal)
assert len(prev) == 35 and len(edges) == 34  # Connected tree: one simple route per endpoint.
fork = solution[8]
off = next(n for n in adj[fork] if n not in solution)
branch = [fork, off]
while len(adj[branch[-1]]) == 2:
    branch.append(next(n for n in adj[branch[-1]] if n != branch[-2]))
assert len(adj[branch[-1]]) == 1  # Mark only a fully explored corridor with a dead end.
check_route(solution, edges)
check_route(branch, edges)
assert set(branch[1:]).isdisjoint(solution)

title = 'Remember the branch. Keep the junction.'
desc = 'An exact 7 by 5 maze. A solid teal route connects S to the flag through open passages. A dashed ochre branch ends at a cross. The two routes share one junction; rejecting that whole junction would discard the solution.'
for name, graph in [('maze-memory.svg', False), ('maze-candidates/03-junction-graph.svg', True)]:
    s = SVG(720, 680, title, desc)
    s.text(40, 48, title, 28, weight=700)
    s.text(40, 81, 'One checked failure does not close every route through a fork.', 18, MUTED)
    draw_maze(s, 7, 5, edges, (80, 115), 80,
              [(branch, AMBER, True), (solution, GREEN, False)], graph=graph,
              goal=goal, cross=branch[-1], junction=fork)
    s.line(42, 556, 83, 556, GREEN, 5)
    s.text(98, 563, 'Checked route from S to the flag', 22)
    s.line(42, 596, 83, 596, AMBER, 5, '5 9')
    s.text(98, 603, 'Explored dead-end branch; × records its limit', 22)
    s.circle(62, 638, 8, BG, INK)
    s.text(98, 645, 'Shared junction stays open', 22)
    s.save(OUT / name)

s = SVG(720, 775, 'The same maze, before and after checking', desc)
s.text(40, 48, 'Carry the evidence into the next attempt', 27, weight=700)
for y, heading, trails in [(100, '1 / Record the failed branch', [(branch, AMBER, True)]),
                           (438, '2 / Keep the fork; check another route', [(branch, AMBER, True), (solution, GREEN, False)])]:
    s.text(40, y, heading, 23, weight=700)
    draw_maze(s, 7, 5, edges, (157, y+24), 58, trails, goal=goal,
              cross=branch[-1], junction=fork)
s.save(OUT / 'maze-candidates/02-before-after.svg')

# Three epistemically different stopping states, all derived from the same tiny tree.
small_cells, small_edges = maze(3, 3, 3)
small_adj = adjacency(small_cells, small_edges)
small_path = route(explore(small_adj, (0,0)), (2,2))
cut = edge(small_path[-2], small_path[-1])
blocked_edges = small_edges - {cut}
reachable = set(explore(adjacency(small_cells, blocked_edges), (0,0)))
assert (2,2) not in reachable
assert len(small_path) > 3
prefix = small_path[:3]
assert prefix[-1] != (2,2) and (2,2) in explore(small_adj, prefix[-1])

s = SVG(720, 744, 'Three reasons a search can end', 'Solved: a legal route reaches the flag. Exhausted: after closing one passage, every reachable cell is checked and the flag is outside that component. Paused: only a route prefix was explored when the budget expired; the goal is still reachable.')
s.text(36, 45, 'Three reasons a search can end', 29, weight=700)
rows = [
    (90, small_edges, [(small_path, GREEN, False)], None, None, 'SOLVED', 'A checked route reaches the flag.', ['Keep the route as evidence.', 'The task is complete.']),
    (304, blocked_edges, [], reachable, None, 'EXHAUSTED', 'Every reachable cell was checked.', ['The added wall disconnects the flag.', 'No route exists in this fixed maze.']),
    (518, small_edges, [(prefix, GREEN, False)], None, prefix[-1], 'PAUSED', 'The run used up its budget.', ['The frontier is still open.', 'Save it and ask whether to resume.'])]
for y, es, trails, fills, dot, heading, sub, lines in rows:
    draw_maze(s, 3, 3, es, (40, y), 52, trails, goal=(2,2), fills=fills, dot=dot)
    if heading == 'EXHAUSTED':
        a, b = cut
        mx, my = (a[0]+b[0]+1)/2, (a[1]+b[1]+1)/2
        if a[0] == b[0]:
            s.line(40+(mx-.5)*52, y+my*52, 40+(mx+.5)*52, y+my*52, AMBER, 5)
        else:
            s.line(40+mx*52, y+(my-.5)*52, 40+mx*52, y+(my+.5)*52, AMBER, 5)
    s.text(230, y+24, heading, 24, GREEN if heading == 'SOLVED' else INK, 700)
    s.text(230, y+67, sub, 22)
    for i, line in enumerate(lines):
        s.text(230, y+105+i*31, line, 21, MUTED)
    if y < 518:
        s.line(36, y+184, 684, y+184, LIGHT, 1.5)
s.text(40, 714, 'A timeout is evidence about the run, not proof about the maze.', 21, weight=700)
s.save(OUT / 'bounded-persistence.svg')

s = SVG(720, 562, 'The neurosymbolic loop', 'The model proposes a candidate. A symbolic checker returns accept, reject, or unresolved with evidence. All verdicts enter scoped memory, which informs the next proposal. Accept also produces a checked proof of the specified statement; it does not prove the specification matches human intent.')
s.text(40, 47, 'The neurosymbolic loop', 30, weight=700)
s.text(40, 82, 'The next proposal starts from the previous check.', 22, MUTED)
for x, y, title_, sub in [(50,135,'MODEL','Propose candidate pₜ'), (420,135,'CHECKER','Check candidate pₜ'),
                         (50,365,'MEMORY','Verdict + evidence'), (420,365,'CHECKED PROOF','Of that exact statement')]:
    s.rect(x, y, 250, 96, '#edf2ec' if title_ == 'CHECKED PROOF' else BG, '#84938b', 4)
    s.text(x+18, y+35, title_, 22, weight=700)
    s.text(x+18, y+69, sub, 18, MUTED)
s.path('M300 183 H417', arrow=True)
s.text(360, 166, 'pₜ', 24, anchor='middle')
s.path('M545 231 V360', arrow=True)
s.text(565, 312, 'accept', 20, GREEN)
s.circle(545, 270, 4, MUTED, MUTED)
s.path('M545 270 H351 V413 H305', arrow=True)
s.text(344, 299, 'all', 19, MUTED, anchor='end')
s.text(344, 326, 'verdicts', 19, MUTED, anchor='end')
s.path('M175 365 V236', arrow=True)
s.text(158, 296, 'next', 19, MUTED, anchor='end')
s.text(158, 323, 'context', 19, MUTED, anchor='end')
s.text(40, 510, 'Scope σ fixes the target, assumptions, checker, and versions.', 21)
s.text(40, 539, 'The operator still has to ask: is this the statement I meant?', 21, MUTED)
s.save(OUT / 'neurosymbolic-loop.svg')

report = {
    'method': 'Explicit undirected cell graphs; deterministic DFS construction and independent BFS reachability; routes checked against all open edges before rendering.',
    'formal_status': 'Executable Python assertions, not a Lean proof of SVG rendering.',
    'maze': {'width':7, 'height':5, 'seed':6, 'cells':len(cells), 'edges':len(edges),
             'start':start, 'goal':goal, 'solution':solution, 'dead_branch':branch,
             'checks':['Connected tree', 'Each trail traverses open orthogonal edges only', 'Dead branch terminates at a degree-one cell', 'Dead branch and solution share only the marked junction', 'Walls are precisely the missing cell edges']},
    'stopping_examples': {'base_edges': sorted(small_edges), 'blocked_edge':cut,
                          'blocked_reachable_cells':sorted(reachable), 'prefix':prefix,
                          'checks':['Complete route reaches flag', 'Flag absent from exhaustive reachable component after wall added', 'Budget-stop prefix has not reached flag although flag remains reachable']},
    'candidates':[
        {'path':'maze-memory.svg','concept':'Full overhead map','selected':True,'reason':'Largest corridors and clearest wall geometry; shows why the junction survives a valid branch rejection.'},
        {'path':'maze-candidates/02-before-after.svg','concept':'Before and after','selected':False,'reason':'Accurate temporal comparison, but repeats geometry and makes each maze smaller.'},
        {'path':'maze-candidates/03-junction-graph.svg','concept':'Graph of cell connections','selected':False,'reason':'Exact topology, but missing walls makes it less immediately recognizable as a maze.'}
    ]
}
(OUT / 'maze-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(f'Validated {len(cells)} cells, {len(edges)} passages, {len(solution)-1} solution steps, {len(branch)-1} dead-branch steps. Wrote three maze candidates and two concept diagrams.')
