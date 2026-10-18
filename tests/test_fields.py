import pytest
from lasensei.finite import Field, F2, F3, F4, F8, F9


@pytest.mark.parametrize('field',[F2,F3,F4,F8,F9])
def test_field_axioms_exhaustive(field):
    values=range(field.order)
    for a in values:
        assert field.add(a,0)==a and field.mul(a,1)==a
        assert field.add(a,field.neg(a))==0
        if a: assert field.mul(a,field.inv(a))==1
        assert field.pow(a,field.order)==a
        for b in values:
            assert field.add(a,b)==field.add(b,a)
            assert field.mul(a,b)==field.mul(b,a)
            for c in values:
                assert field.mul(a,field.add(b,c))==field.add(field.mul(a,b),field.mul(a,c))
                assert field.mul(field.mul(a,b),c)==field.mul(a,field.mul(b,c))


def test_f4_trace_norm_and_orbit():
    assert F4.frobenius_orbit(2)==(2,3)
    assert F4.trace(2)==1 and F4.norm(2)==1
    assert F4.trace(1)==0


def test_f8_trace():
    assert F8.frobenius_orbit(2)==(2,4,6)
    assert F8.trace(2)==0


def test_irreducibility_rejected():
    with pytest.raises(ValueError):
        Field(2, (0,1,1))  # x²+x has x factor
    with pytest.raises(ValueError):
        Field(4)


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError): F4.inv(0)
