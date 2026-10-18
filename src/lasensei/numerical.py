"""The book's nonnormal example, without assuming spectral radius controls transients."""
import math


def jordan_power(a, coupling, n):
    if not 0 <= a < 1 or n < 0:
        raise ValueError('expected 0 <= a < 1 and n >= 0')
    if n == 0:
        return ((1, 0), (0, 1))
    return ((a ** n, n * coupling * a ** (n - 1)), (0.0, a ** n))


def norm2(matrix):
    """Exact formula for spectral norm of a 2x2 real matrix, up to FP arithmetic."""
    a, b = matrix[0]
    c, d = matrix[1]
    trace = a*a + b*b + c*c + d*d
    detsq = (a*d - b*c) ** 2
    return math.sqrt((trace + math.sqrt(max(0.0, trace*trace - 4*detsq))) / 2)


def transient_profile(a=0.8, coupling=30.0, steps=60):
    return tuple((n, norm2(jordan_power(a, coupling, n))) for n in range(steps + 1))
