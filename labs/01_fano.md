# Laboratory I — Seven points that make a universe

**Book correspondence:** Extended Laboratory I; E01.04, E13.02, E14.05.

Start with the seven nonzero vectors of $\mathbb{F}_2^3$. In characteristic two, the unique third point on the projective line through $u$ and $v$ is $u+v$. The program enumerates seven projective lines, checks 21 point-line incidences, and confirms that exactly seven nonzero Hamming codewords have weight three.

```bash
la-sensei lab fano
la-sensei chapter 1
```

Notebook: [`01_fano.ipynb`](../notebooks/01_fano.ipynb).

**Investigate.** Verify that each unordered pair of points belongs to one line. Interpret a triple summing to zero both as a Fano line and as a codeword. Then prove why the same dependence pattern cannot be represented in odd characteristic; the determinant obstruction is $-2$, not a failure of a plotting library.

**Do not confuse:** projective lines are *incidence structures*; one is drawn as a circle for visibility.
