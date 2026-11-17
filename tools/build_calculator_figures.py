"""Reproduce the essay's numerical figures; no generated imagery supplies data."""
from pathlib import Path
import json
import subprocess
import mpmath as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/essays/calculator'
DATA = ROOT / 'proofs/positive-seeds'
OUT.mkdir(parents=True, exist_ok=True)
DATA.mkdir(parents=True, exist_ok=True)
mp.mp.dps = 100
TEAL, INK, RUST = '#276c64', '#252927', '#a24832'
plt.rcParams.update({'svg.fonttype':'none', 'font.family':'DejaVu Sans', 'font.size':12,
                     'axes.labelcolor':INK, 'text.color':INK, 'xtick.color':INK, 'ytick.color':INK,
                     'axes.spines.top':False, 'axes.spines.right':False, 'svg.hashsalt':'calculator-v2'})

def T(b):
    q = mp.exp(-mp.exp(b))
    l = mp.log(b)
    return b-l+b*b*l*q/(1-b*l*q)

b = mp.exp(2)-mp.log(2)
rows = []
for n in range(9):
    rows.append({'round':n, 'value':mp.nstr(b,80), 'gap':mp.nstr(b-1,80),
                 'copied':2*5**n-1, 'saved':1+4*n})
    assert b > 1
    nxt = T(b)
    assert 1 < nxt < b
    b = nxt
root = mp.findroot(lambda x:T(x)-1, (mp.mpf('.85'),mp.mpf('.9')))
xs = [mp.mpf('.8')+mp.mpf('.15')*i/300 for i in range(301)]
mp.iv.dps = 50
bounds = {}
for s in ['0.85','0.90']:
    z=mp.iv.mpf(s); q=mp.iv.exp(-mp.iv.exp(z)); l=mp.iv.ln(z)
    t=z-l+z*z*l*q/(1-z*l*q)
    assert (t > 1) if s=='0.85' else (t < 1)
    bounds[s]=str(t)

reachable={0,15,3,5}
while True:
    bigger=reachable | {x^y for x in reachable for y in reachable} | {x^15 for x in reachable}
    if bigger==reachable: break
    reachable=bigger
assert reachable=={x for x in range(16) if x.bit_count()%2==0}
assert 1 not in reachable

evidence={'precision_decimal_digits':100,'initial_value':'exp(2)-ln(2)',
 'recurrence':'b-ln(b)+b^2*ln(b)*exp(-exp(b))/(1-b*ln(b)*exp(-exp(b)))',
 'scope':'Numerical illustrations of exact-real results; not Lean proofs or certified browser arithmetic.',
 'rounds':rows, 'crossing':{'recipe':'T(c), four presses directly on c, without initialization',
 'root_approximation':mp.nstr(root,80),'endpoint_interval_enclosures':bounds,
 'samples':[{'start':mp.nstr(x,20),'answer':mp.nstr(T(x),40)} for x in xs]},
 'parity':{'initial_patterns':['0000','1111','0011','0101'],
 'reachable':[f'{x:04b}' for x in sorted(reachable)],'target':'0001'}}
(DATA/'visual-data.json').write_text(json.dumps(evidence,indent=2)+'\n')

def save(fig,name):
    fig.savefig(OUT/(name+'.svg'),facecolor='white',metadata={'Date':None},bbox_inches='tight')
    plt.close(fig)

for mobile in [False,True]:
    suffix='-mobile' if mobile else ''
    size=(4.8,4.1) if mobile else (8,4.1)
    fig,ax=plt.subplots(figsize=size,layout='constrained')
    ax.plot(range(9),[float(mp.mpf(r['gap'])) for r in rows],'-o',color=TEAL,lw=2.5,ms=5)
    ax.set(yscale='log',xlabel='Completed four-press rounds',ylabel='Gap above 1',xticks=range(9),ylim=(1e-5,10))
    ticks=[10,1,.1,.01,.001,.0001,.00001]
    ax.yaxis.set_major_locator(FixedLocator(ticks))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x,p:format(x,'.5f').rstrip('0').rstrip('.') if x<1 else str(int(x))))
    ax.minorticks_off(); ax.grid(axis='y',color='#ddddda',lw=.7)
    ax.set_title('Each horizontal line means a tenfold smaller gap',fontsize=11,pad=17)
    save(fig,'gap'+suffix)

    fig,ax=plt.subplots(figsize=size,layout='constrained')
    ax.plot([float(x) for x in xs],[float(T(x)) for x in xs],color=TEAL,lw=2.5)
    ax.axhline(1,color=RUST,lw=1.5,ls='--',label='Target: 1')
    ax.scatter([float(root)],[1],color=INK,zorder=4,s=35)
    ax.annotate('Crossing near 0.86564',xy=(float(root),1),xytext=(.825,1.005),fontsize=11,
                arrowprops={'arrowstyle':'->','color':INK},color=INK)
    ax.set(xlabel='Starting number',ylabel='Answer after four presses',xlim=(.8,.95),ylim=(.9965,1.009),xticks=[.8,.85,.9,.95],yticks=[.998,1,1.002,1.004,1.006,1.008])
    ax.ticklabel_format(axis='y',style='plain',useOffset=False)
    ax.grid(axis='y',color='#ddddda',lw=.7);ax.legend(frameon=False,loc='upper right',fontsize=11)
    save(fig,'crossing'+suffix)

    fig,ax=plt.subplots(figsize=size,layout='constrained')
    ax.plot(range(9),[r['copied'] for r in rows],'-o',color=RUST,lw=2.5,ms=5,label='Copy every earlier recipe')
    ax.plot(range(9),[r['saved'] for r in rows],'-s',color=TEAL,lw=2.5,ms=5,label='Save and reuse answers')
    ax.set(yscale='log',xlabel='Completed four-press rounds',ylabel='Written instructions',xticks=range(9),ylim=(.7,2e6))
    ax.yaxis.set_major_locator(FixedLocator([1,10,100,1000,10000,100000,1000000]))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x,p:format(int(x),',')))
    ax.minorticks_off();ax.grid(axis='y',color='#ddddda',lw=.7)
    ax.legend(frameon=False,loc='upper left',fontsize=10)
    ax.set_title('Each horizontal line means ten times as many',fontsize=11,pad=17)
    save(fig,'growth'+suffix)

# Nine operation nodes versus five: leaf inputs c=2 are deliberately not counted.
common='graph [bgcolor="white",rankdir=BT,pad="0.25",nodesep="0.35",ranksep="0.45"]; node [shape=circle,fontname="sans-serif",fontsize=16,style=filled,color="#276c64",fillcolor="#e8f2ef",width=.48]; edge [color="#5d6662",fontname="sans-serif",fontsize=12,arrowsize=.7];'
tree='digraph G {'+common+' b1[label="B"];b2[label="B"];b3[label="B"];b4[label="B"];b5[label="B"];u[label="U"];v[label="V"];w[label="W"];n[label="Next"]; b1->u[label="L"];b2->u[label="R"];u->v[label="L"];b3->v[label="R"];b4->w[label="L"];v->w[label="R"];w->n[label="L"];b5->n[label="R"]; }'
shared='digraph G {'+common+' b[label="B"];u[label="U"];v[label="V"];w[label="W"];n[label="Next"]; b->u[label="L"];b->u[label="R"];u->v[label="L"];b->v[label="R"];b->w[label="L"];v->w[label="R"];w->n[label="L"];b->n[label="R"]; }'
for name,dot in [('copied-tree',tree),('saved-graph',shared)]:
    subprocess.run(['dot','-Tsvg','-o',str(OUT/(name+'.svg'))],input=dot,text=True,check=True)
print('Built six plots, two graphs, and data with positive gaps, interval sign checks, and all 16 patterns checked.')
