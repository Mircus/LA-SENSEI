"""Boolean, min-plus and max-plus multiplication: same syntax, new operations."""
from math import inf


def semiring_product(a, b, *, mode):
    if mode not in ('boolean', 'minplus', 'maxplus'):
        raise ValueError('unsupported semiring')
    if not a or not b or len(a[0]) != len(b):
        raise ValueError('incompatible dimensions')
    if mode == 'boolean':
        return [[int(any(bool(a[i][k]) and bool(b[k][j])
                         for k in range(len(b)))) for j in range(len(b[0]))]
                for i in range(len(a))]
    combine = min if mode == 'minplus' else max
    return [[combine(a[i][k] + b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def maxplus_mv(a, x):
    return [max(y + xj for y, xj in zip(row, x)) for row in a]


def floyd_warshall(weights):
    """Min-plus closure; reject negative cycles (distances undefined)."""
    n = len(weights)
    if any(len(row) != n for row in weights):
        raise ValueError('square required')
    d = [row[:] for row in weights]
    for i in range(n):
        d[i][i] = min(d[i][i], 0)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    if any(d[i][i] < 0 for i in range(n)):
        raise ValueError('negative cycle: no finite shortest path')
    return d
