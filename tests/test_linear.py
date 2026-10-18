from itertools import product
from lasensei.finite import F2,F3,F4
from lasensei.linear import (eye,mul,power,rref,rank,nullspace,determinant,
                              vec,companion,minimal_polynomial,poly_eval_matrix,all_gl2,solve)


def test_order_three_without_binary_eigenvalues():
    a=[[0,1],[1,1]]
    assert power(a,3,F2)==eye(2)
    assert minimal_polynomial(a,F2)==[1,1,1]
    assert [lam for lam in range(F2.order) if determinant([[F2.sub(a[i][j],lam if i==j else 0) for j in range(2)] for i in range(2)],F2)==0]==[]
    assert [lam for lam in range(F4.order) if determinant([[F4.sub(a[i][j],lam if i==j else 0) for j in range(2)] for i in range(2)],F4)==0]==[2,3]


def test_companion_minimal_polynomial():
    b=companion([1,0,1,0,1],F2)
    assert minimal_polynomial(b,F2)==[1,0,1,0,1]
    assert poly_eval_matrix([1,0,1,0,1],b,F2)==[[0]*4 for _ in range(4)]


def test_rank_nullity_and_rref():
    a=[[1,0,1,1],[0,1,1,0]]
    ns=nullspace(a,F3)
    assert rank(a,F3)==2 and len(ns)==2
    assert all(vec(a,x,F3)==[0,0] for x in ns)


def test_linear_system_solve_and_inconsistent():
    assert solve([[1,0],[0,1]],[2,1],F3)==[2,1]
    assert solve([[0]],[1],F3) is None


def test_gl2_counts():
    assert len(all_gl2(F2))==6
    assert len(all_gl2(F3))==48


def test_det_multiplicative_many_binary_matrices():
    all_mats=[[[a,b],[c,d]] for a,b,c,d in product(range(2),repeat=4)]
    for a in all_mats:
        for b in all_mats:
            assert determinant(mul(a,b,F2),F2)==F2.mul(determinant(a,F2),determinant(b,F2))
