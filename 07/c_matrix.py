from typing import List

import cffi


def c_matmul(
    matrix1: List[List[float]], matrix2: List[List[float]]
) -> List[List[float]]:
    shape1 = [len(i) for i in matrix1]
    shape2 = [len(i) for i in matrix2]
    if min(shape1) != max(shape1) or min(shape2) != max(shape2):
        raise ValueError("Given object(s) must be matrices")
    rows1 = len(shape1)
    cols1 = shape1[0]
    rows2 = len(shape2)
    cols2 = shape2[0]

    if cols1 != rows2:
        raise ValueError("Matrices are incompatible")

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

    cm1 = lib.create_matrix(rows1, cols1)
    cm2 = lib.create_matrix(rows2, cols2)

    for i in range(rows1):
        for j in range(cols1):
            cm1.array[i][j] = matrix1[i][j]

    for i in range(rows2):
        for j in range(cols2):
            cm2.array[i][j] = matrix2[i][j]

    c_res = lib.mul(cm1, cm2)
    assert lib.free_matrix(cm1) + lib.free_matrix(cm2) == 0

    py_res = [[c_res.array[i][j] for j in range(cols2)] for i in range(rows1)]
    assert lib.free_matrix(c_res) == 0

    return py_res
