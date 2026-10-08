#!/usr/bin/env python3
"""Exact diagrams, checked against the finite case graph."""
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'assets/essays'
BG, INK, MUTED, GREEN, RUST = '#faf9f5', '#242b2b', '#58615e', '#086451', '#93422c'


class Figure:
    def __init__(self, height, title, desc):
        self.p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{height}" viewBox="0 0 720 {height}" role="img" aria-labelledby="title desc">',
                  f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>',
                  f'<rect width="720" height="{height}" fill="{BG}"/>',
                  '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10Z" fill="context-stroke"/></marker></defs>']

    def text(self, x, y, text, size=20, color=INK, weight=400, anchor='start'):
        self.p.append(f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(text)}</text>')

    def box(self, x, y, w, h, fill=BG, stroke='#b7c3ba'):
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

    def arrow(self, d, color=GREEN):
        self.p.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.5" marker-end="url(#a)"/>')

    def save(self, name):
        (OUT/name).write_text('\n'.join(self.p+['</svg>'])+'\n')


def phase(state):
    status, first, _ = state
    return 'approved' if status == 151 else 'cancelled' if status == 152 else 'empty' if first == 160 else 'one'


data = json.loads((ROOT/'examples/two-key-release/evidence/finite-check.json').read_text())
edges = {(phase(e['state']), phase(e['next'])) for e in data['edges']}
expected = {('empty','one'), ('one','approved'), ('empty','cancelled'), ('one','cancelled')}
expected |= {(s,s) for s in ('empty','one','approved','cancelled')}
assert edges == expected
assert all((e['releases'] == 1) == (phase(e['state']) == 'one' and phase(e['next']) == 'approved') for e in data['edges'])

f = Figure(450, 'Two keys, one release intent',
           'Four phases group fourteen reachable states. First approval records an ID. A different ID completes approval and emits one release intent. Either pending phase can cancel. The loop on each phase denotes a rejected attempt that changes nothing.')
f.text(36,44,'Two keys, one release intent',27,weight=700)
f.text(36,78,'“Key” means an approval by an ID, not a cryptographic signature.',17,MUTED)
for x, title, line, color in [(36,'Pending','no approvals',MUTED),(276,'Pending','first ID saved',INK),(516,'Approved','release intent: 1',GREEN)]:
    f.box(x,150,168,76,'#e8efe8' if title=='Approved' else BG)
    f.text(x+84,180,title,22,color,700,'middle')
    f.text(x+84,208,line,17,color,anchor='middle')
    f.arrow(f'M{x+105} 150 C{x+159} 92 {x+19} 92 {x+63} 150',MUTED)
f.arrow('M204 188 H274');f.arrow('M444 188 H514')
f.text(240,247,'first ID',16,MUTED,anchor='middle')
f.text(480,247,'different ID',16,GREEN,anchor='middle')
f.box(276,302,168,70,'#f1e7df','#cdb2a2')
f.text(360,332,'Cancelled',22,RUST,700,'middle')
f.text(360,357,'release intent: 0',17,RUST,anchor='middle')
f.arrow('M120 226 V338 H274',RUST)
f.text(145,323,'cancel',17,RUST)
f.arrow('M360 226 V300',RUST)
f.text(375,281,'cancel',17,RUST)
f.arrow('M444 330 C515 288 515 388 444 351',MUTED)
f.text(36,407,'Loops: rejected attempts leave state and outbox unchanged.',18,MUTED)
f.text(36,435,'Only recognized IDs can approve or cancel a pending request.',18,MUTED)
f.save('two-key-state.svg')

f = Figure(520,'Separate meaning, decision and action',
           'A human chooses the intended rules. An agent and the factory produce a contract. The pure verified Authority evaluates explicit state, command and context under that contract. Only a law-admitted committing decision produces a private publication for the imperative shell. Authentication, storage and external delivery remain outside the pure core.')
f.text(36,45,'Meaning → decision → action',28,weight=700)
f.box(36,78,648,96,'#e8efe8')
f.text(56,107,'HUMAN STEERING',16,GREEN,700)
f.text(56,138,'Choose the rules and what counts as success.',23,weight=700)
f.text(56,160,'Agent + factory produce the explicit contract P.',18,MUTED)
f.arrow('M232 174 V217')
f.text(260,202,'contract',17,MUTED)
f.box(36,222,400,182,BG,GREEN)
f.text(56,252,'VERIFIED FUNCTIONAL CORE',17,GREEN,700)
f.text(56,288,'D = Fₚ(state, command, context)',24,weight=700)
f.text(56,324,'Typed inputs · checked laws · metered work',18,MUTED)
f.text(56,355,'No database, network or callbacks here.',18,INK)
f.text(56,383,'Reject / refuse → no commit capability',18,RUST)
f.box(482,222,202,182,'#eeeae2')
f.text(500,252,'IMPERATIVE SHELL',16,INK,700)
f.text(500,289,'Commit state',22,weight=700)
f.text(500,318,'+ outbox',22,weight=700)
f.text(500,356,'Then deliver',19,MUTED)
f.text(500,383,'explicit intents.',19,MUTED)
f.arrow('M436 290 H480')
f.text(459,327,'pub',14,GREEN,700,'middle')
f.text(36,447,'pub: a private Publication, created only by Authority.',18,MUTED)
f.text(36,480,'Outside the core: authenticate IDs, protect storage, handle retries.',18,MUTED)
f.text(36,507,'Those responsibilities need their own evidence.',18,MUTED)
f.save('zenofcis-boundary.svg')
print('Rendered two exact figures; all abstract state edges match the 112-edge case graph.')
