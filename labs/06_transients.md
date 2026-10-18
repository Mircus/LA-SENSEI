# Laboratory VI — Eigenvalues miss instability

**Book correspondence:** Extended Laboratory VI, Chapter 13 numerical dialect.

Over the reals, $T=\begin{pmatrix}a&M\\0&a\end{pmatrix}$ for $0<a<1$. Both eigenvalues decay as $a^n$, yet $T^n$ contains the term $nMa^{n-1}$, which can become large before ultimately decaying. The notebook graphs the norm $\|T^n\|_2$.

```bash
la-sensei lab transients
```

Notebook: [`06_transients.ipynb`](../notebooks/06_transients.ipynb).

**Investigate.** Fix $a=0.8$ and compare $M=1,10,30,100$. Is the peak bounded by eigenvalues alone? Distinguish spectral radius from operator norm and explain why there is no direct analogue of Euclidean transient growth for the finite-state $\mathbb F_2$ example.
