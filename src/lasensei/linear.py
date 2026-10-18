"""Gaussian elimination and operator calculations over arbitrary finite fields."""

from .finite import Field


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def zero(m, n):
    return [[0] * n for _ in range(m)]


def add(a, b, f: Field):
    return [[f.add(x, y) for x, y in zip(row, b[i])] for i, row in enumerate(a)]


def scale(a, c, f: Field):
    return [[f.mul(c, x) for x in row] for row in a]


def mul(a, b, f: Field):
    if not a or not b or len(a[0]) != len(b):
        raise ValueError('incompatible matrix dimensions')
    return [[_dot(row, col, f) for col in zip(*b)] for row in a]


def _dot(row, col, f):
    v = 0
    for a, b in zip(row, col):
        v = f.add(v, f.mul(a, b))
    return v


def vec(a, v, f: Field):
    if any(len(row) != len(v) for row in a):
        raise ValueError('incompatible matrix/vector dimensions')
    return [_dot(row, v, f) for row in a]


def power(a, k, f: Field):
    if k < 0 or len(a) != len(a[0]):
        raise ValueError('requires square matrix, nonnegative power')
    result = eye(len(a))
    while k:
        if k & 1:
            result = mul(result, a, f)
        a = mul(a, a, f)
        k >>= 1
    return result


def rref(a, f: Field):
    if not a:
        return [], []
    b = [row[:] for row in a]
    if any(len(row) != len(b[0]) for row in b):
        raise ValueError('ragged matrix')
    m, n, pivots = len(b), len(b[0]), []
    row = 0
    for col in range(n):
        pivot = next((j for j in range(row, m) if b[j][col]), None)
        if pivot is None:
            continue
        b[row], b[pivot] = b[pivot], b[row]
        inv = f.inv(b[row][col])
        b[row] = [f.mul(inv, x) for x in b[row]]
        for j in range(m):
            if j != row and b[j][col]:
                c = b[j][col]
                b[j] = [f.sub(x, f.mul(c, y)) for x, y in zip(b[j], b[row])]
        pivots.append(col)
        row += 1
        if row == m:
            break
    return b, pivots


def rank(a, f: Field):
    return len(rref(a, f)[1])


def nullspace(a, f: Field):
    if not a:
        raise ValueError('pass at least one row')
    b, pivots = rref(a, f)
    n = len(b[0])
    basis = []
    for free in range(n):
        if free not in pivots:
            v = [0] * n
            v[free] = 1
            for row, col in enumerate(pivots):
                v[col] = f.neg(b[row][free])
            basis.append(v)
    return basis


def solve(a, b, f: Field):
    """Return one solution of A*x=b or None if inconsistent."""
    if len(a) != len(b):
        raise ValueError('incompatible system')
    if not a:
        return []
    n = len(a[0])
    reduced, pivots = rref([row[:] + [rhs] for row, rhs in zip(a, b)], f)
    if n in pivots:
        return None
    solution = [0] * n
    for i, pivot in enumerate(pivots):
        solution[pivot] = reduced[i][n]
    return solution


def determinant(a, f: Field):
    if not a or len(a) != len(a[0]):
        raise ValueError('square nonempty matrix required')
    n = len(a)
    b = [row[:] for row in a]
    d = 1
    for col in range(n):
        j = next((i for i in range(col, n) if b[i][col]), None)
        if j is None:
            return 0
        if j != col:
            b[j], b[col] = b[col], b[j]
            d = f.neg(d)
        pivot = b[col][col]
        d = f.mul(d, pivot)
        for i in range(col + 1, n):
            factor = f.div(b[i][col], pivot)
            for k in range(col, n):
                b[i][k] = f.sub(b[i][k], f.mul(factor, b[col][k]))
    return d


def poly_eval_matrix(coefficients, a, f: Field):
    """Ascending coefficients: c_0 I + c_1 A + ..."""
    n = len(a)
    result = zero(n, n)
    for c in reversed(coefficients):
        result = add(mul(result, a, f), scale(eye(n), c, f), f)
    return result


def companion(coefficients, f: Field):
    """Multiplication-by-x matrix for a monic polynomial (ascending coefficients)."""
    if coefficients[-1] != 1:
        raise ValueError('monic polynomial required')
    n = len(coefficients) - 1
    a = zero(n, n)
    for j in range(n - 1):
        a[j + 1][j] = 1
    for i in range(n):
        a[i][-1] = f.neg(coefficients[i])
    return a


def minimal_polynomial(a, f: Field):
    """Exact linear-dependence algorithm, appropriate for small matrices."""
    n = len(a)
    powers = [eye(n)]
    for degree in range(1, n + 1):
        current = mul(powers[-1], a, f)
        previous = [[p[i][j] for p in powers] for i in range(n) for j in range(n)]
        rhs = [f.neg(current[i][j]) for i in range(n) for j in range(n)]
        coeff = solve(previous, rhs, f)
        if coeff is not None:
            return coeff + [1]
        powers.append(current)
    raise AssertionError('Cayley–Hamilton guarantees a dependence')


def all_gl2(f: Field):
    from itertools import product
    return [a for values in product(range(f.order), repeat=4)
            if determinant((a := [list(values[:2]), list(values[2:])]), f) != 0]
