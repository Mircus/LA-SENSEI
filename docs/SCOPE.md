# Scope, mathematical assumptions, and limitations

**Version:** 0.1.0, aligned to the October 2026 booklet manuscript.

- **Finite fields:** `Field(p, modulus)` uses base-`p` integer encodings for coefficients of `1, α, ...`. Coefficients of the modulus are in ascending order. The constructor checks irreducibility by exhaustive trial divisors, intended for small fields only. The library has **no cryptographic, performance, or constant-time guarantees**.
- **Vectors:** use column vectors. Python lists of rows represent matrices. Matrix columns are images of basis vectors.
- **Polynomial coefficients:** always in ascending order, e.g. `[1,1,1]` is `1+x+x²`.
- **Hamming indexing:** the book and CLI use **1-based** bit positions; Python containers index from zero. H columns appear in the exact Chapter 13 order. Decoder corrects **one** error, and may *miscorrect* a two-bit error.
- **Smith form:** `smith_2x2_full_rank` computes invariants using gcd of minors for **nonsingular 2×2 integer matrices only**. It is not a general-purpose Smith normal form implementation.
- **Operators:** exact matrix arithmetic in finite fields; numerical norms for a specific real 2×2 Jordan-type family only. Do not extrapolate numerical conditioning results to finite fields.
- **Tensors:** demonstrations compute Plücker coordinates and flattening lower bounds. They **do not algorithmically certify general tensor rank**; especially, W-flattening rank 2 is insufficient to prove tensor rank 3.
- **Lie / Clifford:** small exact demonstrations are examples rather than full packages for representation theory or Clifford classification.
- **Exercise tracking:** every numbered chapter exercise in the supplied source is indexed. Pure proofs remain reader exercises. Some computational demos illustrate special cases, not the universal theorem.
- **Book edition:** if the LaTeX manuscript changes, confirm exercise IDs and statements before tagging a release; `exercises/index.json` is a snapshot, not a dynamic source of truth.

## Tests versus theorems

Tests make implementation regressions visible and check many finite cases. They cannot establish universal mathematical claims. The notebook prompts explicitly request explanations of hypotheses and statements independent of computation.

## Optional notebook dependencies

Core package and CLI work with only Python. Notebooks use core code plus the `lab` extra for plotting and additional experiments; a separate SageMath installation is **not required** in this version. SageMath would be appropriate for a later advanced chapter on general modules, polynomial factorization and representation theory.
