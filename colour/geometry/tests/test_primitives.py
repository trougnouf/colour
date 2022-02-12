"""Defines the unit tests for the :mod:`colour.geometry.primitives` module."""

import numpy as np
import unittest

from colour.geometry import (
    MAPPING_PLANE_TO_AXIS,
    primitive_grid,
    primitive_cube,
)

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "New BSD License - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestPrimitiveGrid",
    "TestPrimitiveCube",
]


class TestPrimitiveGrid(unittest.TestCase):
    """
    Define :func:`colour.geometry.primitives.primitive_grid`
    definition unit tests methods.
    """

    def test_primitive_grid(self):
        """
        Test :func:`colour.geometry.primitives.primitive_grid`
        definition.
        """

        vertices, faces, outline = primitive_grid()
        np.testing.assert_almost_equal(
            vertices["position"],
            np.array(
                [
                    [-0.5, 0.5, 0.0],
                    [0.5, 0.5, 0.0],
                    [-0.5, -0.5, 0.0],
                    [0.5, -0.5, 0.0],
                ]
            ),
            decimal=7,
        )

        np.testing.assert_almost_equal(
            vertices["uv"],
            np.array([[0, 1], [1, 1], [0, 0], [1, 0]]),
            decimal=7,
        )

        np.testing.assert_almost_equal(
            vertices["normal"],
            np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]]),
            decimal=7,
        )

        np.testing.assert_almost_equal(
            vertices["colour"],
            np.array(
                [
                    [0, 1, 0, 1],
                    [1, 1, 0, 1],
                    [0, 0, 0, 1],
                    [1, 0, 0, 1],
                ]
            ),
            decimal=7,
        )

        np.testing.assert_equal(faces, np.array([[0, 2, 1], [2, 3, 1]]))

        np.testing.assert_equal(
            outline, np.array([[0, 2], [2, 3], [3, 1], [1, 0]])
        )

        vertices, faces, outline = primitive_grid(
            width=0.2,
            height=0.4,
            width_segments=1,
            height_segments=2,
            axis="+z",
        )

        np.testing.assert_almost_equal(
            vertices["position"],
            np.array(
                [
                    [-0.10000000, 0.20000000, 0.00000000],
                    [0.10000000, 0.20000000, 0.00000000],
                    [-0.10000000, -0.00000000, 0.00000000],
                    [0.10000000, -0.00000000, 0.00000000],
                    [-0.10000000, -0.20000000, 0.00000000],
                    [0.10000000, -0.20000000, 0.00000000],
                ]
            ),
            decimal=7,
        )

        np.testing.assert_almost_equal(
            vertices["uv"],
            np.array(
                [
                    [0.00000000, 1.00000000],
                    [1.00000000, 1.00000000],
                    [0.00000000, 0.50000000],
                    [1.00000000, 0.50000000],
                    [0.00000000, 0.00000000],
                    [1.00000000, 0.00000000],
                ]
            ),
            decimal=7,
        )

        np.testing.assert_almost_equal(
            vertices["normal"],
            np.array(
                [
                    [0, 0, 1],
                    [0, 0, 1],
                    [0, 0, 1],
                    [0, 0, 1],
                    [0, 0, 1],
                    [0, 0, 1],
                ]
            ),
            decimal=7,
        )

        np.testing.assert_almost_equal(
            vertices["colour"],
            np.array(
                [
                    [0.25000000, 1.00000000, 0.00000000, 1.00000000],
                    [0.75000000, 1.00000000, 0.00000000, 1.00000000],
                    [0.25000000, 0.50000000, 0.00000000, 1.00000000],
                    [0.75000000, 0.50000000, 0.00000000, 1.00000000],
                    [0.25000000, 0.00000000, 0.00000000, 1.00000000],
                    [0.75000000, 0.00000000, 0.00000000, 1.00000000],
                ]
            ),
            decimal=7,
        )

        np.testing.assert_equal(
            faces,
            np.array(
                [
                    [0, 2, 1],
                    [2, 3, 1],
                    [2, 4, 3],
                    [4, 5, 3],
                ]
            ),
        )

        np.testing.assert_equal(
            outline,
            np.array(
                [
                    [0, 2],
                    [2, 3],
                    [3, 1],
                    [1, 0],
                    [2, 4],
                    [4, 5],
                    [5, 3],
                    [3, 2],
                ]
            ),
        )

        for plane in MAPPING_PLANE_TO_AXIS.keys():
            np.testing.assert_almost_equal(
                primitive_grid(axis=plane)[0]["position"],
                primitive_grid(axis=MAPPING_PLANE_TO_AXIS[plane])[0][
                    "position"
                ],
                decimal=7,
            )


class TestPrimitiveCube(unittest.TestCase):
    """
    Define :func:`colour.geometry.primitives.primitive_cube`
    definition unit tests methods.
    """

    def test_primitive_cube(self):
        """
        Test :func:`colour.geometry.primitives.primitive_cube`
        definition.
        """

        vertices, faces, outline = primitive_cube()
        np.testing.assert_almost_equal(
            vertices["position"],
            np.array(
                [
                    [-0.5, 0.5, -0.5],
                    [0.5, 0.5, -0.5],
                    [-0.5, -0.5, -0.5],
                    [0.5, -0.5, -0.5],
                    [-0.5, 0.5, 0.5],
                    [0.5, 0.5, 0.5],
                    [-0.5, -0.5, 0.5],
                    [0.5, -0.5, 0.5],
                    [0.5, -0.5, -0.5],
                    [0.5, -0.5, 0.5],
                    [-0.5, -0.5, -0.5],
                    [-0.5, -0.5, 0.5],
                    [0.5, 0.5, -0.5],
                    [0.5, 0.5, 0.5],
                    [-0.5, 0.5, -0.5],
                    [-0.5, 0.5, 0.5],
                    [-0.5, -0.5, 0.5],
                    [-0.5, 0.5, 0.5],
                    [-0.5, -0.5, -0.5],
                    [-0.5, 0.5, -0.5],
                    [0.5, -0.5, 0.5],
                    [0.5, 0.5, 0.5],
                    [0.5, -0.5, -0.5],
                    [0.5, 0.5, -0.5],
                ]
            ),
            decimal=7,
        )

        np.testing.assert_almost_equal(
            vertices["uv"],
            np.array(
                [
                    [0, 1],
                    [1, 1],
                    [0, 0],
                    [1, 0],
                    [0, 1],
                    [1, 1],
                    [0, 0],
                    [1, 0],
                    [0, 1],
                    [1, 1],
                    [0, 0],
                    [1, 0],
                    [0, 1],
                    [1, 1],
                    [0, 0],
                    [1, 0],
                    [0, 1],
                    [1, 1],
                    [0, 0],
                    [1, 0],
                    [0, 1],
                    [1, 1],
                    [0, 0],
                    [1, 0],
                ]
            ),
            decimal=7,
        )

        np.testing.assert_almost_equal(
            vertices["normal"],
            np.array(
                [
                    [0, 0, -1.0],
                    [0, 0, -1],
                    [0, 0, -1],
                    [0, 0, -1],
                    [0, 0, 1],
                    [0, 0, 1],
                    [0, 0, 1],
                    [0, 0, 1],
                    [0, -1, 0],
                    [0, -1, 0],
                    [0, -1, 0],
                    [0, -1, 0],
                    [0, 1, 0],
                    [0, 1, 0],
                    [0, 1, 0],
                    [0, 1, 0],
                    [-1, 0, 0],
                    [-1, 0, 0],
                    [-1, 0, 0],
                    [-1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0],
                ]
            ),
            decimal=7,
        )

        np.testing.assert_almost_equal(
            vertices["colour"],
            np.array(
                [
                    [0, 1, 0, 1],
                    [1, 1, 0, 1],
                    [0, 0, 0, 1],
                    [1, 0, 0, 1],
                    [0, 1, 1, 1],
                    [1, 1, 1, 1],
                    [0, 0, 1, 1],
                    [1, 0, 1, 1],
                    [1, 0, 0, 1],
                    [1, 0, 1, 1],
                    [0, 0, 0, 1],
                    [0, 0, 1, 1],
                    [1, 1, 0, 1],
                    [1, 1, 1, 1],
                    [0, 1, 0, 1],
                    [0, 1, 1, 1],
                    [0, 0, 1, 1],
                    [0, 1, 1, 1],
                    [0, 0, 0, 1],
                    [0, 1, 0, 1],
                    [1, 0, 1, 1],
                    [1, 1, 1, 1],
                    [1, 0, 0, 1],
                    [1, 1, 0, 1],
                ]
            ),
            decimal=7,
        )

        np.testing.assert_equal(
            faces,
            np.array(
                [
                    [1, 2, 0],
                    [1, 3, 2],
                    [4, 6, 5],
                    [6, 7, 5],
                    [9, 10, 8],
                    [9, 11, 10],
                    [12, 14, 13],
                    [14, 15, 13],
                    [17, 18, 16],
                    [17, 19, 18],
                    [20, 22, 21],
                    [22, 23, 21],
                ]
            ),
        )

        np.testing.assert_equal(
            outline,
            np.array(
                [
                    [0, 2],
                    [2, 3],
                    [3, 1],
                    [1, 0],
                    [4, 6],
                    [6, 7],
                    [7, 5],
                    [5, 4],
                    [8, 10],
                    [10, 11],
                    [11, 9],
                    [9, 8],
                    [12, 14],
                    [14, 15],
                    [15, 13],
                    [13, 12],
                    [16, 18],
                    [18, 19],
                    [19, 17],
                    [17, 16],
                    [20, 22],
                    [22, 23],
                    [23, 21],
                    [21, 20],
                ]
            ),
        )

        vertices, faces, outline = primitive_cube(
            width=0.2,
            height=0.4,
            depth=0.6,
            width_segments=1,
            height_segments=2,
            depth_segments=3,
        )

        np.testing.assert_almost_equal(
            vertices["position"],
            np.array(
                [
                    [-0.10000000, 0.30000001, -0.20000000],
                    [0.10000000, 0.30000001, -0.20000000],
                    [-0.10000000, 0.10000000, -0.20000000],
                    [0.10000000, 0.10000000, -0.20000000],
                    [-0.10000000, -0.10000000, -0.20000000],
                    [0.10000000, -0.10000000, -0.20000000],
                    [-0.10000000, -0.30000001, -0.20000000],
                    [0.10000000, -0.30000001, -0.20000000],
                    [-0.10000000, 0.30000001, 0.20000000],
                    [0.10000000, 0.30000001, 0.20000000],
                    [-0.10000000, 0.10000000, 0.20000000],
                    [0.10000000, 0.10000000, 0.20000000],
                    [-0.10000000, -0.10000000, 0.20000000],
                    [0.10000000, -0.10000000, 0.20000000],
                    [-0.10000000, -0.30000001, 0.20000000],
                    [0.10000000, -0.30000001, 0.20000000],
                    [0.10000000, -0.30000001, -0.20000000],
                    [0.10000000, -0.30000001, 0.00000000],
                    [0.10000000, -0.30000001, 0.20000000],
                    [-0.10000000, -0.30000001, -0.20000000],
                    [-0.10000000, -0.30000001, 0.00000000],
                    [-0.10000000, -0.30000001, 0.20000000],
                    [0.10000000, 0.30000001, -0.20000000],
                    [0.10000000, 0.30000001, 0.00000000],
                    [0.10000000, 0.30000001, 0.20000000],
                    [-0.10000000, 0.30000001, -0.20000000],
                    [-0.10000000, 0.30000001, 0.00000000],
                    [-0.10000000, 0.30000001, 0.20000000],
                    [-0.10000000, -0.30000001, 0.20000000],
                    [-0.10000000, -0.10000000, 0.20000000],
                    [-0.10000000, 0.10000000, 0.20000000],
                    [-0.10000000, 0.30000001, 0.20000000],
                    [-0.10000000, -0.30000001, -0.00000000],
                    [-0.10000000, -0.10000000, -0.00000000],
                    [-0.10000000, 0.10000000, -0.00000000],
                    [-0.10000000, 0.30000001, -0.00000000],
                    [-0.10000000, -0.30000001, -0.20000000],
                    [-0.10000000, -0.10000000, -0.20000000],
                    [-0.10000000, 0.10000000, -0.20000000],
                    [-0.10000000, 0.30000001, -0.20000000],
                    [0.10000000, -0.30000001, 0.20000000],
                    [0.10000000, -0.10000000, 0.20000000],
                    [0.10000000, 0.10000000, 0.20000000],
                    [0.10000000, 0.30000001, 0.20000000],
                    [0.10000000, -0.30000001, -0.00000000],
                    [0.10000000, -0.10000000, -0.00000000],
                    [0.10000000, 0.10000000, -0.00000000],
                    [0.10000000, 0.30000001, -0.00000000],
                    [0.10000000, -0.30000001, -0.20000000],
                    [0.10000000, -0.10000000, -0.20000000],
                    [0.10000000, 0.10000000, -0.20000000],
                    [0.10000000, 0.30000001, -0.20000000],
                ]
            ),
            decimal=7,
        )

        np.testing.assert_almost_equal(
            vertices["uv"],
            np.array(
                [
                    [0.00000000, 1.00000000],
                    [1.00000000, 1.00000000],
                    [0.00000000, 0.66666669],
                    [1.00000000, 0.66666669],
                    [0.00000000, 0.33333334],
                    [1.00000000, 0.33333334],
                    [0.00000000, 0.00000000],
                    [1.00000000, 0.00000000],
                    [0.00000000, 1.00000000],
                    [1.00000000, 1.00000000],
                    [0.00000000, 0.66666669],
                    [1.00000000, 0.66666669],
                    [0.00000000, 0.33333334],
                    [1.00000000, 0.33333334],
                    [0.00000000, 0.00000000],
                    [1.00000000, 0.00000000],
                    [0.00000000, 1.00000000],
                    [0.50000000, 1.00000000],
                    [1.00000000, 1.00000000],
                    [0.00000000, 0.00000000],
                    [0.50000000, 0.00000000],
                    [1.00000000, 0.00000000],
                    [0.00000000, 1.00000000],
                    [0.50000000, 1.00000000],
                    [1.00000000, 1.00000000],
                    [0.00000000, 0.00000000],
                    [0.50000000, 0.00000000],
                    [1.00000000, 0.00000000],
                    [0.00000000, 1.00000000],
                    [0.33333334, 1.00000000],
                    [0.66666669, 1.00000000],
                    [1.00000000, 1.00000000],
                    [0.00000000, 0.50000000],
                    [0.33333334, 0.50000000],
                    [0.66666669, 0.50000000],
                    [1.00000000, 0.50000000],
                    [0.00000000, 0.00000000],
                    [0.33333334, 0.00000000],
                    [0.66666669, 0.00000000],
                    [1.00000000, 0.00000000],
                    [0.00000000, 1.00000000],
                    [0.33333334, 1.00000000],
                    [0.66666669, 1.00000000],
                    [1.00000000, 1.00000000],
                    [0.00000000, 0.50000000],
                    [0.33333334, 0.50000000],
                    [0.66666669, 0.50000000],
                    [1.00000000, 0.50000000],
                    [0.00000000, 0.00000000],
                    [0.33333334, 0.00000000],
                    [0.66666669, 0.00000000],
                    [1.00000000, 0.00000000],
                ]
            ),
            decimal=7,
        )

        np.testing.assert_almost_equal(
            vertices["normal"],
            np.array(
                [
                    [-0.0, -0.0, -1.0],
                    [0, 0, -1],
                    [0, 0, -1],
                    [0, 0, -1],
                    [0, 0, -1],
                    [0, 0, -1],
                    [0, 0, -1],
                    [0, 0, -1],
                    [0, 0, 1],
                    [0, 0, 1],
                    [0, 0, 1],
                    [0, 0, 1],
                    [0, 0, 1],
                    [0, 0, 1],
                    [0, 0, 1],
                    [0, 0, 1],
                    [0, -1, 0],
                    [0, -1, 0],
                    [0, -1, 0],
                    [0, -1, 0],
                    [0, -1, 0],
                    [0, -1, 0],
                    [0, 1, 0],
                    [0, 1, 0],
                    [0, 1, 0],
                    [0, 1, 0],
                    [0, 1, 0],
                    [0, 1, 0],
                    [-1, 0, 0],
                    [-1, 0, 0],
                    [-1, 0, 0],
                    [-1, 0, 0],
                    [-1, 0, 0],
                    [-1, 0, 0],
                    [-1, 0, 0],
                    [-1, 0, 0],
                    [-1, 0, 0],
                    [-1, 0, 0],
                    [-1, 0, 0],
                    [-1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0],
                ]
            ),
            decimal=7,
        )

        np.testing.assert_almost_equal(
            vertices["colour"],
            np.array(
                [
                    [0.33333334, 1.00000000, 0.16666667, 1.00000000],
                    [0.66666669, 1.00000000, 0.16666667, 1.00000000],
                    [0.33333334, 0.66666669, 0.16666667, 1.00000000],
                    [0.66666669, 0.66666669, 0.16666667, 1.00000000],
                    [0.33333334, 0.33333334, 0.16666667, 1.00000000],
                    [0.66666669, 0.33333334, 0.16666667, 1.00000000],
                    [0.33333334, 0.00000000, 0.16666667, 1.00000000],
                    [0.66666669, 0.00000000, 0.16666667, 1.00000000],
                    [0.33333334, 1.00000000, 0.83333331, 1.00000000],
                    [0.66666669, 1.00000000, 0.83333331, 1.00000000],
                    [0.33333334, 0.66666669, 0.83333331, 1.00000000],
                    [0.66666669, 0.66666669, 0.83333331, 1.00000000],
                    [0.33333334, 0.33333334, 0.83333331, 1.00000000],
                    [0.66666669, 0.33333334, 0.83333331, 1.00000000],
                    [0.33333334, 0.00000000, 0.83333331, 1.00000000],
                    [0.66666669, 0.00000000, 0.83333331, 1.00000000],
                    [0.66666669, 0.00000000, 0.16666667, 1.00000000],
                    [0.66666669, 0.00000000, 0.50000000, 1.00000000],
                    [0.66666669, 0.00000000, 0.83333331, 1.00000000],
                    [0.33333334, 0.00000000, 0.16666667, 1.00000000],
                    [0.33333334, 0.00000000, 0.50000000, 1.00000000],
                    [0.33333334, 0.00000000, 0.83333331, 1.00000000],
                    [0.66666669, 1.00000000, 0.16666667, 1.00000000],
                    [0.66666669, 1.00000000, 0.50000000, 1.00000000],
                    [0.66666669, 1.00000000, 0.83333331, 1.00000000],
                    [0.33333334, 1.00000000, 0.16666667, 1.00000000],
                    [0.33333334, 1.00000000, 0.50000000, 1.00000000],
                    [0.33333334, 1.00000000, 0.83333331, 1.00000000],
                    [0.33333334, 0.00000000, 0.83333331, 1.00000000],
                    [0.33333334, 0.33333334, 0.83333331, 1.00000000],
                    [0.33333334, 0.66666669, 0.83333331, 1.00000000],
                    [0.33333334, 1.00000000, 0.83333331, 1.00000000],
                    [0.33333334, 0.00000000, 0.50000000, 1.00000000],
                    [0.33333334, 0.33333334, 0.50000000, 1.00000000],
                    [0.33333334, 0.66666669, 0.50000000, 1.00000000],
                    [0.33333334, 1.00000000, 0.50000000, 1.00000000],
                    [0.33333334, 0.00000000, 0.16666667, 1.00000000],
                    [0.33333334, 0.33333334, 0.16666667, 1.00000000],
                    [0.33333334, 0.66666669, 0.16666667, 1.00000000],
                    [0.33333334, 1.00000000, 0.16666667, 1.00000000],
                    [0.66666669, 0.00000000, 0.83333331, 1.00000000],
                    [0.66666669, 0.33333334, 0.83333331, 1.00000000],
                    [0.66666669, 0.66666669, 0.83333331, 1.00000000],
                    [0.66666669, 1.00000000, 0.83333331, 1.00000000],
                    [0.66666669, 0.00000000, 0.50000000, 1.00000000],
                    [0.66666669, 0.33333334, 0.50000000, 1.00000000],
                    [0.66666669, 0.66666669, 0.50000000, 1.00000000],
                    [0.66666669, 1.00000000, 0.50000000, 1.00000000],
                    [0.66666669, 0.00000000, 0.16666667, 1.00000000],
                    [0.66666669, 0.33333334, 0.16666667, 1.00000000],
                    [0.66666669, 0.66666669, 0.16666667, 1.00000000],
                    [0.66666669, 1.00000000, 0.16666667, 1.00000000],
                ]
            ),
            decimal=7,
        )

        np.testing.assert_equal(
            faces,
            np.array(
                [
                    [1, 2, 0],
                    [1, 3, 2],
                    [3, 4, 2],
                    [3, 5, 4],
                    [5, 6, 4],
                    [5, 7, 6],
                    [8, 10, 9],
                    [10, 11, 9],
                    [10, 12, 11],
                    [12, 13, 11],
                    [12, 14, 13],
                    [14, 15, 13],
                    [17, 19, 16],
                    [17, 20, 19],
                    [18, 20, 17],
                    [18, 21, 20],
                    [22, 25, 23],
                    [25, 26, 23],
                    [23, 26, 24],
                    [26, 27, 24],
                    [29, 32, 28],
                    [29, 33, 32],
                    [30, 33, 29],
                    [30, 34, 33],
                    [31, 34, 30],
                    [31, 35, 34],
                    [33, 36, 32],
                    [33, 37, 36],
                    [34, 37, 33],
                    [34, 38, 37],
                    [35, 38, 34],
                    [35, 39, 38],
                    [40, 44, 41],
                    [44, 45, 41],
                    [41, 45, 42],
                    [45, 46, 42],
                    [42, 46, 43],
                    [46, 47, 43],
                    [44, 48, 45],
                    [48, 49, 45],
                    [45, 49, 46],
                    [49, 50, 46],
                    [46, 50, 47],
                    [50, 51, 47],
                ]
            ),
        )

        np.testing.assert_equal(
            outline,
            np.array(
                [
                    [0, 2],
                    [2, 3],
                    [3, 1],
                    [1, 0],
                    [2, 4],
                    [4, 5],
                    [5, 3],
                    [3, 2],
                    [4, 6],
                    [6, 7],
                    [7, 5],
                    [5, 4],
                    [8, 10],
                    [10, 11],
                    [11, 9],
                    [9, 8],
                    [10, 12],
                    [12, 13],
                    [13, 11],
                    [11, 10],
                    [12, 14],
                    [14, 15],
                    [15, 13],
                    [13, 12],
                    [16, 19],
                    [19, 20],
                    [20, 17],
                    [17, 16],
                    [17, 20],
                    [20, 21],
                    [21, 18],
                    [18, 17],
                    [22, 25],
                    [25, 26],
                    [26, 23],
                    [23, 22],
                    [23, 26],
                    [26, 27],
                    [27, 24],
                    [24, 23],
                    [28, 32],
                    [32, 33],
                    [33, 29],
                    [29, 28],
                    [29, 33],
                    [33, 34],
                    [34, 30],
                    [30, 29],
                    [30, 34],
                    [34, 35],
                    [35, 31],
                    [31, 30],
                    [32, 36],
                    [36, 37],
                    [37, 33],
                    [33, 32],
                    [33, 37],
                    [37, 38],
                    [38, 34],
                    [34, 33],
                    [34, 38],
                    [38, 39],
                    [39, 35],
                    [35, 34],
                    [40, 44],
                    [44, 45],
                    [45, 41],
                    [41, 40],
                    [41, 45],
                    [45, 46],
                    [46, 42],
                    [42, 41],
                    [42, 46],
                    [46, 47],
                    [47, 43],
                    [43, 42],
                    [44, 48],
                    [48, 49],
                    [49, 45],
                    [45, 44],
                    [45, 49],
                    [49, 50],
                    [50, 46],
                    [46, 45],
                    [46, 50],
                    [50, 51],
                    [51, 47],
                    [47, 46],
                ]
            ),
        )

        for plane in MAPPING_PLANE_TO_AXIS.keys():
            np.testing.assert_almost_equal(
                primitive_cube(planes=[plane])[0]["position"],
                primitive_cube(planes=[MAPPING_PLANE_TO_AXIS[plane]])[0][
                    "position"
                ],
                decimal=7,
            )


if __name__ == "__main__":
    unittest.main()
