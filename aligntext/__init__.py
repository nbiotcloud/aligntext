#
# MIT License
#
# Copyright (c) 2023 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""
Text Align - Python Text Alignment.
"""
import types
from itertools import zip_longest as _zip_longest


def align(
    *rows, seps=None, sepfirst=None, seplast=None, alignments=None, rtrim=True, strip_empty_cols=False, header=None
):
    r"""
    Align `rows` using separators `seps` and align to `alignments`.

    Keyword Args:
        seps (list, tuple): separators (see :any:`set_separators()`).
        sepfirst (str): prefix for every row. Empty by default. (see :any:`set_separators()`).
        seplast (str): suffix for every row. Empty by default. (see :any:`set_separators()`).
        alignments (list, tuple): alignments (see :any:`set_alignments()`).
        rtrim (bool): Remove whitespaces at the end of the line.
        strip_empty_cols (bool): Skip the column and the seperator of empty columns.

    >>> print(align([["a", "bb", "ccc"], ["zzz", "yyyy", "x"]], rtrim=True))
    a   bb   ccc
    zzz yyyy x

    >>> print(align([["a", "bb", "ccc"], ["zzz", "yyyy", "x"]], header=('Col1', 'C2', 'Column3'),
    ...       rtrim=True))
    Col1 C2   Column3
    ---- --   -------
    a    bb   ccc
    zzz  yyyy x

    >>> print(align(["a", "bb", "ccc"], ["zzz", "yyyy", "x"], seps=["|"], sepfirst="B", seplast="E",
    ...       rtrim=True))
    Ba  |bb  |cccE
    Bzzz|yyyy|x  E

    >>> print(align(["a", "bb", "ccc"], ["zzz", "yyyy", "x"], alignments=(center, right), rtrim=True))
     a    bb ccc
    zzz yyyy   x

    Generators are also allowed:

    >>> def myiter(num):
    ...     for idx in range(num):
    ...         yield idx
    >>> def myiteriter(rows, cols):
    ...     for idx in range(rows):
    ...         yield myiter(cols)
    >>> align(myiteriter(2, 3))
    '0 1 2\n0 1 2'
    """
    inst = Align(rtrim=rtrim, strip_empty_cols=strip_empty_cols)
    if header:
        header = tuple(header)
        inst.add_row(header)
        inst.add_row(("-" * max(len(cellrow) for cellrow in cell.split("\n")) for cell in header))
    inst.add_rows(*rows)
    if seps is None:
        inst.set_separators(first=sepfirst, last=seplast)
    else:
        inst.set_separators(*seps, first=sepfirst, last=seplast)
    if alignments:
        inst.set_alignments(*alignments)
    return inst.get()


def iter_align(*rows, seps=None, sepfirst=None, seplast=None, alignments=None, rtrim=True, strip_empty_cols=False):
    r"""
    Iterate over aligned `rows` using separators `seps` and align to `alignments`.

    Keyword Args:
        seps (list, tuple): separators (see :any:`set_separators()`).
        sepfirst (str): prefix for every row. Empty by default. (see :any:`set_separators()`).
        seplast (str): suffix for every row. Empty by default. (see :any:`set_separators()`).
        alignments (list, tuple): alignments (see :any:`set_alignments()`).
        rtrim (bool): Remove whitespaces at the end of the line.
        strip_empty_cols (bool): Skip the column and the seperator of empty columns.

    >>> '\n'.join(iter_align([["a", "bb", "ccc"], ["zzz", "yyyy", "x"]]))
    'a   bb   ccc\nzzz yyyy x'

    >>> '\n'.join(iter_align(["a", "bb", "ccc"], ["zzz", "yyyy", "x"], seps=["|"], sepfirst="B", seplast="E"))
    'Ba  |bb  |cccE\nBzzz|yyyy|x  E'

    >>> '\n'.join(iter_align(["a", "bb", "ccc"], ["zzz", "yyyy", "x"], alignments=(center, right)))
    ' a    bb ccc\nzzz yyyy   x'

    Generators are also allowed:

    >>> def myiter(num):
    ...     for idx in range(num):
    ...         yield idx
    >>> def myiteriter(rows, cols):
    ...     for idx in range(rows):
    ...         yield myiter(cols)
    >>> '\n' .join(iter_align(myiteriter(2, 3)))
    '0 1 2\n0 1 2'
    """
    inst = Align(rtrim=rtrim, strip_empty_cols=strip_empty_cols)
    inst.add_rows(*rows)
    if seps is None:
        inst.set_separators(first=sepfirst, last=seplast)
    else:
        inst.set_separators(*seps, first=sepfirst, last=seplast)
    if alignments:
        inst.set_alignments(*alignments)
    return iter(inst)


class Align:
    """
    Align table data.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, rtrim=False, strip_empty_cols=False):
        r"""
        Align table data.

        Keyword Arguments:
            rtrim (bool): Remove whitespaces at the end of the line.
            strip_empty_cols (bool): Skip the column and the seperator of empty columns.

        Example:
        >>> al = Align()

        Data is added via :any:`add_rows()` or via :any:`add_row()`:

        >>> al.add_rows([[1, 33, 1.001],
        ...              ["foo", "barcelona", "tschustify"],
        ...             ])
        >>> al.add_row(None, "None")

        The aligned content is served by :any:`get()` or by iteration:

        >>> al.get()
        '1   33        1.001     \nfoo barcelona tschustify\n    None                '
        >>> for row in al:
        ...     row
        '1   33        1.001     '
        'foo barcelona tschustify'
        '    None                '

        Trailing whitespaces can be disabled via:

        >>> al.rtrim=True
        >>> for row in al:
        ...     row
        '1   33        1.001'
        'foo barcelona tschustify'
        '    None'

        The `len()` function will retrun the current filling level.

        >>> al.clear()
        >>> al.get()
        ''
        >>> len(al)
        0
        >>> al.add_row(1, 2, 3)
        >>> al.get()
        '1 2 3'
        >>> len(al)
        1

        Empty columns can be collapsed on request:

        >>> al = Align()
        >>> al.add_row("a", None, "cc")
        >>> al.add_row("ddd", "", "f")
        >>> for row in al:
        ...     row
        'a    cc'
        'ddd  f '
        >>> al.strip_empty_cols = True
        >>> for row in al:
        ...     row
        'a   cc'
        'ddd f '

        Also multiline cells are supported:

        >>> al = Align()
        >>> al.add_row("a\nbb", "ccc")
        >>> al.add_row("ddd", "\nlonger")
        >>> for row in al:
        ...     row
        'a   ccc   '
        'bb        '
        'ddd       '
        '    longer'
        """
        super().__init__()
        self._separators = []
        self._sepfirst = None
        self._seplast = None
        self.rtrim = rtrim
        self.strip_empty_cols = strip_empty_cols
        self._alignments = [left]
        self._rows = []
        self._maxcols = 0

    def add_rows(self, *rows):
        """
        Add `rows`.

        Rows are accepted as `tuple`, `list` or positional arguments.

        The data is always extended to the width of the broadest row.

        >>> al = Align()
        >>> al.add_rows([[11, 12, 13], [14, 15, 16]])  # list of lists
        >>> al.add_rows(((21, 22, 23), (24, 25, 26)))  # tuple of tuples
        >>> al.add_rows((31, 32, 33), [34, 35, 36])    # positional arguments
        >>> for row in al:
        ...     row
        '11 12 13'
        '14 15 16'
        '21 22 23'
        '24 25 26'
        '31 32 33'
        '34 35 36'
        """
        for row in _iter_items(rows):
            self._add_row(row)

    def add_row(self, *cols):
        """
        Add a row with `cols`.

        Column values are accepted as `tuple`, `list` or positional arguments.

        The data is always extended to the width of the broadest row.

        >>> al = Align()
        >>> al.add_row([1, 2, 3])     # list
        >>> al.add_row((4, 5, 6, 7))  # tuple
        >>> al.add_row(8, 9, 10)      # positional arguments
        >>> for row in al:
        ...     row
        '1 2 3   '
        '4 5 6  7'
        '8 9 10  '
        """
        self._add_row(_iter_items(cols))

    def _add_row(self, cols):
        normedcols = [self.norm(cell) for cell in cols]
        self._rows.append((True, normedcols))
        self._maxcols = max(len(normedcols), self._maxcols)

    def add_spacers(self, *spacers):
        """
        Add unaligned `spacers`.

        >>> al = Align()
        >>> al.add_row(111, 12, 13)
        >>> al.add_spacers("---", None)
        >>> al.add_row(31, 321, 33)
        >>> al.add_spacers("===============")
        >>> al.add_row(21, 22, 231)
        >>> for row in al:
        ...     row
        '111 12  13 '
        '---'
        ''
        '31  321 33 '
        '==============='
        '21  22  231'
        """
        for spacer in spacers:
            self._add_spacer(spacer)

    def add_spacer(self, spacer=None):
        """
        Add unaligned `spacer`.

        >>> al = Align(rtrim=True)
        >>> al.add_row(111, 12, 13)
        >>> al.add_spacer()
        >>> al.add_row(31, 321, 33)
        >>> al.add_spacer("===============")
        >>> al.add_row(21, 22, 231)
        >>> for row in al:
        ...     row
        '111 12  13'
        ''
        '31  321 33'
        '==============='
        '21  22  231'
        """
        self._add_spacer(spacer)

    def _add_spacer(self, spacer):
        if spacer is None:
            spacer = ""
        self._rows.append((False, spacer))

    def clear(self):
        """Remove *all* added rows."""
        self._rows = []
        self._maxcols = 0

    def get(self):
        """Return aligned data."""
        return "\n".join(self._get())

    def set_separators(self, *separators, first=None, last=None, rtrim=None):
        """
        Set the column separators.

        Args:
            *separators (str): separators. Default is " ".

        Keyword Args:
            first (str): prefix for every row. Empty by default.
            last (str): suffix for every row. Empty by default.
            rtrim: Remove whitespaces at the end of the line. Do not change setting by default.

        If there are less separators specified than columns available, the last
        alignment is used for all remaining columns.
        If there are more separators specified than columns available, the
        dispensable ones are ignored.

        Example:
        >>> al = Align()
        >>> al.add_rows(["a", "bb", "ccc"], ["zz", "yyyy", "x"])
        >>> al.set_separators("|", rtrim=True)
        >>> for row in al:
        ...     row
        'a |bb  |ccc'
        'zz|yyyy|x'

        >>> al.set_separators("|", "=", "&")
        >>> for row in al:
        ...     row
        'a |bb  =ccc&'
        'zz|yyyy=x  &'

        >>> al.set_separators("|", first="> ", last=" <")
        >>> for row in al:
        ...     row
        '> a |bb  |ccc <'
        '> zz|yyyy|x   <'


        >>> al.set_separators("|", "=", "&", last="END")
        >>> for row in al:
        ...     row
        'a |bb  =cccEND'
        'zz|yyyy=x  END'
        """
        self._separators = separators
        self._sepfirst = first
        self._seplast = last
        if rtrim is not None:
            self.rtrim = rtrim

    def set_alignments(self, *alignments):
        """
        Set the alignment for every column.

        All left aligned is the default.

        If there are less alignments specified than columns available, the last
        alignment is used for all remaining columns.
        If there are more alignments specified than columns available, the
        dispensable ones are ignored.

        Alignments shall be `left`, `center`, `right` or any function with the
        arguments `cell`, `width`, which returns an aligned string.

        Example:
        >>> al = Align()
        >>> al.add_rows([[1, 33, 1.001],
        ...              ["foo", "barcelona", "tschustify"],
        ...             ])
        >>> al.set_alignments(center)
        >>> for row in al:
        ...     row
        ' 1      33      1.001   '
        'foo barcelona tschustify'

        >>> al.set_alignments(center, right)
        >>> for row in al:
        ...     row
        ' 1         33      1.001'
        'foo barcelona tschustify'

        >>> al.set_alignments(center, right, left, right)
        >>> for row in al:
        ...     row
        ' 1         33 1.001     '
        'foo barcelona tschustify'

        >>> al.set_alignments()
        >>> for row in al:
        ...     row
        '1   33        1.001     '
        'foo barcelona tschustify'
        """
        self._alignments = alignments

    @staticmethod
    def norm(cell):
        """
        Normalize function for any table `cell`.

        Return an empty string, when `cell` is None, otherwise
        convert `cell` to string.

        This static method can be overwritten to implement any other type behaviour.
        """
        if cell is None:
            return ""
        return str(cell)

    def __iter__(self):
        yield from self._get()

    def _get(self):
        # filter out all rows to be aligned
        rows = self._rows
        alignrows = [row for align, row in rows if align]
        widths = [
            max(max(len(cellrow) for cellrow in cell.split("\n")) for cell in col)
            for col in _zip_longest(*alignrows, fillvalue="")
        ]
        sepfirst, separators = self._get_separators()
        alignments = self._get_alignments()
        collapse = self.strip_empty_cols
        for rowalign, row in rows:
            if rowalign:
                subrows = list(_zip_longest(*[cell.split("\n") for cell in row], fillvalue=""))
                for subrow in subrows:
                    items = _zip_longest(alignments, subrow, widths, separators, fillvalue="")
                    line = sepfirst + "".join(
                        [alignment(cell, width) + sep for alignment, cell, width, sep in items if width or not collapse]
                    )
                    if self.rtrim:
                        line = line.rstrip()
                    yield line
            else:
                line = row
                if self.rtrim:
                    line = line.rstrip()
                yield line

    def _get_separators(self):
        sepfirst = self.norm(self._sepfirst)
        separators = [self.norm(sep) for sep in self._separators]
        if not separators:
            separators = [" "]
        seplast = self._seplast
        colslen = self._maxcols
        missing = colslen - len(separators)
        if missing > 0:
            separators = separators + separators[-1:] * (missing - 1) + [self.norm(seplast)]
        elif seplast is not None:
            separators = separators[: colslen - 1] + [self.norm(seplast)]
        else:
            separators = separators[:colslen]
        return sepfirst, separators

    def _get_alignments(self):
        alignments = self._alignments
        if not alignments:
            alignments = [left]
        colslen = self._maxcols
        missing = colslen - len(alignments)
        if missing > 0:
            return alignments + alignments[-1:] * missing
        return alignments[:colslen]

    def __len__(self):
        return len(self._rows)


def left(cell, width):
    """Justify `cell` to left with `width`."""
    return cell.ljust(width)


def center(cell, width):
    """Center `cell` to `width`."""
    return cell.center(width)


def right(cell, width):
    """Justify `cell` to right with `width`."""
    return cell.rjust(width)


def _iter_items(args):
    """Iterate over items in `args`."""
    if len(args) == 1 and isinstance(args[0], (tuple, list, types.GeneratorType)):
        items = args[0]
    else:
        items = args
    for item in items:
        yield item
