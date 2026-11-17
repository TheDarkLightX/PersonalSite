---
title: "Positive Seeds, Exactness, and Certificates for Operation Search"
author: "Dana Edwards"
date: "16 November 2026"
lang: en-US
documentclass: article
fontsize: 11pt
geometry: [letterpaper, margin=0.9in]
mainfont: Latin Modern Roman
sansfont: Latin Modern Sans
monofont: Latin Modern Mono
colorlinks: true
linkcolor: black
urlcolor: blue
header-includes:
  - |
    \usepackage{amsmath,amssymb,amsthm,booktabs,longtable,array}
    \usepackage{microtype}
    \usepackage{placeins,needspace}
    \usepackage{fvextra}
    \DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaklines,commandchars=\\\{\}}
    \setlength{\emergencystretch}{3em}
    \widowpenalty=10000
    \clubpenalty=10000
    \displaywidowpenalty=10000
    \setlength{\parskip}{0.35em}
    \setlength{\parindent}{0pt}
    \linespread{1.02}
    \setcounter{tocdepth}{1}
abstract: |
  We study how constants and strict domains govern operation search for $F(a,b)=\exp(a)-\log b$, defined when $b>0$. A fixed four-node, constant-free term drives every positive seed toward 1. It gives a short constructive proof that every positive ground orbit is dense, an explicit convergence bound, and a strict-domain criterion for uniform approximation on each compact set. Exact seeds are dense as well. They satisfy a dichotomy: either every positive seed generates 1 exactly, or the exact seeds form a countable dense set. O-minimality further makes every finite syntax-budget subset finite in the latter case. For finitely many named seeds, the corresponding proper exact-seed sets are dense but null and meagre. We also give compact domain-safe arithmetic terms and study finite operation languages through their evaluation columns. Their least closed column relation is a complete impossibility certificate on a full finite domain; a definedness-preserving map transports such exclusions between representations. Lean checks the arithmetic, positive-seed density, density of exact seeds, analytic dichotomy, and general certificate and transport theorems. The positive-seed compact-approximation theorem is also formalized; the o-minimal consequences use ordinary proofs. Exact finite experiments reproduce matrix-generator costs and extend the certificate census. Exact sufficiency of seed 2 and expression optimality remain open.

---

# Scope and contribution

An operation language can approximate every target while expressing only countably many values exactly. It can also fail a target for a reason that a small certificate exposes without enumerating expressions. Both questions depend on the same contract: the carrier, constants, primitive operations, evaluation rules, and target domain.

Our continuous example is the strict real exp-minus-log operation introduced in Odrzywołek's single-operation language [1]. We retain real intermediate values and require every logarithm argument to be positive. This differs from constructions that use complex branches or extend undefined real operations. The established seed-1 arithmetic construction supplies a starting point [2]. We give shorter explicit terms, then remove exact access to 1 for approximation by constructing a constant-free attracting term.

The resulting proof answers several questions about the seed parameter. Every positive seed has a dense ground orbit. Exact seeds are themselves dense, yet may still be countable. A fixed compact domain admits constant-free uniform approximation precisely when one coordinate is positive throughout it. These results concern identical $F$ nodes and restricted constants. Germany, Abdo, and Bakarji's approximation theorem [15] studies a richer, six-parameter EML atom and provides Sobolev approximation rates. Our contribution is a constant-policy and strict-domain analysis, complementary to that work. Stachowiak [13] and Odrzywołek [14] give broader algebraic and operator-family perspectives.

In the finite setting, classical semiring classification reduces exact completeness to matrix-algebra generation [5]. We retain an independently reproduced experiment showing that the choice of named generators affects shortest-expression costs. We then make the relation-preservation view explicit: the set of attainable evaluation columns is the least invariant relation and is therefore a complete negative certificate on a full finite domain. This is an application of established preservation and unrealizability theory [8,10,11]. Its value here is the precise treatment of strict partial evaluation, reusable negative information, and transport between representations.

The accompanying Lean development checks the central algebraic and analytic results, with an explicit coverage table in Section 8. Ordinary proofs establish the additional approximation, dynamical, and o-minimal consequences. Finite experiments and historical runtime measurements are identified separately. Fixed-seed countability is consistent with computability-based inexpressibility [3]; the symmetry discussion in [4] addresses a different motivation. The paper makes no worldwide-priority claim and does not equate mathematical formalization with verification of a numerical evaluator or runtime adapter.

# Strict real arithmetic with one named constant

## Semantic contract and elementary constructions

Throughout Sections 2 and 3, the sole primitive is

$$
F(a,b)=e^a-\log b,\qquad (a,b)\in\mathbb R\times(0,\infty).
$$

Evaluation is strict: every child expression must be defined, every logarithm argument must be positive, and every intermediate value is an ordinary finite real number. Infinite values, complex branches, and limiting assignments at missing points are excluded. A finite real can still be too large for a particular implementation to evaluate.

Initially the allowed constant is 1. Define

$$
\begin{aligned}
E(x)&=F(x,1)=e^x,\\
L(u)&=F(1,E(F(1,u)))=\log u \quad(u>0),\\
P(x)&=F(x,E(x))=e^x-x\ge1,\\
H(x)&=L(P(x)).
\end{aligned}
$$

The logarithm identity follows by direct substitution. The inequality $e^x\ge1+x$ makes $P$ positive on the entire real line, so $H$ is also total and nonnegative. For variable arguments, $E,L,P,H$ contain respectively 1, 3, 2, and 5 primitive $F$ nodes.

Addition and subtraction have total real representations:

$$
\begin{aligned}
A(x,y)&=F\bigl(y,E(F(H(y),E(x)))\bigr)=x+y,\\
S(x,y)&=F\bigl(H(y),E(F(y,E(x)))\bigr)=x-y.
\end{aligned}
$$

For example, the first expression is $e^y-(P(y)-x)=x+y$; the second is $P(y)-(e^y-x)=x-y$. Each has nine primitive nodes. Every logarithm sees 1, a positive exponential, or $P(y)\ge1$. These formulas establish their domains as well as their values. The positive-envelope method and real arithmetic completeness already occur in the inspected public formalization associated with Naskręcki and collaborators [2]. The present work specializes that method to reduce explicit expression sizes.

## Multiplication by alternating exponentials

For arbitrary real $a,b,c,d$, put

$$
T(a,b,d,c)=F\bigl(a,E(F(b,E(F(d,E(E(c))))))\bigr).
$$

Expanding from the inside gives

$$
T(a,b,d,c)=e^a-e^b+e^d-e^c.
$$

The wrapper adds seven $F$ nodes. Its second arguments are exponentials, so differences occurring inside it may have either sign.

To obtain multiplication, take

$$
a=x+y,\qquad b=x+H(y),\qquad c=H(x)+y,\qquad d=H(x)+H(y).
$$

Then

$$
T(a,b,d,c)=(e^x-P(x))(e^y-P(y))=xy.
$$

The direct use of addition macros gives a valid construction. A smaller expansion uses

$$
J(x)=F(H(x),P(x))=P(x)-\log P(x)\ge1,
$$

where $u-\log u\ge1$ for $u>0$, followed by

$$
\begin{aligned}
a&=F(y,E(F(H(y),E(x)))),\\
b&=F(x,E(F(H(x),P(y)))),\\
c&=F(y,E(F(H(y),P(x)))),\\
d&=F(H(x),E(F(L(J(x)),P(y)))).
\end{aligned}
$$

These expressions equal the four sums above. In particular,
$b=e^x-(P(x)-H(y))=x+H(y)$ and
$d=P(x)-(J(x)-H(y))=H(x)+H(y)$.
Their primitive-node counts are 9, 10, 10, and 21. Thus

$$
M(x,y)=T(a,b,d,c)=xy
$$

has $9+10+10+21+7=57$ primitive nodes and is defined on all of $\mathbb R^2$. All nontrivial logarithm arguments are $P(x),P(y),J(x)$, each at least 1; the remaining ones are exponentials or the constant 1. Zero and negative inputs require no exceptions.

## A stronger envelope for division

Define

$$
R(x)=F(E(x),E(x))=e^{e^x}-x.
$$

Since $e^{e^x}>e^x\ge1+x$, we have $R(x)>1$ for every real $x$. Both $\log R(x)$ and $\log\log R(x)$ are therefore legal. For $y>0$, set

$$
D_+(x,y)=F\left(F(x,y),
 E\left(E\left(F(L(L(R(x))),y)\right)\right)\right).
$$

The exponential of the first argument of the outermost $F$ equals $e^{e^x}/y$. The logarithm of its second argument equals

$$
\exp\bigl(F(L(L(R(x))),y)\bigr)
=\exp(\log R(x)-\log y)=R(x)/y.
$$

Consequently $D_+(x,y)=x/y$. Every node is defined for $y>0$; the explicit subterm $F(x,y)$ makes the expression undefined for $y\le0$. Its natural domain is exactly $\mathbb R\times(0,\infty)$.

This tree has 14 primitive nodes: three in $R$, six from the two $L$ applications, two nodes with second argument $y$, and three for the outer $F$ and its two $E$ applications. The numerator occurs three times and the denominator twice. Hence

$$
I(x)=D_+(x,M(x,x)),\qquad
D(x,y)=D_+(M(x,y),M(y,y))
$$

represent $1/x$ for $x\ne0$ and $x/y$ for $y\ne0$. Their natural domains are exactly the stated domains, because the square denominator is positive exactly when its input is nonzero. Together, $E,L,A,S,M,D$ give fixed representations of exponential, logarithm, addition, subtraction, multiplication, and division from $F$ and 1. In this report, exact exp-log-arithmetic completeness means representing these operations and the expressions built from them, variables, and 1. Zero is $L(1)$, and rational constants follow from arithmetic. It does not assert that every real number has a finite name.

## Syntax accounting and verification

A tree token is either a primitive node or a leaf. A binary tree with $m$ primitive nodes therefore has $2m+1$ tokens. Shared directed acyclic graphs are counted separately.

| Target and natural domain | Primitive tree nodes | Tree tokens | Shared primitive nodes |
|:--|--:|--:|--:|
| Multiplication, $\mathbb R^2$ | 57 | 115 | 33 |
| Square, $\mathbb R$ | 57 | 115 | 24 |
| Quotient, $y>0$ | 14 | 29 | 13 |
| Reciprocal, $x\ne0$ | 128 | 257 | 36 |
| Quotient, $y\ne0$ | 299 | 599 | 61 |

The last two tree counts are $14+2\cdot57$ and $14+3\cdot57+2\cdot57$. The companion audit's constructions for the same strict domains used 1,019 multiplication tokens, 6,197 reciprocal tokens, and 9,251 division tokens. These are comparisons between retained upper bounds, not optimality claims or comparisons with restricted-domain identities.

The expander retains raw and simplified trees. Its inverse cancellations are $L(E(u))\to u$, which preserves strict definedness, and $E(L(u))\to u$ only when positivity of $u$ is established. The latter premise is essential: deleting $\log u$ without it would enlarge the domain. The implementation uses positivity facts for 1, exponentials, and $P$. All emitted target nodes remain plain $F$ nodes.

An independent evaluator checked 50 valid input cases for each of the raw and simplified versions, using 300 decimal digits and normalized error below $10^{-70}$. Inputs included zeros, negative values, mixed signs, and unequal magnitudes. These 100 checks test the generated syntax; the algebra and domain proofs establish the universal identities. The evaluator's exponential-argument budget of $10^6$ is a computational bound. Nested exponentials and cancellation can make these expressions numerically impractical despite their shorter syntax.

# Positive seeds: approximation and exactness

## Ground generation and the role of 1

For a real seed $c$, let $\mathcal A(c)$ be the set of values of all defined finite ground $F$ terms whose only leaf is $c$. Write $K(c)=\overline{\mathcal A(c)}$ for its ordinary real closure. More generally, ground terms over a set $C$ may use any named constant in $C$.

\Needspace{6\baselineskip}

**Proposition 1 (exact constant reduction).** For a nonempty set $C$ of named real constants, the full strict real exp-log-arithmetic language is expressible by fixed $F$ terms if and only if the set of its defined ground-term values contains 1.

*Proof.* If 1 has a ground representation, substitute it into the constructions of Section 2. Conversely, fixed representations of exponential and subtraction compose to the constant function $\exp(x-x)=1$, defined for all real $x$. Substituting any named $c\in C$ for its variables gives a ground representation of 1. The argument requires a nonempty constant set and fixed operation terms; selecting a different expression separately at each input is a different specification. $\square$

If all named constants are nonpositive, no non-leaf ground term is defined: a deepest internal node has two constant leaves, with a nonpositive second argument. In particular, $\mathcal A(c)=\{c\}$ for $c\le0$. The positive case has a much stronger approximation property.

## A four-node attracting term

Define the constant-free unary term

$$
T(b)=F\bigl(F(b,F(F(b,b),b)),b\bigr).
$$

It contains four primitive nodes and five copies of its input. This small context supplies the positive-seed argument.

\Needspace{6\baselineskip}

**Theorem 2 (positive attractor).** The natural strict domain of $T$ is $(0,\infty)$. It maps that interval into itself, has the unique fixed point 1, and $T^n(c)\to1$ for every $c>0$. For $b>1$,

$$
1<T(b)<b-\frac23\log b<b.
$$

*Proof.* Put $H=\exp(\exp b)$ and $D=H-b\log b$. The inequalities $\exp(b-1)\ge b$ and $e>2$ give $\exp b>2b$ for $b>0$. Hence $H>4b^2$, and $\log b\le b-1$ yields

$$
D>3b^2+b>0.
$$

The inner logarithm argument is

$$
F(F(b,b),b)=\frac{H}{b}-\log b=\frac Db>0.
$$

Every other logarithm in the four-node tree has argument $b>0$. Expanding only after these domain checks gives

$$
\boxed{T(b)=b-\log b+\frac{b^2\log b}{H-b\log b}
       =b-(1-r(b))\log b},\qquad
r(b)=\frac{b^2}{H-b\log b}\in(0,1/3).
$$

For $b>1$, $b-\log b\ge1$ and the correction is strictly positive, giving the stated inequalities. At $b=1$, direct evaluation gives $T(1)=1$. For $0<b<1$, the same identity gives $T(b)>b>0$. The equation $T(b)=b$ is equivalent to $\log b=0$, so the only positive fixed point is 1.

An orbit that enters $[1,\infty)$ stays there and decreases to a limit at least 1. An orbit that stays below 1 increases and has a positive limit at most 1. Continuity makes either limit a fixed point, hence 1. For $b\le0$, the subterm $F(b,b)$ is undefined. This also proves the exact natural-domain claim. $\square$

The identity presents $T$ as a variable-step update using $\log b$, the derivative of $b\log b-b+1$. It is a useful change of representation for the proof. Differentiating at the fixed point gives $T'(1)=\exp(-e)$, approximately $0.06599$. The fixed iteration is locally linear, not quadratic.

## Constructive density and its cost

For a positive seed $c$, initialize $b_0=F(c,c)>2$, using $\exp c>1+c$ and $\log c\le c-1$, and set $b_{n+1}=T(b_n)$. Each $b_n$ is a defined ground term over $c$.

\Needspace{6\baselineskip}

**Theorem 3 (positive-seed density).** For every $c>0$,

$$
\overline{\mathcal A(c)}=\mathbb R.
$$

*Proof.* Theorem 2 gives $b_n\to1$, so $1\in K=\overline{\mathcal A(c)}$. The set $K$ is closed under every defined $F$ application. To see this, approximate $a,b\in K$, with $b>0$, by orbit elements $a_n,b_n$. Eventually $b_n>0$; continuity gives $F(a_n,b_n)\to F(a,b)\in K$. The domain-safe seed-1 constructions of Section 2 therefore place every rational in $K$. Closedness and density of $\mathbb Q$ imply $K=\mathbb R$. $\square$

This proof uses a single fixed syntactic iteration. It avoids extracting logarithms by asymptotic cancellation or classifying closed additive semigroups.

There is also an explicit convergence bound. Let $B=b_0$ and $\rho=1-2/(3B)\in(0,1)$. For $1\le b\le B$, $\log b\ge(b-1)/B$, so

$$
0<b_n-1\le\rho^n(B-1).
$$

For $0<\varepsilon<B-1$, it suffices to take

$$
n\ge\left\lceil\frac{\log((B-1)/\varepsilon)}{-\log\rho}\right\rceil.
$$

If the positive seed is a continuous function on a compact set, its initializer has a finite maximum $B>1$. The same estimate proves uniform convergence on that set.

For the literal initialized trees, $m_0=1$ and $m_{n+1}=4+5m_n$. Thus the construction has

$$
\begin{array}{c|c}
\text{Representation} & \text{Size after }n\text{ iterations}\\ \hline
\text{Primitive nodes in expanded tree} & 2\cdot5^n-1\\
\text{Tree tokens} & 4\cdot5^n-1\\
\text{Tree depth} & 1+4n\\
\text{Retained straight-line constructor nodes} & 1+4n
\end{array}
$$

The last row stores each iterate once and adds four new nodes per step. It counts retained instructions before optional simplification. These are constructive upper bounds, not minima. They expose the difference between tree and shared-graph representations without making a runtime claim.

![The four-node map and initialized convergence. Left: the transformed real formula for $T$ and the identity line; all values above 1 move downward toward 1. Right: errors for several positive seeds after the common initializer $F(c,c)$. These are high-precision illustrations of the proved bound, not proof by sampling.](figures/contraction.pdf){width=95%}

Every initialized iterate is strictly greater than 1. This supplies a useful negative result: **the entire initialized iteration family fails to produce 1 exactly at every finite stage**, even though it converges to 1. Density alone does not decide exact expressibility by other trees.

The original tree can be poorly conditioned because it forms nested exponentials and subtracts large values. A transformed formula can evaluate the correction using $\exp(-\exp b)$; that is a different runtime representation. Neither the iteration bound nor the shared-node count establishes numerical bit complexity.

\Needspace{6\baselineskip}

**Corollary 4 (closed scalar invariants).** The closed subsets of $\mathbb R$ stable under every defined $F$ application are exactly $\mathbb R$ and the closed subsets of $(-\infty,0]$, including the empty set.

A positive member forces the invariant to contain its dense orbit and hence all reals. If it has no positive member, stability is vacuous. A proper nonclosed invariant can still obstruct exact generation.

\Needspace{11\baselineskip}

## The strict-domain criterion for uniform approximation

**Theorem 5 (fixed-compact approximation).** Let $n\ge1$, let $K\subseteq\mathbb R^n$ be nonempty and compact, and let $C\subseteq\mathbb R$ be any set of named constants, possibly empty. Strict $F$ terms over $C$, defined on an open neighborhood of $K$, are uniformly dense in $C(K)$ if and only if either:

1. $C$ contains a positive constant; or
2. one fixed coordinate $x_j$ is positive at every point of $K$.

*Proof.* Choose a positive constant or the uniformly positive coordinate as a continuous seed function. The preceding construction gives constant-free or $C$-based terms $u_n$ converging uniformly to 1 on $K$.

By the real Stone–Weierstrass theorem and rational approximation of finitely many coefficients, a rational polynomial $p$ approximates a given $f\in C(K)$ to error below $\varepsilon/2$. Section 2 compiles $p$ into a strict $F$ term with constant 1, defined on all of $\mathbb R^n$. Replace every 1-leaf by $u_n$. A finite-tree induction proves eventual validity and uniform convergence on $K$: each original logarithm argument is continuous and positive on $K$, hence has a positive minimum; uniform perturbations preserve that minimum and continuity through the next node. Exponential and logarithm are uniformly continuous on the resulting compact ranges, with logarithm arguments bounded away from zero. For sufficiently large $n$, the perturbed term approximates $p$ to error below $\varepsilon/2$. Its natural domain is open and contains $K$.

Conversely, a composite finite tree has a deepest internal node whose right child is a leaf. Definedness throughout $K$ forces that fixed leaf to be positive everywhere on $K$. It must be a positive named constant or a uniformly positive coordinate. If neither exists, only leaves can be defined throughout $K$. All constant leaves are nonpositive, while the finitely many coordinate functions have bounded maxima. A sufficiently large positive constant function cannot be approximated by any leaf to error below 1. $\square$

Requiring approximation on **every** compact subset recovers the original positive-constant criterion: sufficiency follows above; necessity uses $K=\{0\}$. On a particular positive domain, no named constant is needed.

The quantifier order matters. The set $K=\{(1,-1),(-1,1)\}$ has a positive coordinate at each point but no single coordinate positive everywhere. With no positive named constant, no composite strict term is defined on all of this $K$. A rule that selects a different leaf at each input would change the language.

## Exact seeds: density and a dichotomy

Write

$$
\mathcal U=\{c>0:1\in\mathcal A(c)\}.
$$

By Proposition 1, these are precisely the positive seeds sufficient for exact exp-log arithmetic.

\Needspace{6\baselineskip}

**Theorem 6 (density of exact seeds).** The set $\mathcal U$ is dense in $(0,\infty)$.

*Proof.* Fix $0<a<b$ and a rational $r\in(a,b)$. Theorem 5, with no named constants and the positive coordinate $x$, gives a constant-free unary term $t$ uniformly approximating $h(x)=1+x-r$ on $[a,b]$ to error less than $\min(r-a,b-r)/2$. Its strict domain contains a neighborhood of $[a,b]$, so $t$ is continuous there and $t(a)<1<t(b)$. The intermediate value theorem supplies $c\in(a,b)$ with $t(c)=1$. Substituting the seed $c$ for its leaves gives an exact ground witness. $\square$

\Needspace{6\baselineskip}

**Theorem 7 (analytic exact-seed dichotomy).** The following are equivalent:

1. $\mathcal U=(0,\infty)$;
2. $\mathcal U$ is uncountable;
3. some constant-free unary strict $F$ term is identically 1 on a nonempty open interval.

Otherwise $\mathcal U$ is countably infinite and dense.

*Proof.* A unary strict term is real analytic on its open natural domain. Induct on syntax, using analyticity of exponential and of logarithm on positive inputs. An open subset of $\mathbb R$ has countably many connected components. On each component, the zeros of $t-1$ are isolated and countable unless it vanishes identically. Since there are countably many finite trees, uncountably many exact seeds force a local identity. This proves $2\Rightarrow3$.

If $t=1$ on an open interval $I$, every positive seed $c$ has a ground value in $I$ by Theorem 3. Substitute that ground term into $t$ to obtain 1 exactly. Thus $3\Rightarrow1$; $1\Rightarrow2$ is immediate. When no local identity exists, the countable union of zero sets is countable, and Theorem 6 makes it infinite and dense. $\square$

The dichotomy remains unresolved. It does not decide seed 2 or $e$, and it distinguishes $\forall c\,\exists t$ from one tree valid for every seed.

## Definable geometry of the seed space

The real exponential field supplies a sharper representation. Both a strict term's domain and its exact-one level set are definable: logarithm is the inverse relation $b>0\wedge\exp y=b$, and every node adds a strict domain condition. Wilkie's o-minimality theorem [12] says that a definable subset of the line is a finite union of points and intervals.

\Needspace{6\baselineskip}

**Corollary 8 (finite budgets and local exact complexity).** If the countable branch holds, every fixed unary tree has finitely many positive exact seeds, and so does every finite node budget. The exact seeds form a dense, null, meagre set; their minimum exact tree size, measured among exact seeds, is unbounded on every nondegenerate compact positive interval. If the universal branch holds, minimum exact tree size is locally bounded and a finite menu of exact trees covers every compact positive interval.

*Proof.* In the countable branch an exact-one level set contains no interval, so o-minimality makes it finite. There are finitely many unary trees below each node bound. Density then prevents a fixed budget from covering the exact seeds in any interval. Countability gives nullness and meagreness.

In the universal branch choose an identity term $t=1$ on an interval $I$. For each $c>0$, density supplies a unary tree $s$ with $s(c)\in I$. Openness of its domain and continuity give a neighborhood on which $s$ remains in $I$. The fixed composition $t\circ s$ is identically 1 there. A finite subcover gives a finite menu on a compact positive interval. $\square$

This gives a qualitative distinction in exact expression complexity. It supplies no effective zero-count algorithm or explicit global syntax bound.

\Needspace{6\baselineskip}

**Theorem 9 (finitely many named seeds).** For $k\ge1$, let

$$
P_k=\{z\in\mathbb R^k:\text{some }z_j>0\},\qquad
\mathcal U_k=\{z\in P_k:1\text{ is generated by the named entries of }z\}.
$$

Either $\mathcal U_k=P_k$ for every $k$, or, for every $k$, $\mathcal U_k$ is dense in $P_k$ but Lebesgue-null and meagre. In the latter case, each finite-budget subset is definable of dimension less than $k$.

*Proof.* If every positive single seed is exact, use any positive coordinate. Otherwise each fixed tree's exact-seed set is definable and has empty interior. If it contained an open box, the dense ground orbit of any single positive seed could provide one value in each coordinate interval; substitution into the tree would generate 1, contradicting the proper branch. Standard o-minimal dimension facts [16] make each such set null and its closure nowhere dense. A countable union gives nullness and meagreness; a finite union handles a fixed budget. Density follows by perturbing one positive coordinate into $\mathcal U$, leaving the others unchanged. Tuples with no positive coordinate cannot produce any defined non-leaf ground term. $\square$

These geometric consequences use classical o-minimality and dimension theory. They are ordinary proofs in this paper, outside the current Lean coverage.

## What bounded numerical search establishes

The inherited search retained all 23,714 ordered unary trees with at most ten $F$ nodes and sole leaf $z$. With seven probes, 100 decimal digits, and an absolute exponential-argument budget of 1,000, 944 trees completed every probe. None passed the retained constant-function test at tolerance $10^{-70}$.

This diagnostic does not decide the dichotomy or certify absence of a local identity within its node bound. Probe failures can miss a domain component, numerical equality cannot certify an analytic identity, and a resource stop is inconclusive. The contraction theorem supplies a stronger, properly scoped negative result for one infinite family: all its initialized finite iterates remain above 1.

# Constants in finite semiring languages

## Exact completeness and minimum constant budgets

Let $S$ be a finite nontrivial unital semiring with commutative addition, absorbing zero, and both distributive laws. Fix the total language $\{+,\times,0,1\}\cup C$. Completeness means expressing every map $S^r\to S$ for every $r\ge1$, including constant maps.

\Needspace{6\baselineskip}

**Theorem 10 (constant completion).** This language is complete if and only if

$$
S\cong M_d(\mathbb F_{p^k})
\quad\text{and}\quad
\mathbb F_p\langle C\rangle=S,
$$

where the latter denotes the unital algebra generated over the prime field.

*Proof.* With all constants available, the finite complete-semiring classification gives exactly the full matrix rings over finite fields [5, Theorem 32 and Corollary 34]. Completeness with $C$ implies that all-constants completeness. For each $a\in S$, a term for the constant unary map $a$, evaluated at $x=0$, gives a ground expression over $0,1,C$. In characteristic $p$, the ground subsemiring is the unital $\mathbb F_p$-algebra generated by $C$: additive inverses use $p-1$ copies. Conversely, matrix rings over finite fields are polynomially complete with all coefficients [5, Theorem 16]. Ground definitions for those coefficients remove the additional constants. $\square$

The classification is prior mathematics; the constant-policy reduction makes its synthesis consequence explicit. In particular, 0 and 1 are genuinely present. A general constant-free language cannot use the substitution argument to infer ground generation.

\Needspace{12\baselineskip}

The minimum number of additional named constants is therefore:

| Carrier | Minimum additional constants |
|:--|:--|
| Prime field $\mathbb F_p$ | 0 |
| Proper extension $\mathbb F_{p^k}$, $k>1$ | 1 |
| $M_d(\mathbb F_{p^k})$, $d\ge2$ | 2 |
| Any other finite nontrivial unital semiring | Impossible even with all constants |

Prime-field elements are numerals; one field generator suffices for a proper extension. A single matrix generates a commutative unital algebra, so cannot generate $M_d$ for $d\ge2$.

To attain two, choose a nonzero field generator $\alpha$ over $\mathbb F_p$ (take $\alpha=1$ if $k=1$), let $P e_j=e_{j+1\bmod d}$, and set $B=\alpha E_{00}$. With $q=p^k$,

$$
E_{00}=B^{q-1},\qquad E_{ij}=P^iE_{00}P^{-j},\qquad
\alpha I=\sum_iP^iBP^{-i}.
$$

Negative powers are replaced modulo $d$. These identities produce all matrix units and field scalars. The cyclic-permutation and matrix-unit construction is classical [6]. Encoding $\alpha$ in $B$ ensures generation over the prime field rather than silently granting extension scalars.

A shorter idempotent expression follows from the minimal polynomial
$m_\alpha(t)=t^k+c_{k-1}t^{k-1}+\cdots+c_1t+c_0$, with $c_0\ne0$:

$$
E_{00}=-c_0^{-1}(B^k+c_{k-1}B^{k-1}+\cdots+c_1B).
$$

The distinguished diagonal entry is 1 by $m_\alpha(\alpha)=0$; every other entry is zero. All coefficients are prime-field numerals. For $\mathbb F_4=\mathbb F_2[\alpha]/(\alpha^2+\alpha+1)$, this is $B^2+B$. The reduction concerns expanded trees; repeated squaring already makes the power witness logarithmic in $q$ as a shared graph.

## Generation certificates and the scalar-base error

Let $m=kd^2$ be the prime-field dimension. If $W_\ell$ spans all words of length at most $\ell$ in $C$, including $I$, then

$$
W_{\ell+1}=W_\ell+\sum_{a\in C}W_\ell a.
$$

Equality at one step means the space contains every word. Before equality, dimension strictly increases; hence $W_{m-1}$ decides generation. A queue needs at most $m$ independent words and $|C|m$ matrix products. Gaussian reduction uses $O(|C|m^3)$ prime-field operations, in addition to matrix-product costs.

A positive certificate lists $m$ independent word values. A negative certificate is a proper subspace containing $I,C$ and stable under right multiplication by every generator. It excludes every ground term outside that subspace, and thus the corresponding constant maps. This is an all-term obstruction with no arbitrary expression-size limit.

\Needspace{15\baselineskip}

A fresh exhaustive replay reproduces all six generator counts below, in agreement with established formulas [7, 9]. The computation uses exact Gaussian elimination over the declared scalar field.

| Ring | Scalar base supplied | Ordered pairs | Generating pairs |
|:--|:--|--:|--:|
| $M_2(\mathbb F_2)$ | $\mathbb F_2$ | 256 | 96 |
| $M_2(\mathbb F_3)$ | $\mathbb F_3$ | 6,561 | 3,888 |
| $M_2(\mathbb F_4)$ | $\mathbb F_2$ | 65,536 | 45,120 |
| $M_2(\mathbb F_4)$ | All $\mathbb F_4$ scalars | 65,536 | 46,080 |
| $M_2(\mathbb F_5)$ | $\mathbb F_5$ | 390,625 | 300,000 |
| $M_3(\mathbb F_2)$ | $\mathbb F_2$ | 262,144 | 129,024 |

For $M_2(\mathbb F_q)$ over its full scalar field, the published count is $q^5(q-1)(q^2-1)$ [7]. Change of base requires a further correction [9]. In $M_2(\mathbb F_4)$, checking span over $\mathbb F_4$ wrongly accepts 960 pairs for the language whose free scalars are only $\mathbb F_2$. Ten conjugate copies of $M_2(\mathbb F_2)$ contribute 96 such pairs each. For example, $P=\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)$ and $E_{00}$ generate only the 16-element prime-field subring. The carrier has 256 elements. This is a specification error, not a numerical tolerance issue.

## Exact optimization of two named constants

The finite cost experiment fixes $M_2(\mathbb F_2)$, zero-cost leaves $0,I$, exactly two additional zero-cost named values, and the lexicographic objective “minimum worst constant-expression cost, then minimum sum of the 16 costs.” All 256 ordered pairs were checked; 96 generate the ring. For each generating pair, the optimizer retains minimum costs and witness trees for every carrier element.

Bellman inequalities certify lower bounds by structural induction: a proposed cost must be no greater than each constructor weight plus the costs of its children. Matching witness trees certify attainability. A separate increasing-cost enumerator, using a distinct multiplication implementation, agrees on all 192 pair/profile cost vectors, comprising 3,072 individual values.

Let $E=E_{00}$. Replacing the canonical pair $(P,E)$ by $(P+E,E)$ improves both tested tree objectives:

| Cost convention | Canonical worst / sum | Improved worst / sum | Optimal generating pairs |
|:--|--:|--:|--:|
| Tree: $+$ weight 1, $\times$ weight 1 | 3 / 21 | 2 / 19 | 48 of 96 |
| Tree: $+$ weight 1, $\times$ weight 4 | 6 / 45 | 5 / 43 | 48 of 96 |
| Depth: both delays 1 | 2 / 19 | 2 / 19 | All 96 |
| Depth: delays 1 and 4 | 5 / 43 | 5 / 43 | All 96 |

The pairs can recover one another by one addition, so expressive power is unchanged. Shortest trees depend on which values are available as leaves. There is no improvement in the tested critical-path objectives and no measured runtime claim.

Within this exact census, the 48 tree-optimal pairs are precisely those containing a matrix with irreducible characteristic polynomial $t^2+t+1$. There are two such matrices. Each has centralizer $\mathbb F_4$ of size four; adjoining any of the other 12 matrices gives the full matrix ring. This yields $2\cdot12$ ordered pairs in either position, with no overlap because the two irreducible matrices commute. The cost-optimality characterization is a verified finite statement, not a classification for larger rings.

**Parametric refinement.** The same optimal pairs can be certified for an entire cone of real costs. Let addition cost $\alpha$ and multiplication cost $\beta$, with $\beta\ge\alpha>0$. Among the 96 generating pairs, the 48 containing an irreducible-characteristic-polynomial matrix have

$$
(\max_X c(X),\ \sum_X c(X))=(\alpha+\beta,\ 11\alpha+8\beta).
$$

The other 48 have $(2\alpha+\beta,13\alpha+8\beta)$. Thus precisely the former pairs minimize the lexicographic objective throughout this cone, including $\alpha=\beta$.

For each pair and value $X$, the certificate gives a witness with cost $p_X=u_X\alpha+v_X\beta$. Every Bellman inequality has slack $a\alpha+b\beta$ with $b\ge0$ and $a+b\ge0$, so

$$
a\alpha+b\beta=(a+b)\alpha+b(\beta-\alpha)\ge0.
$$

Structural induction gives a lower bound for every tree, and the retained witnesses attain it. The exact certificate checks all 49,152 constructor inequalities, the displayed sums, and attainable maxima. This proves a parameterized statement, rather than extrapolating from the two sampled weight profiles.

The cone assumption is necessary for this characterization. At $\alpha=2,\beta=1$, only 12 generating pairs attain the optimum $(3,25)$. The pair

$$
E_{00},\quad\begin{pmatrix}0&1\\1&1\end{pmatrix}
$$

contains an irreducible matrix but has objective $(3,26)$; replacing its second matrix by $\begin{pmatrix}1&1\\1&0\end{pmatrix}$ gives $(3,25)$. This exact counterexample is retained as a boundary on reusing the cost theorem.

For completeness, generation can be turned into explicit arbitrary-function interpolation. With matrix units available,

$$
L_{ij}(X)=\sum_sE_{si}XE_{js}=X_{ij}I,
\qquad
\delta_A(X)=\prod_{i,j}\left[I-(L_{ij}(X)-a_{ij}I)^{q-1}\right].
$$

The latter is $I$ when $X=A$ and zero otherwise. Consequently

$$
f(X_1,\ldots,X_r)=\sum_{A\in S^r}f(A)\prod_{j=1}^r\delta_{A_j}(X_j).
$$

This standard construction [5] explains sufficiency. Its truth-table sum has $|S|^r$ terms and supplies no efficient general synthesis algorithm.

# All-term certificates from preserved relations

## Certificate theorem for strict partial languages

Throughout this section, the language contains all finite compositional trees over its declared signature. Additional syntax-grammar restrictions need nonterminal-indexed closures. A closure for a larger unrestricted language remains sound for exclusion but its members need not satisfy a smaller grammar.

Let $A$ be a finite nonempty carrier, with partial primitive operations $f:A^k\rightharpoonup A$, named constants $C$, and a target $g:D\to A$ on $D\subseteq A^d$. Terms use strict evaluation. A proposed certificate consists of a relation $R\subseteq A^m$, $m\ge1$, and witness rows $w_1,\ldots,w_m\in D$.

\Needspace{6\baselineskip}

**Theorem 11 (relation obstruction).** No term implements $g$ on $D$ if all four conditions hold:

1. Every named constant diagonal $(c,\ldots,c)$ belongs to $R$.
2. Each primitive preserves $R$ on fully defined coordinate frames: applying it coordinatewise to argument columns in $R$ gives an output in $R$ whenever all coordinates are defined.
3. Each variable column $(w_{1j},\ldots,w_{mj})$ belongs to $R$.
4. The target column $(g(w_1),\ldots,g(w_m))$ does not belong to $R$.

*Proof.* Suppose a strict term implements $g$. At all witness rows it and every subterm are defined. Induct on the expression tree. Leaves give columns in $R$ by conditions 1 and 3. At an internal node, its child columns lie in $R$ and its primitive is defined in every coordinate, so condition 2 puts its output column in $R$. The root column must therefore lie in $R$, contradicting condition 4. $\square$

A frame with any undefined coordinate imposes no preservation obligation: that frame cannot occur at a node of a term defined on every witness row. Nullary primitives are handled as constant outputs. Shared finite graphs have the same expressive power as their unfolded trees. Lazy or short-circuit evaluation needs a separate semantic argument.

This is the classical functions-and-relations preservation principle, including partial-operation considerations in Geiger's treatment [8]. It is not a new algorithmic theorem. The useful implementation boundary is that a small independent checker can verify a candidate obstruction without trusting the process that proposed it.

Proving unrealizability for an entire synthesis grammar is also established research. Hu, Cyphert, D’Antoni, and Reps develop exact and abstract methods based on the possible outputs of grammar terms on examples [10]. Kim, Hu, D’Antoni, and Reps allow user-defined syntax and semantics and address both synthesis and unrealizability [11]. The present contribution is a small checked certificate format and a reviewed local integration for the declared Boolean profile; it does not introduce grammar-wide impossibility reasoning.

## Complete finite closure and reusable negative memory

For witness rows indexed by $I$, define the attainable column relation

$$
G_I=\{(t(w_i))_{i\in I}:t\text{ is defined at every witness row}\}.
$$

Call a relation *admissible* if it contains the variable columns and constant diagonals and is preserved by every fully defined primitive frame.

\Needspace{6\baselineskip}

**Theorem 12 (complete column certificate).** The relation $G_I$ is admissible and is contained in every admissible relation. A target column is unrealizable if and only if some admissible relation excludes it; $G_I$ itself is a complete choice.

*Proof.* Each leaf has its stipulated column. Given finitely many attainable child columns and a coordinatewise defined primitive application, compose their witnessing trees to obtain a tree for the output column. This proves admissibility of $G_I$. Structural induction puts every attainable column in every other admissible relation. Exclusion follows from Theorem 11; conversely, an unattainable target is excluded by $G_I$. $\square$

For finite $A$, finite $I$, and a finite explicitly tabulated primitive signature, saturation from the leaves adds at most $|A|^{|I|}$ distinct columns. Store a derivation for each addition. Once closure is reached, membership gives a term and absence gives a relation certificate. If the witness rows cover all of $D$, this decides realizability on $D$. A proper batch decides only that batch: absence still excludes the full target, while membership need not implement it elsewhere. Exhausting a work budget before closure is inconclusive.

This makes the information order on negative memory precise. An admissible $R$ excludes $A^I\setminus R$; a smaller relation excludes more columns. The canonical $G_I$ is therefore the strongest admissible memory for the fixed batch. Intersections combine memories:

$$
R,S\text{ admissible}\Longrightarrow R\cap S\text{ admissible},\qquad
A^I\setminus(R\cap S)=(A^I\setminus R)\cup(A^I\setminus S).
$$

This is an order on semantic exclusion power. It does not imply that storing or computing the smallest relation is cheapest. Every retained exclusion remains bound to its operation tables, constants, witness rows, and evaluation semantics. Search failures without those conditions remain observations rather than pruning rules.

## Transport between representations

\Needspace{6\baselineskip}

**Theorem 13 (forward transport of exclusion).** Let $A$ and $B$ interpret the same signature and let $h:A\to B$. Assume that $h$ maps every named constant to its $B$ interpretation and, whenever

$$
f_A(a_1,\ldots,a_k)=a
$$

is defined, $f_B(h(a_1),\ldots,h(a_k))$ is defined and equals $h(a)$. Then every defined source term transports through $h$. Any relation certificate in $B$ excluding the row-indexed target column $(h(g(w_i)))_i$, on input columns $(h(w_{ij}))_i$, excludes the source target in $A$.

*Proof.* Induct on source evaluation. The leaf cases use the constant and input conditions. At each internal node, the induction hypothesis supplies the abstract child values; the primitive hypothesis supplies definedness and the correct abstract result. Apply Theorem 11 in $B$. $\square$

The row-indexed formulation does not require $h\circ g$ to descend to a well-defined function on $h(D)$. The map need not be injective for sound exclusion. Loss of information may make some certificates unavailable. A bijection with operation and domain correspondence in both directions preserves realizability in both directions. A forward map alone does not transport a synthesized solution back.

Agreement merely *when both sides are defined* is insufficient: it would permit deleting abstract operation-table entries and creating false exclusions. Language extensions also require a fresh preservation check; a previously certified relation may fail a newly added operation. Language restrictions retain valid exclusions.

## Four rows separate every nonaffine Boolean target

XOR, NOT, and constants 0 and 1 generate exactly the affine Boolean maps. They express every unary Boolean map but exclude binary AND.

\Needspace{6\baselineskip}

**Theorem 14 (optimal affine separation).** Every nonaffine $g:\mathbb F_2^n\to\mathbb F_2$ has a four-row relation certificate for this grammar, using

$$
R_4=\{u\in\mathbb F_2^4:u_1\oplus u_2\oplus u_3\oplus u_4=0\}.
$$

No certificate with at most three coordinates excludes any Boolean target from the affine grammar.

*Proof.* If $g(0)\oplus g(x)\oplus g(y)\oplus g(x\oplus y)=0$ for all $x,y$, then $g(x)\oplus g(0)$ is additive and hence linear over $\mathbb F_2$. For nonaffine $g$, choose a violating pair and rows $(0,x,y,x\oplus y)$. Every variable column and constant diagonal has even parity, while the target column has odd parity. XOR and NOT preserve $R_4$. A repeated row would cancel in pairs, so the four rows are distinct.

For the lower bound, a relation containing zero and closed under XOR is a linear subspace. Inclusion of the all-one column forces each orthogonal constraint to have even Hamming weight. In at most three coordinates, every nonzero such constraint has weight two and equates two coordinates. Coordinate-equality relations are preserved by every Boolean operation; they cannot separate the target. $\square$

For AND, rows $00,01,10,11$ give input columns $0011,0101\in R_4$ and output $0001\notin R_4$. The eight-member relation uses $8^2+8=72$ XOR/NOT preservation frames and 288 coordinate lookups. The four-row result is the classical affine parallelogram criterion expressed as a certificate statement.

The number of reusable relations also has an exact description. Relations preserved by XOR and NOT and containing both diagonals are subspaces containing the all-one vector, in bijection with subspaces of $\mathbb F_2^{m-1}$. Those also preserved by AND are Boolean subalgebras of $\mathbb F_2^m$; their atoms partition the coordinates. Consequently the number failing AND preservation is

$$
\sum_{j=0}^{m-1}{m-1\brack j}_2-B_m,
$$

where the bracket is a Gaussian binomial coefficient and $B_m$ is the Bell number.

| Relation arity $m$ | Affine-grammar invariants | Also preserve AND | Fail AND preservation |
|---:|---:|---:|---:|
| 1 | 1 | 1 | 0 |
| 2 | 2 | 2 | 0 |
| 3 | 5 | 5 | 0 |
| 4 | 16 | 15 | 1 |
| 5 | 67 | 52 | 15 |
| 6 | 374 | 203 | 171 |
| 7 | 2,825 | 877 | 1,948 |

A fresh exact enumeration reproduces these counts. These are reusable relation counts; a particular exclusion also needs suitable witness rows.

The revised finite experiment checks all Boolean targets through four inputs. It verifies four-row witnesses for every one of the 65,752 nonaffine targets across two, three, and four inputs. A separate complete census tests all 81 partial binary Boolean operations with four constant policies: 324 profiles and 5,184 targets, of which 1,404 have checked realizing trees and 3,780 have checked closed-relation exclusions. These computations illustrate the generic theorem; they do not establish a runtime-adapter refinement.

## The semantic bridge is a proof obligation

A correct finite-table certificate can still be misapplied to a richer runtime. Consider integer successor and negation with target inputs $\{0,1\}$. The expression $\operatorname{succ}(-x)=1-x$ implements Boolean NOT, but uses the intermediate value $-1$. If both operations are truncated to the carrier $\{0,1\}$, their partial tables preserve the order relation $\{00,01,11\}$, which excludes NOT. The exclusion is correct for the truncated language and false for the integer language.

Finite input domains therefore do not justify finite intermediate carriers. An adapter must establish an exact closed carrier or a sound overapproximation of the actual term language. Adding constants or operations makes the abstract language larger; an exclusion for that larger language is safe for the original only when every original term is represented by the abstraction.

The inherited software audit exercised the generic checker on ten impossibility tasks and three positive controls, with 499 retained semantic and budget mutation entries, ten malformed cases, eight input-cap checks, and a mutable-alias regression. It rejected 428 stale model bindings. A separate table-oriented reference checker agreed on the retained certificate results. These are software checks and finite experiments; they do not replace the theorem or prove arbitrary runtime correspondence.

# Executed experiments and runtime boundaries

The exact finite study uses complete enumerations on declared carriers. The arithmetic evaluator uses high precision only as a diagnostic for emitted syntax. The distinction is material: symbolic algebra and Lean prove universal identities; finite numerical agreement checks whether the retained syntax behaves as expected at the selected inputs.

| Fresh replay | Scope | Result |
|---|---|---|
| Compact arithmetic | 50 valid inputs for each of raw and simplified constructions, 300 decimal digits | 100 agreements at normalized tolerance $10^{-70}$ |
| Matrix generation | All ordered pairs in the six scalar-field profiles of Section 4 | All six generator counts reproduced by exact elimination |
| Matrix generator/cost census | All 256 ordered pairs in $M_2(\mathbb F_2)$, four cost profiles | 96 generating pairs; tree/depth objectives reproduced |
| Parametric matrix cost certificate | All 96 generating pairs, all 16 values, both constructors | 49,152 symbolic Bellman inequalities valid for $\beta\ge\alpha>0$ |
| Affine Boolean separation | Every Boolean function through four inputs | Four-row certificates for all 65,752 nonaffine targets |
| Partial Boolean languages | 81 partial binary operations, four constant policies, 16 binary targets | 1,404 realizing trees and 3,780 closed-relation exclusions |
| Reusable relation census | Arities 1 through 7 | Subspace/partition counts agree with the formula in Section 5 |

The parametric certificate is checked twice. Its producer retains witness trees and coefficient pairs. A separate read-only checker recomputes matrix products, ground closure, witness costs, and every coefficient inequality. The general Bellman theorem is Lean-checked; the specific matrix tables are exact executable evidence. This combination establishes an ordinary theorem with a finite auditable certificate, without claiming that all tables were imported into Lean.

The original draft also described an opt-in Boolean preflight integrated with a native synthesis runtime. Its retained local records report 54 all-term exclusions among 128 core cases, with no false exclusions in that census; ten additional native misses remained bounded-search outcomes. Those historical records illustrate a possible application but are outside the fresh runtime validation of this revision. The original adapter's correspondence was manually reviewed, not formally proved.

The unsafe-carrier example in Section 5 remains a mandatory design constraint. A finite input domain does not bound intermediates. An abstract relation may authorize pruning only after the actual source language is shown to map into the abstract interpretation with definedness preserved. Rejected certificates, unsupported operations, and exhausted checking budgets must remain inconclusive.

# Interpretation and open questions

Several representations answer different questions about the same syntax. The four-node context is a finite tree, an economical shared program, and a real dynamical system with a positive attractor. Its exact rational correction exposes the domain and convergence proof. The seed parameter space is analytic and definable, allowing zero-set and dimension arguments. Finite evaluation columns turn an unbounded family of trees into a finite algebraic closure, while relation transport states when an exclusion survives a change of carrier.

These views preserve different information. Closing a scalar orbit forgets exact finite expressibility. Sharing preserves values and strict definedness while changing syntax cost. A noninjective semantic map can preserve sound exclusion but lose opportunities to separate targets. Negative memory is strongest when its scope and preserved information are explicit: the canonical column relation is maximal in exclusion power for a fixed batch, while a certified family such as the initialized attractor can be rejected for exact-1 search without rejecting its approximation role.

The central unresolved question is whether any constant-free strict EML term is identically 1 on an open interval. A positive answer makes every positive seed exact and gives locally bounded exact expression complexity. A negative answer makes exact seeds countably dense with finite support at every finite tree budget. Neither the contraction nor the numerical searches decide seed 2.

Other questions now have sharper boundaries. The compact-approximation theorem is existential beyond its constant bootstrap; it gives no useful general polynomial or numerical-conditioning bound. The arithmetic sizes are upper bounds without lower-bound optimality. The matrix cost theorem is exact on its declared weight cone and carrier, with an explicit counterexample outside that cone. Extending relation certificates to a richer runtime requires a new definedness-preserving semantic bridge; the abstract theorem supplies no such bridge automatically.

\clearpage

# Formalization and reproducibility

## Lean coverage

The proof development uses Lean 4.24.0 and Mathlib 4.24.0 (revision `f897ebcf72cd`; full pin in the supplement). Strict validity is a recursive predicate: children must be valid and every right child must have positive value. Value functions may use Mathlib's total real logarithm internally, but mathematical conclusions about terms carry the strict-validity predicate. This prevents a totalized logarithm from silently changing the paper's language.

\begingroup
\small

| Result | Executed formal coverage |
|---|---|
| Arithmetic and compilation | `Arithmetic`, `Compiler`: exact values, natural domains, and 57/14/128/299 node counts |
| Positive-seed density | `Density`, `ExactSeeds`: strict syntax, contraction, geometric rate, dense ground orbits |
| Dense exact seeds | `DenseExactSeeds`: an exact witness in every positive interval and $\overline{\mathcal U}=[0,\infty)$ |
| Analytic dichotomy | `ExactSeeds`: all-positive-or-countable; equivalence with a local interval identity |
| Compact approximation | `PolynomialApproximation`, `Approximation`, `FiniteApproximation`: Stone–Weierstrass, rational compilation, declared finite variables and an open valid neighborhood |
| Replacement stability | `ParameterStability`, `CompactTransfer`: uniform value/domain stability and actual substitution |
| Domain obstructions | `NonpositiveObstruction`, `DomainWitness`: origin obstruction and one fixed positive leaf; `Density`: no initialized finite iterate equals 1 |
| Relational certificates | `RelationCertificates`: scalar/column semantics, least closure, complete exclusion, intersection and definedness-preserving transport |
| General cost bounds | `RelationCertificates`: Bellman lower bounds and attaining-witness optimality |

\endgroup

The displayed axioms are limited to Lean's standard `propext`, `Classical.choice`, and `Quot.sound`; some structural and size results use none. The sources contain no admitted proofs or custom axioms. The packet retains source hashes, compiler output, and axiom reports.

The global-basin part of Theorem 2 below 1, the local derivative, the constant-free positive-coordinate sufficiency direction of Theorem 5, o-minimal results, finite-semiring classification, and specialized finite cost tables have ordinary proofs or executed finite certificates as indicated. They are not collectively described as Lean-verified. Nor does the development verify the Python evaluator, table checker, or a native runtime adapter. The positive-named-constant approximation direction is fully formalized, including polynomial approximation.

## Evidence and replay

The supplement contains the manuscript sources and vector figure, self-contained Lean project metadata, exact finite replay programs and witnesses, a source ledger, and a separate negative-memory ledger. Its manifest records file hashes and sizes. A clean Lean build is the proof replay; finite Python replays independently validate the empirical tables and symbolic cost certificate.

Representative commands from the supplement root are:

```sh
cd lean
lake exe cache get
lake build
cd ..
python3 experiments/finite/replay.py
python3 experiments/finite/parametric_cost.py
python3 experiments/finite/check_parametric_certificate.py
python3 experiments/finite/run_pair_census.py
python3 experiments/analytic/compact_construction.py
```

Lean dependencies are pinned, and the delivered build receipt records the executed local environment. Initial dependency installation requires network access. Python finite checks use the standard library; the six-profile matrix census additionally requires a C11 compiler. Analytic numerical diagnostics use `mpmath==1.3.0`. The figure additionally uses Matplotlib. Numerical checks are not used as theorem proofs.

The inherited continuation archive was checked against all 578 manifest entries before use, with no mismatches. The revised study freshly replays the compact arithmetic syntax checks and matrix cost results, and adds the finite certificate and parametric-cost experiments. Earlier native integration remains historical evidence with its own source bindings; it is not re-certified by the Lean mathematics. Private research identifiers are omitted from the publication manuscript.

## Acknowledgements

AI research assistance supported derivation, source inspection, formalization, implementation, and drafting. Separate review passes examined the ordinary arguments and independent finite implementations. This does not imply external peer review or endorsement by the cited authors.

# References

\begingroup
\small
\raggedright
\interlinepenalty=10000

1. A. Odrzywołek. *All elementary functions from a single binary operator*. arXiv:2603.21852v2, 2026. Main text and supplementary information. <https://arxiv.org/html/2603.21852v2>; <https://arxiv.org/src/2603.21852v2/anc/SupplementaryInformation.pdf>.

2. B. Naskręcki and contributors. *EML formalization*, public source repository. Inspected revision `d7d041df73e14da6ff5db889015d6e6b89615982`, especially arithmetic, unconditional-domain, and alternative-witness source files. Source inspected; no local Lean build claimed. <https://github.com/nasqret/eml-formalization>.

3. M. Carney. *Inexpressibility in Exp-Minus-Log*. arXiv:2605.01636v1, 2026. <https://arxiv.org/html/2605.01636v1>.

4. V. Kreinovich, L. Valera, I. Atamanyuk, and Y. Kondratenko. “Why Exp-Minus-Log (eml): Towards an Explanation Based on Optimization and Symmetry.” *Mathematics* 14(22), 4170, 2026. <https://www.mdpi.com/2227-7390/14/22/4170>.

5. G. Horváth. *Functions and Polynomials over Finite Groups from the Computational Perspective*. PhD thesis, University of Hertfordshire, 2008. Theorem 16, Theorem 32, and Corollary 34. <https://uhra.herts.ac.uk/id/eprint/16291/1/GaborHorvathPhD.pdf>.

6. B. V. Petrenko and S. N. Sidki. “On pairs of matrices generating matrix rings and their presentations.” *Journal of Algebra* 310 (2007), 15–40. Inspected arXiv:math/0512186v2, Sections 1.1–1.2. <https://arxiv.org/pdf/math/0512186v2>.

7. R. V. Kravchenko, M. Mazur, and B. V. Petrenko. “On the smallest number of generators and the probability of generating an algebra.” *Algebra & Number Theory* **6**(2) (2012), 243–291. Inspected arXiv:1001.2873v2, especially equation (9). <https://arxiv.org/pdf/1001.2873v2>.

8. D. Geiger. “Closed systems of functions and predicates.” *Pacific Journal of Mathematics* 27(1) (1968), 95–100. <https://msp.org/pjm/1968/27-1/pjm-v27-n1-p08-s.pdf>.

9. R. V. Kravchenko, M. Mazur, and B. V. Petrenko. “Generators of maximal orders.” *Journal of Algebra* **426** (2015), 32–50. DOI: 10.1016/j.jalgebra.2014.11.020. Inspected preprint arXiv:1406.6465v1. Theorems 3.2 and 3.4 and Proposition 3.3. <https://arxiv.org/pdf/1406.6465v1>.

10. Q. Hu, J. Cyphert, L. D’Antoni, and T. Reps. “Exact and Approximate Methods for Proving Unrealizability of Syntax-Guided Synthesis Problems.” *Proceedings of PLDI 2020*, 1128–1142. DOI: 10.1145/3385412.3385979. <https://cseweb.ucsd.edu/~ldantoni/papers/pldi20unrealizability.pdf>.

11. J. Kim, Q. Hu, L. D’Antoni, and T. Reps. “Semantics-Guided Synthesis.” *Proceedings of the ACM on Programming Languages* 5, POPL, Article 30 (2021), 32 pages. DOI: 10.1145/3434311. <https://cseweb.ucsd.edu/~ldantoni/papers/popl21.pdf>.


12. A. J. Wilkie. “Model completeness results for expansions of the ordered field of real numbers by restricted Pfaffian functions and the exponential function.” *Journal of the American Mathematical Society* **9**(4) (1996), 1051–1094. DOI: 10.1090/S0894-0347-96-00216-0. See also the author's “O-Minimality,” *Documenta Mathematica*, Extra Volume ICM 1998, vol. I, 633–636. <https://ems.press/content/book-chapter-files/27125?nt=1>.

13. T. Stachowiak. *Algebraic structure behind Odrzywołek's EML operator*. arXiv:2604.23893v1, 2026. <https://arxiv.org/html/2604.23893v1>.

14. A. Odrzywołek. *Diversity of EML-type operators*. arXiv:2609.11210v1, 2026. <https://arxiv.org/html/2609.11210v1>.

15. J. Germany, E. Abdo, and J. Bakarji. *EML Trees Are Universal Approximators*. arXiv:2606.23179v1, 2026. <https://arxiv.org/html/2606.23179v1>.

16. L. van den Dries. *Tame Topology and O-minimal Structures*. London Mathematical Society Lecture Note Series 248. Cambridge University Press, 1998. DOI: 10.1017/CBO9780511525919.

\endgroup
