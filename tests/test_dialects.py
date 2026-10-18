import math
import pytest
from lasensei.finite import F2,F3,F4
from lasensei.rings import smith_2x2_full_rank,rank_mod,circle_boundary
from lasensei.tropical import semiring_product,maxplus_mv,floyd_warshall
from lasensei.tensors import exterior_dimensions,plucker_coordinates,plucker_relation,w_flattenings
from lasensei.symmetry import gl2_f2_permutations,modular_cp_invariants
from lasensei.numerical import jordan_power,norm2,transient_profile
from lasensei.advanced import q_f2,polar_q_f2,quaternion_mul,commutator,sl2_basis


def test_smith_and_rank_jumps():
    d=[[2,4],[0,6]]
    assert smith_2x2_full_rank(d)==(2,6)
    assert [rank_mod(d,p) for p in (2,3,5)]==[0,1,2]
    with pytest.raises(ValueError): smith_2x2_full_rank([[1,0],[0,0]])


def test_circle_boundary_column_sums():
    d=circle_boundary(5)
    assert all(sum(row[j] for row in d)==0 for j in range(5))
    assert rank_mod(d,2)==4


def test_tropical_and_boolean():
    a=[[0,1,0],[0,0,1],[0,0,0]]
    assert semiring_product(a,a,mode='boolean')==[[0,0,1],[0,0,0],[0,0,0]]
    assert maxplus_mv([[0,2],[1,0]],[.5,0])==[2,1.5]
    w=[[float('inf'),4,9],[float('inf'),float('inf'),-1],[float('inf'),float('inf'),float('inf')]]
    assert floyd_warshall(w)[0][2]==3
    with pytest.raises(ValueError): floyd_warshall([[0,-1],[-1,0]])


def test_plucker_and_w():
    assert exterior_dimensions(5)==(1,5,10,10,5,1)
    p=plucker_coordinates((1,0,1,0),(0,1,0,1),F3)
    assert plucker_relation(p,F3)==0
    assert w_flattenings()==(2,2,2)


def test_symmetry():
    perms=gl2_f2_permutations()
    assert len(perms)==6 and len({perm for _,perm in perms})==6
    assert modular_cp_invariants(5)==[[1,0]]


def test_forms_and_clifford():
    assert [q_f2(*v) for v in ((0,0),(1,0),(0,1),(1,1))]==[0,1,1,1]
    assert polar_q_f2((1,0),(0,1))==1
    k=(0,0,0,1)
    assert quaternion_mul(k,k)==(-1,0,0,0)


def test_sl2_char2_center():
    (E,F,H),f=sl2_basis(3)
    assert commutator(E,F,f)==H
    (E,F,H),f=sl2_basis(2)
    assert all(commutator(H,x,f)==[[0,0],[0,0]] for x in (E,F,H))


def test_stable_eigenvalues_transient_amplification():
    prof=transient_profile(a=.8,coupling=30,steps=70)
    assert max(v for _,v in prof)>60
    assert prof[-1][1]<.001
    assert jordan_power(.8,30,0)==((1,0),(0,1))
    assert math.isclose(norm2(((1,0),(0,1))),1)
