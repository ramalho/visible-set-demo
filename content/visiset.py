import numpy as np

EMPTY_BUCKET = -1  # -1 is never returned by hash() in CPython
NULL = object()  # sentinel representing a null pointer


class VisiSet:
    """Set backed by a numpy structured array of (hash: int64, value: object) rows.

    Emulates CPython's set hash table: 8 initial slots, linear probing on collision.
    Empty slots hold hash=-1 and value=NULL.
    """

    _dtype = np.dtype([('hash', np.int64), ('value', object)])
    _INIT_SIZE = 8

    def _make_table(self, size):
        table = np.empty(size, dtype=self._dtype)
        table['hash'][:] = EMPTY_BUCKET
        table['value'][:] = NULL
        return table

    def __init__(self, iterable=()):
        self._table = self._make_table(self._INIT_SIZE)
        self._len = 0
        for item in iterable:
            self.add(item)

    # ---- set interface -------------------------------------------------------

    def _crowded(self):
        """Report whether adding one item makes table > 2/3 full"""
        return (self._len + 1) / len(self._table) > 2 / 3

    def add(self, item, grow=True):
        """Add one item; grow if needed and caller allows"""
        if item in self:
            return
        if grow and self._crowded():
            self._grow()
        h = hash(item)
        idx = int(h % len(self._table))
        while self._table['value'][idx] is not NULL:
            idx = (idx + 1) % len(self._table)
        self._table['hash'][idx] = h
        self._table['value'][idx] = item
        self._len += 1

    def _grow(self):
        """Grow the hash table, re-adding existing elements"""
        current = self._table
        self._table = self._make_table(len(current) * 2)
        self._len = 0
        for row in current:
            if row['value'] is not NULL:
                self.add(row['value'], grow=False)

    def __contains__(self, item):
        idx = int(hash(item) % len(self._table))
        while self._table['value'][idx] is not NULL:
            if self._table['value'][idx] == item:
                return True
            idx = (idx + 1) % len(self._table)
        return False

    def __len__(self):
        return self._len

    def __iter__(self):
        for row in self._table:
            if row['value'] is not NULL:
                yield row['value']

    # ---- display -------------------------------------------------------------

    def __repr__(self):
        """Instances are represented as:

        >>> VisiSet([1, 2, 3])
        VisiSet({1, 2, 3})

        """
        items = ', '.join(repr(v) for v in self)
        return f'VisiSet({{{items}}})'

    def _repr_html_(self):
        rows = []
        n = len(self._table)
        for bucket, row in enumerate(self._table):
            h = row['hash']
            if row['value'] is NULL:
                rows.append(
                    f"<tr class='vs-empty'><td></td><td>{h}</td><td>{NULL_SYMBOL}</td></tr>"
                )
            else:
                slot = h % n
                slot_class = 'vs-displaced' if slot != bucket else 'vs-slot'
                v = repr(row['value'])
                rows.append(f"<tr class='vs-data'><td class='{slot_class}'>{slot}</td><td class='vs-hash'>{h}</td><td class='vs-val'>{POINTER_SYMBOL} {v}</td></tr>")
        return (
            VISISET_CSS
            + "<div class='vs-wrap'>"
            + "<table class='vs-table'>"
            + '<thead><tr><th>%</th><th>hash</th><th>value</th></tr></thead>'
            + '<tbody>'
            + ''.join(rows)
            + '</tbody>'
            + '</table>'
            + '</div>'
        )

POINTER_SYMBOL = '\N{BOX DRAWINGS LIGHT HORIZONTAL}\N{RIGHTWARDS ARROW}'
NULL_SYMBOL = '\N{RISING DIAGONAL CROSSING FALLING DIAGONAL}'

VISISET_CSS = """
<style>
.vs-wrap { font-family: monospace; font-size: 13px; }
.vs-table {
    border-collapse: collapse;
    font-family: monospace;
    font-size: 13px;
}
.vs-table th {
    background: #2b2b2b;
    color: #ddd;
    padding: 3px 6px 3px 6px;
    text-align: right;
    font-weight: normal;
    border: 1px solid #444;
}
.vs-table td {
    padding: 2px 6px 2px 6px;
    text-align: right;
    border: 1px solid #ccc;
}
.vs-table td { background: #fff; }
.vs-table th:nth-child(1), .vs-table td:nth-child(1) { background: #DDD; border-color: #000; }
.vs-table th:nth-child(3), .vs-table td:nth-child(3) { text-align: left; }
.vs-table tr.vs-empty td { color: #bbb; }
.vs-table td.vs-slot, .vs-table td.vs-hash, .vs-table td.vs-val { color: #000; }
.vs-table td.vs-displaced { color: #8b0000; }
</style>
"""
