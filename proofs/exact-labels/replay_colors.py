"""Independent exhaustive checks for the essay's finite color examples.

Only Python's standard library is required. This checks finite functions and
four arithmetic equations; the all-real theorem is proved separately in Lean.
"""
from itertools import product
from pathlib import Path
import argparse
import json

BITS=(0,1)
TABLES=tuple(product(BITS, repeat=4))
def apply(table,a,b): return table[2*a+b]

def run():
    # All possible functions on four residues, without an affine restriction.
    accepted=[]
    for labels in product(BITS,repeat=4):
        if labels[0]==labels[1]: continue
        witnesses={}
        for name,operation in [('subtract',lambda a,b:a-b),('multiply',lambda a,b:a*b)]:
            tables=[t for t in TABLES if all(
                apply(t,labels[a],labels[b])==labels[operation(a,b)%4]
                for a,b in product(range(4),repeat=2))]
            if tables:witnesses[name]=tables
        if len(witnesses)==2:accepted.append({'labels':labels,'tables':witnesses})
    expected={(0,1,0,1),(1,0,1,0)}
    if {r['labels'] for r in accepted}!=expected:raise ValueError('Unexpected finite representations')
    # Exhaust all assignments and all label tables. The four actual real
    # identities involve only 0, 1, 2 and 1/2.
    total=0; survivors=[]; controls=[None]*4; first_failure=[0]*4
    for zero,one,two,half in product(BITS,repeat=4):
        if zero==one:continue
        for sub,mul in product(TABLES,repeat=2):
            total+=1
            tests=(apply(sub,two,one)==one, apply(sub,one,one)==zero,
                   apply(mul,two,half)==one, apply(mul,zero,half)==zero)
            row={'labels':[zero,one,two,half],'sub':sub,'mul':mul}
            if all(tests):survivors.append(row)
            else:first_failure[tests.index(False)]+=1
            for removed in range(4):
                if controls[removed] is None and all(t for j,t in enumerate(tests) if j!=removed):
                    controls[removed]=row
    if total!=2048 or survivors or any(c is None for c in controls):
        raise ValueError('Four-test obstruction or removal control failed')
    return {'schema':'exact-color-replay/1','finite_source':'integers modulo 4',
      'all_label_maps_examined':16,'nonconstant_exact_representations':accepted,
      'extension_values':['0','1','2','1/2'],
      'extension_equations':['2-1=1','1-1=0','2*(1/2)=1','0*(1/2)=0'],
      'extension_configurations_examined':total,'extension_survivors':len(survivors),
      'first_failed_equation_counts':first_failure,
      'remove_one_equation_controls':controls,
      'scope':'Finite exhaustive verification; the unrestricted real statement requires the separate proof.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path);a=p.parse_args()
    result=run();text=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if a.out:a.out.write_text(text)
    print(json.dumps({'label_maps':result['all_label_maps_examined'],
      'accepted_maps':len(result['nonconstant_exact_representations']),
      'extension_configurations':result['extension_configurations_examined'],
      'extensions':result['extension_survivors'],'constraint_removal_controls':'4/4 satisfiable'}))
