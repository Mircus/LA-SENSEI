"""Small matrix groups and modular representation examples."""
from .finite import F2, Field
from .linear import all_gl2, vec, eye, power, nullspace


def gl2_f2_permutations():
    """List (matrix, permutation) of three nonzero binary vectors."""
    nonzero = [(1, 0), (0, 1), (1, 1)]
    result = []
    for a in all_gl2(F2):
        permutation = tuple(nonzero.index(tuple(vec(a, v, F2))) + 1 for v in nonzero)
        result.append((a, permutation))
    return result


def modular_cp_generator(p):
    return [[1, 1], [0, 1]], Field(p)


def modular_cp_invariants(p):
    """Invariant 1-spaces for the C_p action in the book."""
    generator, f = modular_cp_generator(p)
    eigen = [[f.sub(generator[i][j], int(i == j)) for j in range(2)] for i in range(2)]
    return nullspace(eigen, f)
