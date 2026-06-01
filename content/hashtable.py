import numpy as np

DEFAULT_SIZE = 8
EMPTY_HASH = -1  # -1 is never returned by hash() in CPython
NULL = object()  # sentinel representing no value


class HashTable:
    """Hash table backed by a numpy structured array of (hash: int64, value: object) rows.

    Uses linear probing on collision. Empty slots hold hash=-1 and value=NULL.
    Doubles in size if occupancy would exceed 2/3 when adding element.
    """

    def __init__(self, size=DEFAULT_SIZE):
        self._element_count = 0
        self._make_table(size)

    def _make_table(self, size):
        table = np.empty(size, dtype=[('hash', np.int64), ('value', object)])
        table['hash'][:] = EMPTY_HASH
        table['value'][:] = NULL
        self._table = table

    def add(self, element, grow=True):
        offset, h = self.locate(element)
        if h is EMPTY_HASH:
            if grow and self._needs_space():
                self._grow()
                offset, h2 = self.locate(element)
                assert h2 is EMPTY_HASH
            self._table['hash'][offset] = hash(element)
            self._table['value'][offset] = element
            self._element_count += 1

    def _needs_space(self):
        """Return True if adding one element would push occupancy above 2/3."""
        return (self._element_count + 1) / len(self._table) > 2 / 3

    def _grow(self):
        """Double the table size and re-insert all existing elements."""
        current = self._table
        self._make_table(len(current) * 2)
        self._element_count = 0
        for row in current:
            if row['value'] is not NULL:
                self.add(row['value'], grow=False)

    def locate(self, element):
        """Linear probe for element, starting at hash(element) % self.size()

        If found, offset is row where element was found
        If not found, offset is the first empty row and hash is EMPTY_HASH
        """
        h = hash(element)
        offset = h % len(self._table)
        while (v:= self._table['value'][offset]) is not NULL:
            if v == element:
                return offset, h
            offset = (offset + 1) % len(self._table)
        return offset, EMPTY_HASH

    def __contains__(self, element):
        _, h = self.locate(element)
        return h is not EMPTY_HASH

    def __len__(self):
        return self._element_count

    def __iter__(self):
        for row in self._table:
            if row['value'] is not NULL:
                yield row['value']
