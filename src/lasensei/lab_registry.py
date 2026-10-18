"""Book-aligned runnable core laboratories. Each returns plain JSON-compatible data."""
from .finite import F2, F3, F4, F8
from .linear import (all_gl2, determinant, eye, mul, power, companion,
                     minimal_polynomial, poly_eval_matrix, rank)
from .geometry import (FANO_LINES, H, all_codewords, hamming_encode,
                       syndrome, hamming_decode, hamming_weight)
from .rings import smith_2x2_full_rank, rank_mod
from .numerical import transient_profile


LABS = {
    'fano': ('Lab I: seven points and seven lines', 'labs/01_fano.md', 'I'),
    'passports': ('Lab II: the matrix with three passports', 'labs/02_three_passports.md', 'II'),
    'hamming': ('Lab III: decode a damaged seven-bit message', 'labs/03_hamming.md', 'III'),
    'similarity': ('Lab IV: two operators with the same characteristic polynomial', 'labs/04_similarity.md', 'IV'),
    'torsion': ('Lab V: what the rationals erase', 'labs/05_torsion.md', 'V'),
    'transients': ('Lab VI: eigenvalues miss transient growth', 'labs/06_transients.md', 'VI'),
}


def fano():
    count = {a: sum(a in line for line in FANO_LINES) for a in range(1, 8)}
    assert len(FANO_LINES) == 7 and all(c == 3 for c in count.values())
    weights = sorted(hamming_weight(c) for c in all_codewords() if any(c))
    assert weights[0] == 3 and weights.count(3) == 7
    return {
        'points': 7,
        'lines_as_binary_integers': [list(line) for line in FANO_LINES],
        'incidences': sum(count.values()),
        'lines_through_each_point': count,
        'minimum_hamming_weight': weights[0],
        'weight_three_codewords': weights.count(3),
        'invariant': 'u + v + w = 0 in F2^3',
    }


def passports():
    A = [[0, 1], [1, 1]]
    assert power(A, 3, F2) == eye(2)
    a = 2  # 0+1*alpha in the polynomial basis; encoded base 2
    # Multiplication by alpha on basis (1, alpha) has the very same matrix.
    multiplication_columns = [F4.digits(F4.mul(a, x)) for x in (1, a)]
    assert [[multiplication_columns[c][r] for c in range(2)] for r in range(2)] == A
    roots = [x for x in range(F4.order) if F4.add(F4.add(F4.mul(x,x), x), 1) == 0]
    assert roots == [2, 3]
    return {
        'matrix': A,
        'F2_order': 3,
        'F2_eigenvalues': [],
        'GF4_minimal_polynomial': 'x^2 + x + 1',
        'GF4_roots': [F4.display(x) for x in roots],
        'GF4_eigenvectors': [[F4.display(1), F4.display(x)] for x in roots],
        'scalar_warning': 'restriction of scalars is not scalar extension',
    }


def hamming():
    message = (1, 0, 1, 1)
    word = hamming_encode(message)
    corrupted = list(word)
    corrupted[5] ^= 1
    recovered, position = hamming_decode(corrupted)
    assert recovered == word and position == 6
    return {
        'message_c4_to_c7': list(message),
        'codeword': list(word),
        'received': corrupted,
        'syndrome': list(syndrome(corrupted)),
        'flipped_position_one_based': position,
        'recovered': list(recovered),
        'warning': 'two or more errors can cause miscorrection',
    }


def similarity():
    C = companion([1, 1, 1], F2)
    A = [[0] * 4 for _ in range(4)]
    for k in (0, 2):
        for i in range(2):
            for j in range(2):
                A[k+i][k+j] = C[i][j]
    B = companion([1, 0, 1, 0, 1], F2)  # (x^2+x+1)^2
    pa = poly_eval_matrix([1, 1, 1], A, F2)
    pb = poly_eval_matrix([1, 1, 1], B, F2)
    assert minimal_polynomial(A, F2) == [1, 1, 1]
    assert minimal_polynomial(B, F2) == [1, 0, 1, 0, 1]
    return {
        'A': A, 'B': B,
        'characteristic_polynomial_both': '(x^2+x+1)^2',
        'minimal_A': 'x^2+x+1', 'minimal_B': '(x^2+x+1)^2',
        'rank_p_A': rank(pa, F2), 'rank_p_B': rank(pb, F2),
        'similar': False,
    }


def torsion():
    D = [[2, 4], [0, 6]]
    d = smith_2x2_full_rank(D)
    jumps = {str(p): rank_mod(D, p) for p in (2, 3, 5, 7)}
    assert d == (2, 6) and jumps == {'2': 0, '3': 1, '5': 2, '7': 2}
    return {
        'matrix': D, 'smith_diagonal': list(d),
        'cokernel': 'Z/2Z ⊕ Z/6Z', 'cokernel_order': 12,
        'rank_over_Q': 2, 'ranks_mod_primes': jumps,
        'invariant': 'integral torsion disappears after tensoring with Q',
    }


def transients():
    profile = transient_profile(a=0.8, coupling=30, steps=70)
    peak = max(profile, key=lambda row: row[1])
    assert peak[1] > 20
    return {
        'eigenvalues': [0.8, 0.8],
        'spectral_radius': 0.8,
        'matrix': [[0.8, 30.0], [0, 0.8]],
        'peak_step_in_window': peak[0],
        'peak_operator_2_norm': round(peak[1], 6),
        'operator_2_norm_at_step_70': round(profile[-1][1], 6),
        'lesson': 'spectral radius controls asymptotic powers, not transient size',
    }


RUNNERS = dict(fano=fano, passports=passports, hamming=hamming,
               similarity=similarity, torsion=torsion, transients=transients)
