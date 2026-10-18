from itertools import combinations, product
from collections import Counter
from lasensei.geometry import (FANO_POINTS,FANO_LINES,H,hamming_encode,syndrome,
                                hamming_decode,all_codewords,hamming_weight,reed_solomon)


def test_fano_plane_projective_incidence():
    assert len(FANO_POINTS)==7 and len(FANO_LINES)==7
    assert all(len(line)==3 for line in FANO_LINES)
    assert all(sum({u,v}.issubset(line) for line in FANO_LINES)==1
               for u,v in combinations(FANO_POINTS,2))
    assert all(sum(u in line for line in FANO_LINES)==3 for u in FANO_POINTS)


def test_hamming_exhaustive_single_error_correction():
    words=all_codewords()
    assert len(words)==16
    assert len(set(words))==16
    assert all(syndrome(word)==(0,0,0) for word in words)
    for word in words:
        for i in range(7):
            corrupted=list(word); corrupted[i]^=1
            fixed,pos=hamming_decode(corrupted)
            assert fixed==word and pos==i+1


def test_hamming_minimum_distance():
    ws=[hamming_weight(word) for word in all_codewords() if any(word)]
    assert min(ws)==3 and ws.count(3)==7


def test_reed_solomon_example():
    assert reed_solomon((1,2,1),list(range(5)),7)==(1,4,2,2,4)
