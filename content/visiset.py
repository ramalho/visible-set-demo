from hashtable import HashTable, NULL

DEFAULT_HASH_FORMAT_BASE = 16


class VisiSet:
    """Set backed by a HashTable with (hash, value) rows."""

    def __init__(self, iterable=(), fmt_base=DEFAULT_HASH_FORMAT_BASE):
        self._fmt_base = fmt_base
        self._hashtable = HashTable()
        self.update(iterable)

    def update(self, *others):
        for other in others:
            for element in other:
                self._hashtable.insert(element)

    # ---- set interface -------------------------------------------------------

    def add(self, element):
        self._hashtable.insert(element)

    def __contains__(self, element):
        return element in self._hashtable

    def __len__(self):
        return len(self._hashtable)

    def __iter__(self):
        return iter(self._hashtable)

    def union(self, *others):
        result = VisiSet(self, fmt_base=self._fmt_base)
        result.update(*others)
        return result

    # ---- display -------------------------------------------------------------

    def _fmt_hash(self, h):
        if self._fmt_base == 10:
            return str(int(h))
        width = self._hashtable.hash_width
        fmt = f'{width}b' if self._fmt_base == 2 else f'{width // 4}x'
        mask = (1 << width) - 1
        return f'{int(h) & mask:{fmt}}'

    def __repr__(self):
        """Instances are represented as:

        >>> VisiSet([1, 2, 3])
        VisiSet({1, 2, 3})

        """
        elements = ', '.join(repr(v) for v in self)
        return f'VisiSet({{{elements}}})'

    def _repr_html_(self):
        rows = []
        table = self._hashtable._table
        n = len(table)
        for bucket, row in enumerate(table):
            h = row['hash']
            h_str = self._fmt_hash(h)
            if row['value'] is NULL:
                rows.append(
                    f'<tr class="vs-empty"><td></td><td>{h_str}</td><td>{NULL_SYMBOL}</td></tr>'
                )
            else:
                slot = h % n
                slot_class = 'vs-displaced' if slot != bucket else 'vs-slot'
                v = repr(row['value'])
                rows.append(
                    f'<tr class="vs-data"><td class="{slot_class}">{slot}</td>'
                    f'<td class="vs-hash">{h_str}</td><td class="vs-val">{POINTER_SYMBOL} {v}</td></tr>'
                )
        return (
            VISISET_CSS
            + '<div class="vs-wrap">'
            + '<table class="vs-table">'
            + f'<thead><tr><th>%</th><th>{self._hashtable.hash_width}-bit hash</th><th>pointer to value</th></tr></thead>'
            + '<tbody>'
            + ''.join(rows)
            + '</tbody>'
            + '</table>'
            + '</div>'
        )


POINTER_SYMBOL = '\N{RIGHTWARDS TRIANGLE-HEADED ARROW}'
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
    color: #fff;
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
.vs-table th:nth-child(1), .vs-table td:nth-child(1) { background: #DDD; border-color: #000; color: #000; }
.vs-table th:nth-child(3), .vs-table td:nth-child(3) { text-align: left; }
.vs-table tr.vs-empty td { color: #bbb; }
.vs-table td.vs-slot, .vs-table td.vs-hash, .vs-table td.vs-val { color: #000; }
.vs-table td.vs-displaced { color: #8b0000; }
</style>
"""
