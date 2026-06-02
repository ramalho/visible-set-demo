import pytest
from hashtable import HashTable, EMPTY_HASH, NULL, Location


def test_default_size():
    ht = HashTable()
    assert len(ht._table) == 8


def test_custom_size():
    ht = HashTable(size=16)
    assert len(ht._table) == 16


def test_add_and_len():
    ht = HashTable()
    ht.insert('a')
    ht.insert('b')
    ht.insert('c')
    assert len(ht) == 3


def test_add_duplicate_ignored():
    ht = HashTable()
    ht.insert('x')
    ht.insert('x')
    assert len(ht) == 1


def test_contains_true():
    ht = HashTable()
    ht.insert(42)
    assert 42 in ht


def test_contains_false():
    ht = HashTable()
    ht.insert(42)
    assert 99 not in ht


def test_contains_empty():
    ht = HashTable()
    assert 'anything' not in ht


def test_grow_doubles_capacity():
    ht = HashTable()
    old_capacity = len(ht._table)
    ht._grow()
    assert len(ht._table) == old_capacity * 2


def test_grow_preserves_elements():
    ht = HashTable()
    elements = ['a', 'b', 'c']
    for element in elements:
        ht.insert(element)
    ht._grow()
    assert len(ht) == len(elements)
    assert set(ht) == set(elements)


def test_add_triggers_grow():
    ht = HashTable()
    for i in range(5):  # 5/8 = 62.5%, just under 2/3
        ht.insert(i)
    assert len(ht._table) == 8
    ht.insert(5)  # 6/8 = 75% > 2/3, triggers grow
    assert len(ht._table) == 16
    assert set(ht) == set(range(6))


def test_locate_returns_probe_location():
    ht = HashTable()
    ht.insert('hello')
    assert isinstance(ht.locate('hello'), Location)


def test_find_returns_hash_and_slot_for_present_element():
    ht = HashTable()
    ht.insert('hello')
    location = ht.locate('hello')
    assert location.hash_code is not EMPTY_HASH
    assert ht._table['value'][location.offset] == 'hello'


def test_find_returns_no_hash_and_empty_slot_for_absent_element():
    ht = HashTable()
    ht.insert('hello')
    location = ht.locate('world')
    assert location.hash_code is EMPTY_HASH
    assert ht._table['value'][location.offset] is NULL


def test_find_on_empty_table():
    ht = HashTable()
    location = ht.locate(42)
    assert location.hash_code is EMPTY_HASH
    assert location.offset == hash(42) % len(ht._table)


def test_find_loc_is_insertion_point_when_not_found():
    ht = HashTable()
    element = 'new'
    location = ht.locate(element)
    assert location.hash_code is EMPTY_HASH
    ht.insert(element)
    location2 = ht.locate(element)
    assert location2.hash_code is not EMPTY_HASH
    assert location.offset == location2.offset  # same slot used for insertion
    assert location2.hash_code == hash(element)
