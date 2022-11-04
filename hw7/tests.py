import unittest

import cffi


class TestCFuncs(unittest.TestCase):
    ffi = cffi.FFI()
    lib = ffi.dlopen("build/libmatrix.so")
    ffi.cdef("""
    typedef struct Matrix {
        double **array;
        size_t rows, cols;
    } Matrix;

    Matrix *create_matrix(size_t rows, size_t cols);
    int free_matrix(Matrix *matrix);

    Matrix *mul(const Matrix *l, const Matrix *r);""")

    def test_creation(self):
        matrix = self.lib.create_matrix(5, 5)
        self.assertEqual(matrix.rows, 5)
        self.assertEqual(matrix.cols, 5)
        for i in range(matrix.rows):
            for j in range(matrix.cols):
                self.assertEqual(matrix.array[i][j], 0)

        self.lib.free_matrix(matrix)
        

if __name__ == "__main__":
    unittest.main()
