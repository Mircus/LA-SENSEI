"""Exterior powers, Plücker relation and the W-tensor flattenings."""
from math import comb
from .finite import Field
from .linear import determinant, rank


def exterior_dimensions(n):
    return tuple(comb(n, k) for k in range(n + 1))


def plucker_coordinates(u, v, f: Field):
    if len(u) != 4 or len(v) != 4:
        raise ValueError('vectors in F^4 required')
    return {(i + 1, j + 1): f.sub(f.mul(u[i], v[j]), f.mul(u[j], v[i]))
            for i in range(4) for j in range(i + 1, 4)}


def plucker_relation(p, f: Field):
    return f.add(f.sub(f.mul(p[1, 2], p[3, 4]), f.mul(p[1, 3], p[2, 4])),
                 f.mul(p[1, 4], p[2, 3]))


def w_tensor():
    return [[[int((i, j, k) in ((1, 0, 0), (0, 1, 0), (0, 0, 1)))
              for k in range(2)] for j in range(2)] for i in range(2)]


def w_flattenings():
    W = w_tensor()
    f = Field(3)
    matrices = [
        [[W[i][j][k] for j in range(2) for k in range(2)] for i in range(2)],
        [[W[i][j][k] for i in range(2) for k in range(2)] for j in range(2)],
        [[W[i][j][k] for i in range(2) for j in range(2)] for k in range(2)],
    ]
    return tuple(rank(m, f) for m in matrices)
