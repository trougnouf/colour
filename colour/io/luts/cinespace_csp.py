"""
Cinespace .csp LUT Format Input / Output Utilities
==================================================

Defines the *Cinespace* *.csp* *LUT* format related input / output utilities
objects:

-   :func:`colour.io.read_LUT_Cinespace`
-   :func:`colour.io.write_LUT_Cinespace`

References
----------
-   :cite:`RisingSunResearch` : Rising Sun Research. (n.d.). cineSpace LUT
    Library. Retrieved November 30, 2018, from
    https://sourceforge.net/projects/cinespacelutlib/
"""

from __future__ import annotations

import numpy as np

from colour.hints import ArrayLike, List, NDArrayFloat
from colour.io.luts import LUT1D, LUT3x1D, LUT3D, LUTSequence
from colour.utilities import (
    as_float_array,
    as_int_array,
    attest,
    format_array_as_row,
    tsplit,
    tstack,
)

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "read_LUT_Cinespace",
    "write_LUT_Cinespace",
]


def read_LUT_Cinespace(path: str) -> LUT3x1D | LUT3D | LUTSequence:
    """
    Read given *Cinespace* *.csp* *LUT* file.

    Parameters
    ----------
    path
        *LUT* path.

    Returns
    -------
    :class:`colour.LUT3x1D` or :class:`colour.LUT3D` or \
:class:`colour.LUTSequence`
        :class:`LUT3x1D` or :class:`LUT3D` or :class:`LUTSequence` class
        instance.

    References
    ----------
    :cite:`RisingSunResearch`

    Examples
    --------
    Reading a 3x1D *Cinespace* *.csp* *LUT*:

    >>> import os
    >>> path = os.path.join(
    ...     os.path.dirname(__file__),
    ...     "tests",
    ...     "resources",
    ...     "cinespace",
    ...     "ACES_Proxy_10_to_ACES.csp",
    ... )
    >>> print(read_LUT_Cinespace(path))
    LUT3x1D - ACES Proxy 10 to ACES
    -------------------------------
    <BLANKLINE>
    Dimensions : 2
    Domain     : [[ 0.  0.  0.]
                  [ 1.  1.  1.]]
    Size       : (32, 3)

    Reading a 3D *Cinespace* *.csp* *LUT*:

    >>> path = os.path.join(
    ...     os.path.dirname(__file__),
    ...     "tests",
    ...     "resources",
    ...     "cinespace",
    ...     "Colour_Correct.csp",
    ... )
    >>> print(read_LUT_Cinespace(path))
    LUT3D - Generated by Foundry::LUT
    ---------------------------------
    <BLANKLINE>
    Dimensions : 3
    Domain     : [[ 0.  0.  0.]
                  [ 1.  1.  1.]]
    Size       : (4, 4, 4, 3)
    """

    unity_range = np.array([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]])

    def _parse_metadata_section(metadata: list) -> tuple:
        """Parse the metadata at given lines."""

        return (metadata[0], metadata[1:]) if len(metadata) > 0 else ("", [])

    def _parse_domain_section(lines: List[str]) -> NDArrayFloat:
        """Parse the domain at given lines."""

        pre_LUT_size = max(int(lines[i]) for i in [0, 3, 6])
        pre_LUT = [
            as_float_array(lines[i].split()) for i in [1, 2, 4, 5, 7, 8]
        ]

        pre_LUT_padded = []
        for array in pre_LUT:
            if len(array) != pre_LUT_size:
                pre_LUT_padded.append(
                    np.pad(
                        array,
                        (0, pre_LUT_size - array.shape[0]),
                        mode="constant",
                        constant_values=np.nan,
                    )
                )
            else:
                pre_LUT_padded.append(array)

        return np.asarray(pre_LUT_padded)

    def _parse_table_section(lines):
        """Parse the table at given lines."""

        size = as_int_array(lines[0].split())
        table = as_float_array([line.split() for line in lines[1:]])

        return size, table

    with open(path) as csp_file:
        lines = csp_file.readlines()
        attest(len(lines) > 0, '"LUT" is empty!')
        lines = [line.strip() for line in lines if line.strip()]

        header = lines[0]
        attest(header == "CSPLUTV100", '"LUT" header is invalid!')

        kind = lines[1]
        attest(kind in ("1D", "3D"), '"LUT" type must be "1D" or "3D"!')

        is_3D = kind == "3D"

        seek = 2
        metadata = []
        is_metadata = False
        for i, line in enumerate(lines[2:]):
            line = line.strip()  # noqa: PLW2901
            if line == "BEGIN METADATA":
                is_metadata = True
                continue
            elif line == "END METADATA":
                seek += i
                break

            if is_metadata:
                metadata.append(line)

        title, comments = _parse_metadata_section(metadata)

        seek += 1
        pre_LUT = _parse_domain_section(lines[seek : seek + 9])

        seek += 9
        size, table = _parse_table_section(lines[seek:])

        attest(np.prod(size) == len(table), '"LUT" table size is invalid!')

    LUT: LUT3x1D | LUT3D | LUTSequence
    if (
        is_3D
        and pre_LUT.shape == (6, 2)
        and np.array_equal(
            np.transpose(np.reshape(pre_LUT, (3, 4)))[2:4], unity_range
        )
    ):
        table = table.reshape([size[0], size[1], size[2], 3], order="F")
        LUT = LUT3D(
            domain=np.transpose(np.reshape(pre_LUT, (3, 4)))[0:2],
            name=title,
            comments=comments,
            table=table,
        )

    elif (
        not is_3D
        and pre_LUT.shape == (6, 2)
        and np.array_equal(
            np.transpose(np.reshape(pre_LUT, (3, 4)))[2:4], unity_range
        )
    ):
        LUT = LUT3x1D(
            domain=pre_LUT.reshape(3, 4).transpose()[0:2],
            name=title,
            comments=comments,
            table=table,
        )

    elif is_3D:
        pre_domain = tstack((pre_LUT[0], pre_LUT[2], pre_LUT[4]))
        pre_table = tstack((pre_LUT[1], pre_LUT[3], pre_LUT[5]))
        shaper_name = f"{title} - Shaper"
        cube_name = f"{title} - Cube"
        table = table.reshape([size[0], size[1], size[2], 3], order="F")

        LUT = LUTSequence(
            LUT3x1D(pre_table, shaper_name, pre_domain),
            LUT3D(table, cube_name, comments=comments),
        )

    elif not is_3D:
        pre_domain = tstack((pre_LUT[0], pre_LUT[2], pre_LUT[4]))
        pre_table = tstack((pre_LUT[1], pre_LUT[3], pre_LUT[5]))

        if table.shape == (2, 3):
            table_max = table[1]
            table_min = table[0]
            pre_table *= table_max - table_min
            pre_table += table_min

            LUT = LUT3x1D(pre_table, title, pre_domain, comments=comments)
        else:
            pre_name = f"{title} - PreLUT"
            table_name = f"{title} - Table"

            LUT = LUTSequence(
                LUT3x1D(pre_table, pre_name, pre_domain),
                LUT3x1D(table, table_name, comments=comments),
            )

    return LUT


def write_LUT_Cinespace(
    LUT: LUT3x1D | LUT3D | LUTSequence, path: str, decimals: int = 7
) -> bool:
    """
    Write given *LUT* to given  *Cinespace* *.csp* *LUT* file.

    Parameters
    ----------
    LUT
        :class:`LUT1D`, :class:`LUT3x1D` or :class:`LUT3D` or
        :class:`LUTSequence` class instance to write at given path.
    path
        *LUT* path.
    decimals
        Formatting decimals.

    Returns
    -------
    :class:`bool`
        Definition success.

    References
    ----------
    :cite:`RisingSunResearch`

    Examples
    --------
    Writing a 3x1D *Cinespace* *.csp* *LUT*:

    >>> from colour.algebra import spow
    >>> domain = np.array([[-0.1, -0.2, -0.4], [1.5, 3.0, 6.0]])
    >>> LUT = LUT3x1D(
    ...     spow(LUT3x1D.linear_table(16, domain), 1 / 2.2),
    ...     "My LUT",
    ...     domain,
    ...     comments=["A first comment.", "A second comment."],
    ... )
    >>> write_LUT_Cinespace(LUT, "My_LUT.cube")  # doctest: +SKIP

    Writing a 3D *Cinespace* *.csp* *LUT*:

    >>> domain = np.array([[-0.1, -0.2, -0.4], [1.5, 3.0, 6.0]])
    >>> LUT = LUT3D(
    ...     spow(LUT3D.linear_table(16, domain), 1 / 2.2),
    ...     "My LUT",
    ...     domain,
    ...     comments=["A first comment.", "A second comment."],
    ... )
    >>> write_LUT_Cinespace(LUT, "My_LUT.cube")  # doctest: +SKIP
    """

    has_3D, has_3x1D = False, False

    if isinstance(LUT, LUTSequence):
        attest(
            len(LUT) == 2
            and isinstance(LUT[0], (LUT1D, LUT3x1D))
            and isinstance(LUT[1], LUT3D),
            '"LUTSequence" must be "1D + 3D" or "3x1D + 3D"!',
        )
        LUT[0] = (
            LUT[0].convert(LUT3x1D) if isinstance(LUT[0], LUT1D) else LUT[0]
        )
        name = f"{LUT[0].name} - {LUT[1].name}"
        has_3x1D = True
        has_3D = True

    elif isinstance(LUT, LUT1D):
        name = LUT.name
        has_3x1D = True
        LUT = LUTSequence(LUT.convert(LUT3x1D), LUT3D())

    elif isinstance(LUT, LUT3x1D):
        name = LUT.name
        has_3x1D = True
        LUT = LUTSequence(LUT, LUT3D())

    elif isinstance(LUT, LUT3D):
        name = LUT.name
        has_3D = True
        LUT = LUTSequence(LUT3x1D(), LUT)

    else:
        raise TypeError("LUT must be 1D, 3x1D, 3D, 1D + 3D or 3x1D + 3D!")

    if has_3x1D:
        attest(
            2 <= LUT[0].size <= 65536,
            "Shaper size must be in domain [2, 65536]!",
        )
    if has_3D:
        attest(
            2 <= LUT[1].size <= 256, "Cube size must be in domain [2, 256]!"
        )

    def _ragged_size(table: ArrayLike) -> list:
        """Return the ragged size of given table."""

        R, G, B = tsplit(table)

        R_len = R.shape[-1] - np.sum(np.isnan(R))
        G_len = G.shape[-1] - np.sum(np.isnan(G))
        B_len = B.shape[-1] - np.sum(np.isnan(B))

        return [R_len, G_len, B_len]

    with open(path, "w") as csp_file:
        csp_file.write("CSPLUTV100\n")

        if has_3D:
            csp_file.write("3D\n\n")
        else:
            csp_file.write("1D\n\n")

        csp_file.write("BEGIN METADATA\n")
        csp_file.write(f"{name}\n")

        if LUT[0].comments:
            for comment in LUT[0].comments:
                csp_file.write(f"{comment}\n")

        if LUT[1].comments:
            for comment in LUT[1].comments:
                csp_file.write(f"{comment}\n")

        csp_file.write("END METADATA\n\n")

        if has_3D:
            if has_3x1D:
                for i in range(3):
                    size = (
                        _ragged_size(LUT[0].domain)[i]
                        if LUT[0].is_domain_explicit()
                        else LUT[0].size
                    )

                    csp_file.write(f"{size}\n")

                    for j in range(size):
                        entry = (
                            LUT[0].domain[j][i]
                            if LUT[0].is_domain_explicit()
                            else (
                                LUT[0].domain[0][i]
                                + j
                                * (LUT[0].domain[1][i] - LUT[0].domain[0][i])
                                / (LUT[0].size - 1)
                            )
                        )

                        csp_file.write(
                            f"{format_array_as_row(entry, decimals)} "
                        )

                    csp_file.write("\n")

                    for j in range(size):
                        entry = LUT[0].table[j][i]
                        csp_file.write(
                            f"{format_array_as_row(entry, decimals)} "
                        )

                    csp_file.write("\n")
            else:
                for i in range(3):
                    csp_file.write("2\n")
                    domain = format_array_as_row(
                        [LUT[1].domain[0][i], LUT[1].domain[1][i]], decimals
                    )
                    csp_file.write(f"{domain}\n")
                    csp_file.write(
                        f"{format_array_as_row([0, 1], decimals)}\n"
                    )

            csp_file.write(
                f"\n{LUT[1].table.shape[0]} "
                f"{LUT[1].table.shape[1]} "
                f"{LUT[1].table.shape[2]}\n"
            )
            table = LUT[1].table.reshape([-1, 3], order="F")

            for array in table:
                csp_file.write(f"{format_array_as_row(array, decimals)}\n")
        else:
            for i in range(3):
                csp_file.write("2\n")
                domain = format_array_as_row(
                    [LUT[0].domain[0][i], LUT[0].domain[1][i]], decimals
                )
                csp_file.write(f"{domain}\n")
                csp_file.write("0.0 1.0\n")
            csp_file.write(f"\n{LUT[0].size}\n")
            table = LUT[0].table

            for array in table:
                csp_file.write(f"{format_array_as_row(array, decimals)}\n")

    return True
