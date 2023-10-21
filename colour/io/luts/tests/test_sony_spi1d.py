# !/usr/bin/env python
"""Define the unit tests for the :mod:`colour.io.luts.sony_spi1d` module."""

from __future__ import annotations

import os
import shutil
import tempfile
import unittest

import numpy as np

from colour.io import read_LUT_SonySPI1D, write_LUT_SonySPI1D

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "ROOT_LUTS",
    "TestReadLUTSonySPI1D",
    "TestWriteLUTSonySPI1D",
]

ROOT_LUTS: str = os.path.join(
    os.path.dirname(__file__), "resources", "sony_spi1d"
)


class TestReadLUTSonySPI1D(unittest.TestCase):
    """
    Define :func:`colour.io.luts.sony_spi1d.read_LUT_SonySPI1D` definition
    unit tests methods.
    """

    def test_read_LUT_SonySPI1D(self):
        """Test :func:`colour.io.luts.sony_spi1d.read_LUT_SonySPI1D` definition."""

        LUT_1 = read_LUT_SonySPI1D(
            os.path.join(ROOT_LUTS, "eotf_sRGB_1D.spi1d")
        )

        np.testing.assert_array_almost_equal(
            LUT_1.table,
            np.array(
                [
                    -7.73990000e-03,
                    5.16000000e-04,
                    1.22181000e-02,
                    3.96819000e-02,
                    8.71438000e-02,
                    1.57439400e-01,
                    2.52950100e-01,
                    3.75757900e-01,
                    5.27729400e-01,
                    7.10566500e-01,
                    9.25840600e-01,
                    1.17501630e00,
                    1.45946870e00,
                    1.78049680e00,
                    2.13933380e00,
                    2.53715520e00,
                ]
            ),
        )
        self.assertEqual(LUT_1.name, "eotf sRGB 1D")
        self.assertEqual(LUT_1.dimensions, 1)
        np.testing.assert_array_equal(LUT_1.domain, np.array([-0.1, 1.5]))
        self.assertEqual(LUT_1.size, 16)
        self.assertListEqual(
            LUT_1.comments,
            ['Generated by "Colour 0.3.11".', '"colour.models.eotf_sRGB".'],
        )

        LUT_2 = read_LUT_SonySPI1D(
            os.path.join(ROOT_LUTS, "eotf_sRGB_3x1D.spi1d")
        )
        self.assertListEqual(
            LUT_2.comments,
            ['Generated by "Colour 0.3.11".', '"colour.models.eotf_sRGB".'],
        )
        np.testing.assert_array_equal(
            LUT_2.domain, np.array([[-0.1, -0.1, -0.1], [1.5, 1.5, 1.5]])
        )


class TestWriteLUTSonySPI1D(unittest.TestCase):
    """
    Define :func:`colour.io.luts.sony_spi1d.write_LUT_SonySPI1D` definition
    unit tests methods.
    """

    def setUp(self):
        """Initialise the common tests attributes."""

        self._temporary_directory = tempfile.mkdtemp()

    def tearDown(self):
        """After tests actions."""

        shutil.rmtree(self._temporary_directory)

    def test_write_LUT_SonySPI1D(self):
        """Test :func:`colour.io.luts.sony_spi1d.write_LUT_SonySPI1D` definition."""

        LUT_1_r = read_LUT_SonySPI1D(
            os.path.join(ROOT_LUTS, "eotf_sRGB_1D.spi1d")
        )
        write_LUT_SonySPI1D(
            LUT_1_r,
            os.path.join(self._temporary_directory, "eotf_sRGB_1D.spi1d"),
        )
        LUT_1_t = read_LUT_SonySPI1D(
            os.path.join(self._temporary_directory, "eotf_sRGB_1D.spi1d")
        )
        self.assertEqual(LUT_1_r, LUT_1_t)

        LUT_2_r = read_LUT_SonySPI1D(
            os.path.join(ROOT_LUTS, "eotf_sRGB_3x1D.spi1d")
        )
        write_LUT_SonySPI1D(
            LUT_2_r,
            os.path.join(self._temporary_directory, "eotf_sRGB_3x1D.spi1d"),
        )
        LUT_2_t = read_LUT_SonySPI1D(
            os.path.join(self._temporary_directory, "eotf_sRGB_3x1D.spi1d")
        )
        self.assertEqual(LUT_2_r, LUT_2_t)
        self.assertListEqual(LUT_2_r.comments, LUT_2_t.comments)


if __name__ == "__main__":
    unittest.main()
