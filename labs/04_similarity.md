# Laboratory IV — A hidden similarity test

**Book correspondence:** Extended Laboratory IV; E03.01, E04.01, E04.03.

Over $\mathbb F_2$, take $p=x^2+x+1$, $A=C(p)\oplus C(p)$ and $B=C(p^2)$. Both have characteristic polynomial $p^2$. But $m_A=p$, $m_B=p^2$, so they are not similar. The rank of $p(A)$ is 0, while that of $p(B)$ is 2.

```bash
la-sensei lab similarity
```

Notebook: [`04_similarity.ipynb`](../notebooks/04_similarity.ipynb).

**Investigate.** Why does the characteristic polynomial fail to classify similarity? Infer block sizes from the sequence $\dim\ker p(T)^k$. Distinguish primary cyclic summands from arbitrary eigenvector lists.
