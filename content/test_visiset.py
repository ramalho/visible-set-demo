import pytest
from visiset import VisiSet


@pytest.mark.parametrize('hash_code, hash_width, fmt_base, expected', [
    # hex, 64-bit
    ( 0, 64, 16, '0000000000000000'),
    ( 1, 64, 16, '0000000000000001'),
    (-1, 64, 16, 'ffffffffffffffff'),
    # hex, 32-bit
    ( 0, 32, 16, '00000000'),
    ( 1, 32, 16, '00000001'),
    (-1, 32, 16, 'ffffffff'),
    # binary, 64-bit
    ( 0, 64,  2, '0' * 64),
    ( 1, 64,  2, '0' * 63 + '1'),
    (-1, 64,  2, '1' * 64),
    # binary, 32-bit
    ( 0, 32,  2, '0' * 32),
    ( 1, 32,  2, '0' * 31 + '1'),
    (-1, 32,  2, '1' * 32),
])
def test_fmt_hash(hash_code, hash_width, fmt_base, expected):
    vs = VisiSet(fmt_base=fmt_base)
    assert vs._fmt_hash(hash_code, hash_width) == expected


def test_construction_integers_and_iterable_vs():
    vs = VisiSet([10, 20, 30, 40, 50])
    assert set(vs) == {10, 20, 30, 40, 50}


def test_construction_strings():
    vs = VisiSet(['apple', 'banana', 'cherry'])
    assert set(vs) == {'apple', 'banana', 'cherry'}


def test_construction_mixed_hashable_types():
    vs = VisiSet([3.14, True, (1, 2), frozenset({10, 20})])
    assert set(vs) == {3.14, True, (1, 2), frozenset({10, 20})}


def test_len():
    vs = VisiSet(['a', 'b', 'c', 'd'])
    assert len(vs) == 4


def test_add_new_element():
    vs = VisiSet(['a', 'b', 'c'])
    vs.add('d')
    assert set(vs) == {'a', 'b', 'c', 'd'}


def test_add_duplicate_ignored():
    elements = ['a', 'b', 'c']
    vs = VisiSet(elements)
    vs.add('b')
    assert len(vs) == len(elements)


def test_contains_true():
    vs = VisiSet(['a', 'b', 'c', 'd'])
    assert 'b' in vs


def test_contains_false():
    vs = VisiSet(['a', 'b', 'c', 'd'])
    assert 'z' not in vs


def test_repr():
    elements = ['a', 'b', 'c', 'd']
    vs = VisiSet(elements)
    r = repr(vs)
    assert r.startswith('VisiSet(')
    for element in elements:
        assert f"'{element}'" in r
