# Laboratory III — Decode a damaged seven-bit message

**Book correspondence:** Extended Laboratory III; E13.01–E13.02, E01.04.

The parity-check matrix is precisely the Chapter 13 $H$, whose first three columns are $I_3$. Encode $(c_4,c_5,c_6,c_7)=(1,0,1,1)$, flip bit six, calculate the syndrome, and recover the message.

```bash
la-sensei lab hamming
```

Notebook: [`03_hamming.ipynb`](../notebooks/03_hamming.ipynb).

**Investigate.** Exhaust all 16 legal codewords and prove the minimum distance is 3. Flip two bits in one word and observe how the single-error decoder can *miscorrect* rather than reject. State the theorem's correction radius.
