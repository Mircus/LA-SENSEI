"""Tiny, auditable arithmetic for GF(p)[x]/(f); elements encoded base-p.

This is for education, not a high-performance or constant-time crypto library.
"""
from dataclasses import dataclass
from math import isqrt


def _prime(p):
    return p >= 2 and all(p % d for d in range(2, isqrt(p) + 1))


def _trim(a):
    result = list(a)
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def _poly_remainder(a, b, p):
    a, b = _trim(a), _trim(b)
    if b == [0]:
        raise ZeroDivisionError('zero polynomial')
    while a != [0] and len(a) >= len(b):
        factor = a[-1] * pow(b[-1], -1, p) % p
        shift = len(a) - len(b)
        for j, coef in enumerate(b):
            a[j + shift] = (a[j + shift] - factor * coef) % p
        a = _trim(a)
    return a


def _irreducible(modulus, p):
    """Trial monic divisors: fine for the small finite fields used in the book."""
    n = len(modulus) - 1
    for degree in range(1, n // 2 + 1):
        for index in range(p ** degree):
            coeffs = []
            value = index
            for _ in range(degree):
                coeffs.append(value % p)
                value //= p
            if _poly_remainder(modulus, coeffs + [1], p) == [0]:
                return False
    return True


@dataclass(frozen=True)
class Field:
    """GF(p^n), with modulus coefficients in ascending degree order."""

    p: int
    modulus: tuple[int, ...] | None = None

    def __post_init__(self):
        if not _prime(self.p):
            raise ValueError('p must be prime')
        if self.modulus is not None:
            m = tuple(self.modulus)
            if len(m) < 3 or m[-1] != 1 or any(not 0 <= x < self.p for x in m):
                raise ValueError('provide a monic polynomial of degree >=2 over F_p')
            if not _irreducible(m, self.p):
                raise ValueError('modulus must be irreducible')
            object.__setattr__(self, 'modulus', m)

    @property
    def degree(self):
        return len(self.modulus) - 1 if self.modulus else 1

    @property
    def order(self):
        return self.p ** self.degree

    def digits(self, a):
        if not 0 <= a < self.order:
            raise ValueError(f'element {a} outside GF({self.order})')
        coefficients = []
        for _ in range(self.degree):
            coefficients.append(a % self.p)
            a //= self.p
        return coefficients

    def encode(self, coefficients):
        if len(coefficients) > self.degree:
            raise ValueError('too many coefficients')
        return sum((a % self.p) * self.p ** i for i, a in enumerate(coefficients))

    def add(self, a, b):
        return self.encode([(x + y) % self.p for x, y in zip(self.digits(a), self.digits(b))])

    def neg(self, a):
        return self.encode([-x for x in self.digits(a)])

    def sub(self, a, b):
        return self.add(a, self.neg(b))

    def mul(self, a, b):
        if self.modulus is None:
            return a * b % self.p
        u, v = self.digits(a), self.digits(b)
        coeff = [0] * (2 * self.degree - 1)
        for i, x in enumerate(u):
            for j, y in enumerate(v):
                coeff[i + j] = (coeff[i + j] + x * y) % self.p
        for k in range(len(coeff) - 1, self.degree - 1, -1):
            c = coeff[k]
            for j in range(self.degree):
                coeff[k - self.degree + j] = (coeff[k - self.degree + j] - c * self.modulus[j]) % self.p
        return self.encode(coeff[:self.degree])

    def pow(self, a, power):
        if power < 0:
            return self.pow(self.inv(a), -power)
        product = 1
        while power:
            if power & 1:
                product = self.mul(product, a)
            a = self.mul(a, a)
            power >>= 1
        return product

    def inv(self, a):
        if a == 0:
            raise ZeroDivisionError('zero has no inverse')
        return self.pow(a, self.order - 2)

    def div(self, a, b):
        return self.mul(a, self.inv(b))

    def trace(self, a):
        result = 0
        for i in range(self.degree):
            result = self.add(result, self.pow(a, self.p ** i))
        assert result < self.p
        return result

    def norm(self, a):
        result = 1
        for i in range(self.degree):
            result = self.mul(result, self.pow(a, self.p ** i))
        assert result < self.p
        return result

    def frobenius_orbit(self, a):
        orbit = []
        while a not in orbit:
            orbit.append(a)
            a = self.pow(a, self.p)
        return tuple(orbit)

    def display(self, a, generator='α'):
        digits = self.digits(a)
        pieces = []
        for i, coeff in reversed(list(enumerate(digits))):
            if coeff:
                term = '1' if i == 0 else generator if i == 1 else f'{generator}^{i}'
                pieces.append((str(coeff) if i == 0 else ('' if coeff == 1 else str(coeff) + '·') + term))
        return ' + '.join(pieces) if pieces else '0'


F2 = Field(2)
F3 = Field(3)
F4 = Field(2, (1, 1, 1))
F8 = Field(2, (1, 1, 0, 1))
F9 = Field(3, (1, 0, 1))
