import pytest
from visiset import VisiSet


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
    items = ['a', 'b', 'c']
    vs = VisiSet(items)
    vs.add('b')
    assert len(vs) == len(items)


def test_contains_true():
    vs = VisiSet(['a', 'b', 'c', 'd'])
    assert 'b' in vs


def test_contains_false():
    vs = VisiSet(['a', 'b', 'c', 'd'])
    assert 'z' not in vs


def test_repr():
    items = ['a', 'b', 'c', 'd']
    vs = VisiSet(items)
    r = repr(vs)
    assert r.startswith('VisiSet(')
    for item in items:
        assert f"'{item}'" in r


def test_grow():
    items = ['a', 'b', 'c', 'd']
    vs = VisiSet(items)
    old_capacity = len(vs._table)
    vs._grow()
    assert len(vs._table) == old_capacity * 2
    assert len(vs) == len(items)
    assert set(vs) == set(items)


def test_add_triggers_grow():
    vs = VisiSet([1, 2, 3, 4, 5])  # 5/8 = 62.5%, just under 2/3
    assert len(vs._table) == 8
    vs.add(6)  # 6/8 = 75% > 2/3, triggers grow
    assert len(vs._table) == 16
    assert set(vs) == {1, 2, 3, 4, 5, 6}
