"""Regenerate six guided notebooks from prose/code cells kept in this script."""
from pathlib import Path
import nbformat as nbf

ROOT=Path(__file__).resolve().parents[1]


def make(filename, title, intro, cells):
    notebook=nbf.v4.new_notebook()
    notebook['metadata']={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
                          'language_info':{'name':'python'}}
    notebook.cells=[nbf.v4.new_markdown_cell(f'# {title}\n\n{intro}')]
    for kind,content in cells:
        notebook.cells.append(nbf.v4.new_markdown_cell(content) if kind=='md' else nbf.v4.new_code_cell(content))
    path=ROOT/'notebooks'/filename
    nbf.write(notebook,path)
    print(path.name)


make('01_fano.ipynb','Lab I — Seven points that make a universe',
     'From the booklet\'s Extended Laboratory I. We will construct the Fano plane as an incidence geometry, not by assuming the Euclidean picture is its geometry.',[
('code','''from itertools import combinations
from lasensei.geometry import FANO_POINTS, FANO_LINES, all_codewords, hamming_weight
from lasensei.lab_registry import fano
fano()'''),
('md','### Check the defining incidence theorem\n\nEvery pair of distinct points lies on **exactly one** line. Explain why $u+v$ is the third projective point.'),
('code','''incidences = {pair: sum(set(pair).issubset(line) for line in FANO_LINES)
              for pair in combinations(FANO_POINTS,2)}
assert len(incidences)==21 and set(incidences.values())=={1}
FANO_LINES'''),
('md','### Visualize the incidence pattern\n\nOne projective line appears as a circle. That is a property of the **drawing**, not the mathematical line.'),
('code','''import matplotlib.pyplot as plt
from matplotlib.patches import Circle
coords={4:(0,2.15),2:(-1.86,-1.08),1:(1.86,-1.08),3:(0,-1.08),5:(.93,.535),6:(-.93,.535),7:(0,0)}
fig,ax=plt.subplots(figsize=(6,6))
for line in [([4,2,6]),([4,1,5]),([2,1,3]),([4,3,7]),([2,5,7]),([1,6,7])]:
    xs,ys=zip(*(coords[i] for i in line))
    ax.plot(xs,ys)
ax.add_patch(Circle((0,0),1.075,fill=False,linewidth=2))  # 3,5,6
for i,(x,y) in coords.items():
    ax.scatter(x,y,s=65)
    ax.annotate(f'{i:03b}',(x,y),xytext=(6,6),textcoords='offset points')
ax.set_aspect('equal');ax.axis('off');ax.set_title('Seven points, seven projective lines');plt.show()'''),
('md','### Coding connection\n\nCheck that the minimum nonzero Hamming weight is 3 and that there are seven weight-three words. Explain why the support of such a word is a Fano line.'),
('code','''from collections import Counter
weights=Counter(hamming_weight(c) for c in all_codewords())
assert weights[3]==7
weights'''),
('md','**Proof challenge:** Why can the same Fano dependence pattern not be realized over an odd-characteristic field? Locate the determinant $-2$ obstruction in the booklet.\n\nRelated exercises: E01.04, E13.02, E14.05.')])

make('02_three_passports.ipynb','Lab II — Same matrix, three passports',
     'The **same array of entries** lives in different scalar worlds. Be precise about restriction versus extension of scalars.',[
('code','''from lasensei.finite import F2,F4,F8
from lasensei.linear import power,eye,vec
from lasensei.lab_registry import passports
passports()'''),
('md','### Passport 1: a binary operator\n\nThe three nonzero vectors cycle. There is no nonzero fixed eigenvector, and $A^3=I$.'),
('code','''A=[[0,1],[1,1]]
v=[1,0]
orbit=[]
for _ in range(3):
    orbit.append(v)
    v=vec(A,v,F2)
assert v==[1,0] and power(A,3,F2)==eye(2)
orbit'''),
('md','### Passport 2: multiplication by $\\alpha$ on $\\mathbb F_4$'),
('code','''alpha=2  # encoded as 0+1*alpha
[F4.display(F4.mul(alpha,x)) for x in (1,alpha,F4.mul(alpha,alpha))]'''),
('md','### Passport 3: scalar extension produces two eigenvectors'),
('code','''roots=[x for x in range(4) if F4.add(F4.add(F4.mul(x,x),x),1)==0]
assert roots==[2,3]
for x in roots:
    e=[1,x]
    assert vec(A,e,F4)==[F4.mul(x,z) for z in e]
[(F4.display(x), [F4.display(z) for z in [1,x]]) for x in roots]'''),
('md','**Exercise:** What is the dimension over $\\mathbb F_4$ before and after scalar extension? Why is the one-dimensional $\\mathbb F_4$ multiplication operator a different scalar description?\n\nRelated exercises: E02.01, E03.01, E03.04.')])

make('03_hamming.ipynb','Lab III — Decode a damaged seven-bit message',
     'Use the exact parity-check matrix and convention from Chapter 13. A one-bit error is corrected, but do not mistake this for arbitrary error correction.',[
('code','''from collections import Counter
from lasensei.geometry import (H,hamming_encode,syndrome,hamming_decode,
                                 all_codewords,hamming_weight)
from lasensei.lab_registry import hamming
hamming()'''),
('md','### Encode, corrupt and repair'),
('code','''c=hamming_encode((1,0,1,1))
r=list(c);r[5]^=1
fixed,position=hamming_decode(r)
assert fixed==c and position==6
{'H':H,'c':c,'r':r,'syndrome':syndrome(r),'decoded':fixed}'''),
('md','### Enumerate all codeword weights'),
('code','''weights=Counter(map(hamming_weight,all_codewords()))
assert len(all_codewords())==16 and weights[3]==7
weights'''),
('code','''import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(6,3))
ax.bar(list(sorted(weights)),[weights[w] for w in sorted(weights)])
ax.set(xlabel='Hamming weight',ylabel='Number of codewords',title='Weight enumerator of the binary [7,4,3] code')
plt.show()'''),
('md','### A boundary case: two-bit error\n\nA decoder designed for one error can produce another *wrong* codeword after two errors. Identify the first failure of its promise.'),
('code','''two=list(c);two[0]^=1;two[1]^=1
wrong,guessed=hamming_decode(two)
assert wrong != c
{'two_errors_received':two,'guessed_bit':guessed,'incorrect_decode':wrong}'''),
('md','**Proof challenge:** Show that no nonzero codeword has weight 1 or 2. Why are the seven weight-three words exactly the Fano lines?\n\nRelated exercises: E13.01 and E13.02.')])

make('04_similarity.ipynb','Lab IV — Polynomial matrices and similarity',
     'The characteristic polynomial alone fails to determine similarity; the minimal polynomial and the ranks of $p(T)^k$ tell a finer story.',[
('code','''from lasensei.lab_registry import similarity
from lasensei.finite import F2
from lasensei.linear import (rank,eye,poly_eval_matrix,minimal_polynomial, power)
result=similarity(); result'''),
('md','### Evaluate the same irreducible polynomial at both operators'),
('code','''A,B=result['A'],result['B']
pA=poly_eval_matrix([1,1,1],A,F2)
pB=poly_eval_matrix([1,1,1],B,F2)
assert rank(pA,F2)==0 and rank(pB,F2)==2
{'rank_pA':rank(pA,F2),'rank_pB':rank(pB,F2)}'''),
('md','### Read block size using generalized kernels'),
('code','''from lasensei.linear import mul
qB=mul(pB,pB,F2)
assert rank(qB,F2)==0
[(k,4-rank(poly_eval_matrix([1,1,1],T,F2),F2)) for k,T in [('A',A),('B',B)]]'''),
('md','**Prove:** similar matrices have equal minimal polynomials. Give the module-theoretic explanation for the two different primary decompositions.\n\nRelated exercises: E04.01, E04.03.')])

make('05_torsion.ipynb','Lab V — Arithmetic invisible over the rationals',
     'Rank over $\\mathbb Q$ sees an isomorphism. Smith invariants over $\\mathbb Z$ preserve the finite torsion it forgets.',[
('code','''from lasensei.lab_registry import torsion
from lasensei.rings import smith_2x2_full_rank,rank_mod
result=torsion();result'''),
('md','### Detect primes by reduction'),
('code','''D=[[2,4],[0,6]]
primes=[2,3,5,7,11,13]
ranks={p:rank_mod(D,p) for p in primes}
assert ranks=={2:0,3:1,5:2,7:2,11:2,13:2}
ranks'''),
('code','''import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(6,3))
ax.plot(list(ranks),list(ranks.values()),'o-')
ax.set(xlabel='Prime p',ylabel='rank(D mod p)',title='Arithmetic rank jumps',ylim=(-.1,2.3),yticks=[0,1,2]);plt.show()'''),
('md','**Derive:** $d_1=\\gcd(2,4,0,6)=2$ and $d_1d_2=|\\det D|=12$. Why does tensoring the cokernel with $\\mathbb Q$ annihilate both finite cyclic summands?\n\nRelated exercises: E11.03 and E11.04.')])

make('06_transients.ipynb','Lab VI — Nonnormal transient amplification',
     'A stable spectral radius does not bound finite-time amplification. Here is the analytic Jordan-type formula and its Euclidean operator norm.',[
('code','''from lasensei.lab_registry import transients
from lasensei.numerical import jordan_power,norm2,transient_profile
result=transients();result'''),
('md','### Verify the formula $T^n$ and compare couplings'),
('code','''a=.8
Ms=[1,10,30,100]
profiles={M:transient_profile(a,M,steps=70) for M in Ms}
[(M,max(v,key=lambda x:x[1])) for M,v in profiles.items()]'''),
('code','''import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(9,5))
for M,v in profiles.items():
    ax.plot([n for n,_ in v],[norm for _,norm in v],label=f'M={M}')
ax.axhline(1,linestyle='--',label='norm = 1')
ax.set(xlabel='Power n',ylabel=r'Operator norm $\\|T^n\\|_2$',title='Same eigenvalues, radically different transient growth')
ax.legend();plt.show()'''),
('md','**Explain:** If the eigenvalues equal $a=0.8$, why does larger $M$ lead to larger transient norms? Why is a norm essential in this question? What can an $\\varepsilon$-pseudospectrum detect that the eigenvalues alone do not?')])
