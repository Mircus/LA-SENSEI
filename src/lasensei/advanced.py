"""Characteristic-sensitive geometry, Clifford relations and small Lie algebras."""
from .finite import F2, Field
from .linear import mul, add


def q_f2(x, y):
    return (x*x + x*y + y*y) % 2


def polar_q_f2(u, v):
    x, y = u
    a, b = v
    return (q_f2((x+a)%2, (y+b)%2) - q_f2(x,y) - q_f2(a,b)) % 2


def symplectic_form(u, v, p):
    return (u[0]*v[1] - u[1]*v[0]) % p


def quaternion_mul(u, v):
    """Quaternion multiplication in basis (1,i,j,k)."""
    a,b,c,d = u
    e,f,g,h = v
    return (a*e-b*f-c*g-d*h,
            a*f+b*e+c*h-d*g,
            a*g-b*h+c*e+d*f,
            a*h+b*g-c*f+d*e)


def commutator(a, b, f):
    x = mul(a, b, f)
    y = mul(b, a, f)
    return [[f.sub(x[i][j], y[i][j]) for j in range(len(x[0]))]
            for i in range(len(x))]


def sl2_basis(p):
    """E, F, H for p odd; over F2 H equals identity and is central."""
    f = Field(p)
    return (([[0,1],[0,0]], [[0,0],[1,0]], [[1,0],[0,f.neg(1)]]), f)
