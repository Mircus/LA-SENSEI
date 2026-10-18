"""Integer invariants: small illustrative Smith calculations and rank jumps."""
from math import gcd
from functools import reduce
from .finite import Field
from .linear import rank


def smith_2x2_full_rank(a):
    """Smith diagonal d1|d2 for a nonsingular integer 2x2 matrix.

    Intentionally NOT a general Smith algorithm: uses gcd of 1x1 and 2x2 minors.
    """
    if len(a) != 2 or any(len(row) != 2 for row in a):
        raise ValueError('2x2 only')
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if det == 0:
        raise ValueError('full-rank integer matrix required')
    d1 = reduce(gcd, (abs(x) for row in a for x in row))
    d2 = abs(det) // d1
    return (d1, d2)


def rank_mod(a, p):
    return rank([[x % p for x in row] for row in a], Field(p))


def circle_boundary(n):
    """Signed boundary C1 -> C0 for n cyclically oriented edges."""
    if n < 3:
        raise ValueError('a simplicial cycle requires >=3 vertices')
    d = [[0] * n for _ in range(n)]
    for edge in range(n):
        d[edge][edge] -= 1
        d[(edge + 1) % n][edge] += 1
    return d
