"""One executable exercise workshop per chapter of the current booklet draft.

Identifiers Ecc.ee are fixed to the supplied Oct 2026 manuscript edition.
Proof exercises remain proof exercises: the software only checks concrete instances.
"""
from itertools import combinations, product
from .finite import Field, F2, F3, F4, F8, F9
from .linear import (all_gl2, rank, nullspace, power, eye, mul, minimal_polynomial,
                     determinant, companion, poly_eval_matrix, vec)
from .geometry import (FANO_LINES, FANO_POINTS, H, hamming_encode, hamming_decode,
                       syndrome, reed_solomon, all_codewords, hamming_weight)
from .rings import smith_2x2_full_rank, rank_mod, circle_boundary
from .tropical import semiring_product, maxplus_mv, floyd_warshall
from .tensors import (exterior_dimensions, plucker_coordinates,
                      plucker_relation, w_flattenings)
from .symmetry import gl2_f2_permutations, modular_cp_invariants
from .advanced import (q_f2, polar_q_f2, symplectic_form, quaternion_mul,
                       commutator, sl2_basis)


def ch01():
    gl = len(all_gl2(F3))
    lines = (3**2-1) // (3-1)
    assert (gl, lines, len(FANO_LINES)) == (48, 4, 7)
    return {'E01.02': {'GL(2,F3)': gl, 'projective_lines_F3_squared': lines},
            'E01.04': {'Fano_points': len(FANO_POINTS), 'Fano_lines': len(FANO_LINES)}}


def ch02():
    mult = [[F4.display(F4.mul(a,b)) for b in range(4)] for a in range(4)]
    inverses = {F4.display(a): F4.display(F4.inv(a)) for a in (1, 2, 3)}
    trace_norm = {F4.display(a): [F4.trace(a), F4.norm(a)] for a in range(4)}
    orbit = F8.frobenius_orbit(2)
    assert orbit == (2, 4, 6) and F8.trace(2) == 0
    return {'E02.01': {'multiplication_table_order_0_1_alpha_1plusalpha': mult,
                        'nonzero_inverses': inverses},
            'E02.03': {'trace_and_norm': trace_norm},
            'E02.05': {'F8_alpha_Frobenius_orbit': [F8.display(x) for x in orbit],
                        'F8_trace_alpha': F8.trace(2)}}


def ch03():
    A = [[0, 1], [1, 1]]
    rotation = [[0, 2], [1, 0]]  # -1=2 in F3
    roots = [F9.display(x, 'β') for x in range(9) if F9.add(F9.mul(x, x),1)==0]
    assert power(A,3,F2)==eye(2) and power(rotation,4,F3)==eye(2)
    assert len(roots)==2
    return {'E03.01': {'A_cubed_is_identity':True,
                       'GF4_eigenvalues':['α', 'α+1']},
            'E03.02': {'same_characteristic_polynomial':['I', 'I+N'],
                       'different_minimal_polynomials':['x+1','(x+1)^2']},
            'E03.04': {'matrix_order_over_F3':4, 'eigenvalues_in_F9':roots}}


def ch04():
    N = [[0,1,0],[0,0,0],[0,0,0]]
    assert minimal_polynomial(N,F2)==[0,0,1]
    # Exhaust all 2^9 binary matrices; nilpotent classes are detected by ranks
    # of N and N², corresponding to the three partitions of 3.
    counts = {}
    for entries in product(range(2), repeat=9):
        T = [list(entries[i:i+3]) for i in (0,3,6)]
        T2 = mul(T,T,F2)
        T3 = mul(T2,T,F2)
        if T3 == [[0]*3 for _ in range(3)]:
            key = (rank(T,F2),rank(T2,F2))
            counts[key] = counts.get(key,0)+1
    assert set(counts)=={(0,0),(1,0),(2,1)}
    return {'E04.01': {'invariant_factors':['x','x^2'], 'minimal_polynomial':'x^2',
                       'characteristic_polynomial':'x^3'},
            'E04.04': {'nilpotent_similarity_invariants_rankN_rankN2':
                       {str(k):v for k,v in sorted(counts.items())},
                       'similarity_classes': 3, 'nilpotent_matrices_enumerated':sum(counts.values())}}


def ch05():
    T = [[1,2],[0,1],[2,2]]
    transpose = [list(column) for column in zip(*T)]
    M=[[1,0],[0,1]]
    assert rank(M,F3)==2
    return {'E05.03': {'dual_map_matrix_over_F3':transpose},
            'E05.05': {'tensor_example':'e1⊗e1 + e2⊗e2',
                       'corresponding_matrix':M, 'matrix_rank':rank(M,F3)}}


def ch06():
    values = {f'{x},{y}':q_f2(x,y) for x,y in product(range(2),repeat=2)}
    vectors = list(product(range(3), repeat=2))
    lines = {tuple(sorted((v,(2*v[0]%3,2*v[1]%3))))
             for v in vectors if v != (0,0)}
    assert len(lines)==4 and all(symplectic_form(v,v,3)==0 for v in vectors)
    return {'E06.01': {'Q_values':values,'polar_B_e1_e2':polar_q_f2((1,0),(0,1))},
            'E06.04': {'isotropic_lines_in_F3_squared':
                       [[list(v) for v in line] for line in sorted(lines)],
                       'count':len(lines)}}


def ch07():
    p=plucker_coordinates((1,0,1,0),(0,1,0,1),F3)
    assert plucker_relation(p,F3)==0
    return {'E07.01': {'exterior_dimensions_for_n5':list(exterior_dimensions(5))},
            'E07.04': {'Plucker_coordinates':{str(k):v for k,v in p.items()},
                       'quadratic_relation_mod3':plucker_relation(p,F3)},
            'E07.05_PARTIAL': {'W_flattening_ranks':list(w_flattenings()),
                              'warning':'Flattening rank 2 cannot certify tensor rank 3.'}}


def ch08():
    perms = gl2_f2_permutations()
    assert len(perms)==6 and len(set(p for _,p in perms))==6
    return {'E08.02': {'GL2_F2_elements':len(perms),
                       'permutations':[list(p) for _,p in perms]},
            'E08.04': {'Cp_generator_invariant_line_basis_F5':modular_cp_invariants(5)}}


def ch09():
    k=(0,0,0,1); unit=(1,0,0,0); i=(0,1,0,0); j=(0,0,1,0)
    assert quaternion_mul(k,k)==(-1,0,0,0)
    assert quaternion_mul(i,i)==(-1,0,0,0)
    assert quaternion_mul(j,j)==(-1,0,0,0)
    assert quaternion_mul(i,j)==k and quaternion_mul(j,i)==(0,0,0,-1)
    def imul(a,b):
        return [[sum(a[i][t]*b[t][jj] for t in range(2)) for jj in range(2)] for i in range(2)]
    I=[[1,0],[0,1]]; e1=[[1,0],[0,-1]]; e2=[[0,1],[1,0]]
    assert imul(e1,e1)==I and imul(e2,e2)==I
    e12=imul(e1,e2)
    assert [[imul(e1,e2)[r][c]+imul(e2,e1)[r][c] for c in range(2)] for r in range(2)]==[[0,0],[0,0]]
    flattened=[[M[r][c]%3 for r in range(2) for c in range(2)] for M in (I,e1,e2,e12)]
    assert rank(flattened,F3)==4
    return {'E09.01': {'quaternion_k_squared':list(quaternion_mul(k,k))},
            'E09.05': {'Cl_2_0_generators_square_to_plus_I':True,
                       'matrix_monomials_are_linearly_independent':True,
                       'Cl_0_2_generators_quaternion_units_square_to_minus_1':True,
                       'anticommutation_verified':True,
                       'reading':'Together with the universal property and dimension 4, these establish the identifications.'}}


def ch10():
    (E,F,H), f = sl2_basis(3)
    eh=commutator(E,F,f)
    he=commutator(H,E,f)
    assert eh==H and he==[[0,2],[0,0]]
    (E2,F2,H2), f2 = sl2_basis(2)
    assert all(commutator(H2,a,f2)==[[0,0],[0,0]] for a in (E2,F2,H2))
    return {'E10.02': {'basis_E':E,'basis_F':F,'basis_H':H,
                       '[E,F]':eh, '[H,E]':he},
            'E10.05': {'F2_identity_has_trace_0':True,
                       'identity_central_in_sl2_F2':True}}


def ch11():
    solutions_2 = [x for x in range(6) if (2*x-2)%6==0]
    solutions_1 = [x for x in range(6) if (2*x-1)%6==0]
    D=[[2,4],[0,6]]
    circle = circle_boundary(5)
    assert rank_mod(circle,2)==4
    return {'E11.01': {'2x_equals_2_mod6':solutions_2,
                       '2x_equals_1_mod6':solutions_1},
            'E11.03': {'smith_invariants':list(smith_2x2_full_rank(D)),
                       'cokernel':'Z/2 ⊕ Z/6'},
            'E11.05': {'five_edge_circle_rank_mod2':4,
                       'dimension_H1_mod2':1, 'H1_over_Z':'Z'}}


def ch12():
    A=[[0,1,0],[0,0,1],[0,0,0]]
    Boolean_square=semiring_product(A,A,mode='boolean')
    weighted=[[float('inf'),4,9],[float('inf'),float('inf'),-1],
              [float('inf'),float('inf'),float('inf')]]
    distances=floyd_warshall(weighted)
    eigen=maxplus_mv([[0,2],[1,0]],[.5,0])
    assert eigen==[2,1.5] and distances[0][2]==3
    return {'E12.01':{'boolean_square':Boolean_square},
            'E12.03': {'lambda':1.5, 'eigenvector':[.5,0], 'A_times_x':eigen},
            'E12.05': {'shortest_path_1_to_3':distances[0][2],
                       'direct_edge_1_to_3':9}}


def ch13():
    word=hamming_encode((1,0,1,1))
    corrupted=list(word); corrupted[5]^=1
    fixed, position=hamming_decode(corrupted)
    assert fixed==word and position==6
    values=reed_solomon((1,2,1), range(5), 7)
    assert values == (1,4,2,2,4)
    import math
    bell=[[1/math.sqrt(2),0],[0,1/math.sqrt(2)]]
    reduced=[[sum(bell[i][k]*bell[j][k] for k in range(2))
              for j in range(2)] for i in range(2)]
    assert all(math.isclose(reduced[i][j], (.5 if i==j else 0), abs_tol=1e-14)
               for i in range(2) for j in range(2))
    return {'E13.01': {'error_syndrome_bit_6':list(syndrome(corrupted)),
                       'corrected_position':position},
            'E13.03': {'RS_F7':list(values)},
            'E13.05': {'Bell_state_Schmidt_coefficients':['1/sqrt(2)','1/sqrt(2)'],
                       'reduced_density_matrix':reduced}}


def ch14():
    columns=[[1,1,0],[1,0,1],[0,1,1]]
    detZ=-2
    assert determinant(columns,F2)==0 and determinant(columns,F3)!=0
    return {'E14.03': {'det_over_Z':detZ,'det_over_F2':0,
                       'det_over_F3':determinant(columns,F3)},
            'E14.05_PARTIAL': {'binary_Hamming_weight3_words':
                              sum(1 for c in all_codewords() if hamming_weight(c)==3),
                              'note':'Circuits correspond to minimal dependent column sets.'}}


RUNNERS={i:globals()[f'ch{i:02}'] for i in range(1,15)}
