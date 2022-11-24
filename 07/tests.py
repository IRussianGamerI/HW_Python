import unittest

import cffi

from c_matrix import c_matmul
from compare import compare
from python_matrix import py_matmul

MATRIX_LEFT = [
    [-149.460000, -807.030000, -620.660000, 0.000000, -385.310000, 0.000000, 0.000000],
    [
        0.000000,
        -810.540000,
        -858.660000,
        -912.290000,
        -642.500000,
        -700.560000,
        -948.280000,
    ],
    [0.000000, -297.600000, -973.410000, 0.000000, 0.000000, -38.070000, -125.790000],
    [
        0.000000,
        -563.020000,
        -43.970000,
        -819.050000,
        -137.380000,
        -533.340000,
        -480.570000,
    ],
    [0.000000, 0.000000, -766.040000, 0.000000, -665.580000, 0.000000, 0.000000],
]

MATRIX_RIGHT = [
    [-886.520000, -120.680000, 0.000000, 0.000000, 0.000000],
    [-730.250000, -754.480000, 0.000000, -946.920000, -238.630000],
    [-215.770000, -886.890000, -771.440000, -500.190000, -513.630000],
    [0.000000, -521.160000, -768.980000, -240.200000, -450.600000],
    [-803.200000, 0.000000, 0.000000, 0.000000, -45.640000],
    [0.000000, 0.000000, 0.000000, 0.000000, 0.000000],
    [0.000000, -693.720000, -809.540000, -515.250000, -639.940000],
]

MATRIX_RESULT = [
    [1165233.736900, 1177381.974600, 478801.950400, 1074640.773000, 528956.713100],
    [1293225.903200, 2506363.044600, 2131608.025800, 1904743.010200, 1681696.573200],
    [427355.075700, 1175103.881700, 852759.447000, 833506.637400, 651486.918900],
    [530976.377900, 1224021.001300, 1052793.923600, 999477.755200, 839807.692700],
    [699882.306800, 679393.215600, 590953.897600, 383165.547600, 423838.196400],
]


class TestCLib(unittest.TestCase):
    ffi = cffi.FFI()
    lib = ffi.dlopen("build/libmatrix.so")
    ffi.cdef(
        """
    typedef struct Matrix {
        double **array;
        size_t rows, cols;
    } Matrix;

    Matrix *create_matrix(size_t rows, size_t cols);
    int free_matrix(Matrix *matrix);

    Matrix *mul(const Matrix *l, const Matrix *r);"""
    )

    def test_creation(self):
        matrix = self.lib.create_matrix(5, 5)
        self.assertEqual(matrix.rows, 5)
        self.assertEqual(matrix.cols, 5)
        for i in range(matrix.rows):
            for j in range(matrix.cols):
                self.assertEqual(matrix.array[i][j], 0)

        self.lib.free_matrix(matrix)

    def test_multiplication(self):
        self.assertEqual(len(MATRIX_LEFT[0]), len(MATRIX_RIGHT))

        m_left = self.lib.create_matrix(len(MATRIX_LEFT), len(MATRIX_LEFT[0]))
        m_right = self.lib.create_matrix(len(MATRIX_RIGHT), len(MATRIX_RIGHT[0]))

        for i in range(m_left.rows):
            for j in range(m_left.cols):
                m_left.array[i][j] = MATRIX_LEFT[i][j]

        for i in range(m_right.rows):
            for j in range(m_right.cols):
                m_right.array[i][j] = MATRIX_RIGHT[i][j]

        m_res = self.lib.mul(m_left, m_right)

        self.assertEqual(m_res.rows, m_left.rows)
        self.assertEqual(m_res.cols, m_right.cols)

        for i in range(m_res.rows):
            for j in range(m_res.cols):
                self.assertAlmostEqual(
                    m_res.array[i][j], MATRIX_RESULT[i][j], delta=1e-6
                )

        self.lib.free_matrix(m_left)
        self.lib.free_matrix(m_right)
        self.lib.free_matrix(m_res)


class TestCMatmul(unittest.TestCase):
    def test_c_matmul_exceptions(self):
        with self.assertRaises(ValueError):
            _ = c_matmul([[1], [1, 2]], [[1, 2], [1]])

        with self.assertRaises(ValueError):
            _ = c_matmul([[1, 2]], [[1, 2, 3]])

    def test_c_matmul_calcs(self):
        res = c_matmul(MATRIX_LEFT, MATRIX_RIGHT)

        self.assertEqual(len(MATRIX_RESULT), len(res))

        for i, row in enumerate(MATRIX_RESULT):
            self.assertEqual(len(row), len(res[i]))
            for j, value in enumerate(row):
                self.assertAlmostEqual(value, res[i][j], delta=1e-6)


class TestPyMatmul(unittest.TestCase):
    def test_py_matmul_exceptions(self):
        with self.assertRaises(ValueError):
            _ = py_matmul([[1], [1, 2]], [[1, 2], [1]])

        with self.assertRaises(ValueError):
            _ = py_matmul([[1, 2]], [[1, 2, 3]])

    def test_c_matmul_calcs(self):
        res = py_matmul(MATRIX_LEFT, MATRIX_RIGHT)

        self.assertEqual(len(MATRIX_RESULT), len(res))

        for i, row in enumerate(MATRIX_RESULT):
            self.assertEqual(len(row), len(res[i]))
            for j, value in enumerate(row):
                self.assertAlmostEqual(value, res[i][j], delta=1e-6)


class TestMyCompare(unittest.TestCase):
    def test_logic(self):
        c_time, py_time, c_res, py_res = compare([MATRIX_LEFT, MATRIX_RIGHT])

        self.assertEqual(len(c_res), len(py_res))

        for i, row in enumerate(c_res):
            self.assertEqual(len(row), len(py_res[i]))
            for j, value in enumerate(row):
                self.assertAlmostEqual(value, py_res[i][j], delta=1e-6)

        self.assertTrue(py_time < c_time)


if __name__ == "__main__":
    unittest.main()
