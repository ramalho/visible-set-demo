from collections.abc import Iterator
from typing import NamedTuple

import numpy as np

DEFAULT_SIZE = 8
EMPTY_HASH = -1  # -1 is never returned by hash() in CPython
NULL = object()  # sentinel representing no value


class Location(NamedTuple):
    offset: int
    hash_code: int


class HashTable:
    """Hash table backed by a numpy structured array of (hash: int64, value: object) rows.

    Uses linear probing on collision. Empty slots hold hash=-1 and value=NULL.
    Doubles in size if occupancy would exceed 2/3 when adding element.
    """

    def __init__(self, size: int = DEFAULT_SIZE) -> None:
        self._element_count = 0
        self._make_table(size)

    def _make_table(self, size: int) -> None:
        table = np.empty(size, dtype=[('hash', np.int64), ('value', object)])
        table['hash'][:] = EMPTY_HASH
        table['value'][:] = NULL
        self._table = table

    def insert(self, element: object) -> None:
        location = self.locate(element)
        if location.hash_code is EMPTY_HASH:
            if self._needs_space():
                self._grow()
                location = self.locate(element)
            self._new_row(location, element)

    def _needs_space(self) -> bool:
        """Return True if inserting one element would push occupancy above 2/3."""
        return (self._element_count + 1) / len(self._table) > 2 / 3

    def _new_row(self, location: Location, element: object) -> None:
        self._table['hash'][location.offset] = hash(element)
        self._table['value'][location.offset] = element
        self._element_count += 1

    def _grow(self) -> None:
        """Double the table size and re-insert all existing elements."""
        current = self._table
        self._make_table(len(current) * 2)
        self._element_count = 0
        for row in current:
            if row['value'] is not NULL:
                self._new_row(self.locate(row['value']), row['value'])

    def locate(self, element: object) -> Location:
        """Linear probe for element, starting at hash(element) % self.size()

        If found, offset is row where element was found
        If not found, offset is the first empty row and hash_code is EMPTY_HASH
        """
        h = hash(element)
        offset = h % len(self._table)
        while (v:= self._table['value'][offset]) is not NULL:
            if v == element:
                return Location(offset, h)
            offset = (offset + 1) % len(self._table)
        return Location(offset, EMPTY_HASH)

    def __contains__(self, element: object) -> bool:
        return self.locate(element).hash_code is not EMPTY_HASH

    def __len__(self) -> int:
        return self._element_count

    def __iter__(self) -> Iterator[object]:
        for row in self._table:
            if row['value'] is not NULL:
                yield row['value']
