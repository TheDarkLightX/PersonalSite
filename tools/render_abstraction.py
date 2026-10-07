#!/usr/bin/env python3
"""Exact diagrams for Abstraction Is Compression; no generative geometry."""
from html import escape
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'assets/essays'
BG, INK, MUTED, GREEN, BAD = '#faf9f5', '#242b2b', '#58615e', '#086451', '#93422c'


class Figure:
    def __init__(self, height, title, desc):
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{height}" viewBox="0 0 720 {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>',
            f'<rect width="720" height="{height}" fill="{BG}"/>',
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10Z" fill="context-stroke"/></marker></defs>']

    def text(self, x, y, text, size=22, color=INK, weight=400, anchor='start'):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(text)}</text>')

    def path(self, d, color=MUTED, width=2.5, arrow=True):
        self.parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"' + (' marker-end="url(#arrow)"' if arrow else '') + '/>')

    def circle(self, x, y, r, fill=BG, stroke=INK, width=2):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')

    def rect(self, x, y, w, h, fill, stroke=BG):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

    def save(self, name):
        (OUT/name).write_text('\n'.join(self.parts+['</svg>'])+'\n')


def reachable(edges, start):
    seen, todo = {start}, [start]
    while todo:
        here = todo.pop()
        for src, dst in edges:
            if src == here and dst not in seen:
                seen.add(dst)
                todo.append(dst)
    return seen


concrete = [('start','a'), ('start','b'), ('a','c'), ('b','d'), ('c','bad')]
alpha = {'start':'start','a':'work','b':'work','c':'work','d':'work','bad':'bad'}
abstract = sorted({(alpha[x],alpha[y]) for x,y in concrete})
assert abstract == [('start','work'),('work','bad'),('work','work')]
assert 'bad' in reachable(concrete,'start') and 'bad' in reachable(abstract,'start')
assert all((alpha[x],alpha[y]) in abstract for x,y in concrete)
assert 'bad' not in reachable([e for e in abstract if e != ('work','bad')],'start')

f = Figure(560, 'Shrink the map. Keep the dangerous route.',
           'Six concrete states compress to three abstract states. Four private internal states map to Work. Every concrete step has an abstract step, including a Work self-loop; the route to Bad is preserved.')
f.text(36,45,'Shrink the map. Keep the dangerous route.',26,weight=700)
f.text(36,80,'Same question: can the forbidden state be reached?',21,MUTED)
f.text(36,118,'DETAILED / 6 states',17,MUTED,700)
positions={'start':(75,218),'a':(245,163),'b':(245,277),'c':(455,163),'d':(455,277),'bad':(640,218)}
for src,dst in concrete:
    x1,y1=positions[src];x2,y2=positions[dst]
    length=((x2-x1)**2+(y2-y1)**2)**.5
    ux,uy=(x2-x1)/length,(y2-y1)/length
    f.path(f'M{x1+ux*24},{y1+uy*24} L{x2-ux*27},{y2-uy*27}',BAD if dst=='bad' else MUTED)
for name,(x,y) in positions.items():
    f.circle(x,y,23, '#e5eee7' if name not in ['start','bad'] else BG, BAD if name=='bad' else INK)
    f.text(x,y+8, 'S' if name=='start' else '×' if name=='bad' else name,23,BAD if name=='bad' else INK,700,'middle')
f.text(75,325,'Start',21,anchor='middle')
f.text(350,325,'Private internal states',21,MUTED,anchor='middle')
f.text(640,325,'Forbidden',21,BAD,anchor='middle')
f.path('M36 348 H684','#cbd0c8',1,False)
f.text(36,383,'COMPRESSED / 3 states',17,MUTED,700)
f.path('M100 460 H320')
f.path('M402 460 H611',BAD)
f.path('M382 430 C452 365 268 365 338 430')
for x,label in [(75,'S'),(360,'Work'),(640,'×')]:
    f.circle(x,460,37 if label=='Work' else 23,'#e5eee7' if label=='Work' else BG,BAD if label=='×' else INK)
    f.text(x,468,label,22,BAD if label=='×' else INK,700,'middle')
f.text(75,518,'Start',21,anchor='middle')
f.text(360,518,'a, b, c, d merged',21,MUTED,anchor='middle')
f.text(640,518,'Forbidden',21,BAD,anchor='middle')
f.save('abstraction-map.svg')

rows=[{'s':s,'r':r,'feasible':2*s+r>=16 and r<=4,'cost':s*s+2*r*r} for r in range(5) for s in range(11)]
feasible=[p for p in rows if p['feasible']]
best=min(feasible,key=lambda p:p['cost'])
assert len(feasible)==19 and (best['s'],best['r'],best['cost'])==(7,2,57)
assert sum(p['cost']==57 for p in feasible)==1
assert 2*7+1 < 16
f=Figure(570,'A configuration search with a checked witness',
         'Fifty-five thermal setting pairs with all digital controls enabled. Nineteen are feasible. The unique minimum cost in this grid is 57 at s=7,r=2; the independent certificate in the essay proves the global integer minimum. The near miss s=7,r=1 is marked with a cross.')
f.text(36,45,'Find a design that meets the constraints.',26,weight=700)
f.text(36,80,'Five digital controls fixed on · 19 of 55 thermal settings pass',20,MUTED)
f.text(51,124,'r',22,weight=700,anchor='middle')
for p in rows:
    s,r=p['s'],p['r']; x,y=87+s*48,144+(4-r)*48
    f.rect(x,y,48,48,'#c9dfd3' if p['feasible'] else '#e6e7e2')
    if p['feasible'] and (s,r)!=(7,2):f.circle(x+24,y+24,4,GREEN,GREEN,1)
    if (s,r)==(7,2):
        f.circle(x+24,y+24,20,BG,GREEN,2.5)
        f.text(x+24,y+31,'57',21,GREEN,700,'middle')
    if (s,r)==(7,1):f.text(x+24,y+32,'×',30,BAD,700,'middle')
for r in range(5):f.text(65,144+(4-r)*48+31,str(r),20,anchor='end')
for s in range(11):f.text(87+s*48+24,414,str(s),20,anchor='middle')
f.text(351,448,'Attenuation setting s',22,anchor='middle')
f.text(36,488,'●',20,GREEN)
f.text(63,488,'Feasible in the model',20)
f.text(380,488,'×',26,BAD)
f.text(408,488,'Near miss: (7,1)',20)
f.text(36,529,'57',23,GREEN,700)
f.text(78,529,'Least cost: (7,2)',20)
f.text(380,529,'r = regulation setting',20,MUTED)
f.save('containment-search.svg')

receipt={'graph':{'concrete_edges':concrete,'abstraction':alpha,'abstract_edges':abstract,
                  'checks':['All concrete edges map to an abstract edge','Self-loop retained','Bad remains reachable','Deleting Work-to-Bad falsely removes the bad path']},
         'grid':{'rows':rows,'feasible_count':19,'winner':best,'digital_controls':'all five enabled',
                 'scope':'This renderer checks the 55-cell slice. The separate lab certificate establishes the global integer lower bound.'}}
(OUT/'abstraction-visual-checks.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: every graph edge preserved; 55 exact settings, 19 feasible, unique grid winner (7,2), cost 57.')
