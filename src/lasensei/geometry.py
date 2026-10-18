"""Fano incidence, the Hamming [7,4,3] code, and Reed–Solomon evaluation."""

from itertools import combinations, product
from .finite import F2
from .linear import vec


FANO_POINTS = tuple(range(1, 8))
FANO_LINES = tuple(sorted({tuple(sorted((a, b, a ^ b)))
                           for a, b in combinations(FANO_POINTS, 2)}))
H = [[1, 0, 0, 1, 1, 0, 1],
     [0, 1, 0, 1, 0, 1, 1],
     [0, 0, 1, 0, 1, 1, 1]]


def hamming_encode(message):
    """Book convention: message = (c4,c5,c6,c7)."""
    if len(message) != 4 or any(x not in (0, 1) for x in message):
        raise ValueError('four binary message bits required')
    a, b, c, d = message
    return (a ^ b ^ d, a ^ c ^ d, b ^ c ^ d, a, b, c, d)


def syndrome(word):
    if len(word) != 7:
        raise ValueError('seven bits required')
    return tuple(vec(H, word, F2))


def hamming_decode(received):
    """Correct at most one bit. WARNING: cannot detect that 2+ bits flipped."""
    s = syndrome(received)
    if s == (0, 0, 0):
        return tuple(received), None
    col = next((j for j in range(7) if tuple(row[j] for row in H) == s), None)
    if col is None:
        raise AssertionError('every nonzero GF(2)^3 syndrome is a column')
    corrected = list(received)
    corrected[col] ^= 1
    return tuple(corrected), col + 1  # 1-indexed like the book


def all_codewords():
    return tuple(hamming_encode(message) for message in product((0, 1), repeat=4))


def hamming_weight(word):
    return sum(x != 0 for x in word)


def reed_solomon(coefficients, evaluation_points, prime):
    from .finite import Field
    f = Field(prime)
    if len(evaluation_points) != len(set(evaluation_points)):
        raise ValueError('evaluation points must be distinct')
    if any(not 0 <= x < prime for x in evaluation_points):
        raise ValueError('point outside base field')
    return tuple(sum(c * pow(x, i, prime) for i, c in enumerate(coefficients)) % prime
                 for x in evaluation_points)


def representable_fano_determinant():
    """Determinant of 110,101,011: equals -2 over the integers."""
    return -2
