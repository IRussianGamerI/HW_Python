from typing import List


def py_mul_mat(matrix1: List[List[float]], matrix2: List[List[float]]) -> List[List[float]]:
    shape1 = [len(i) for i in matrix1]
    shape2 = [len(i) for i in matrix2]
    if min(shape1) != max(shape1) or min(shape2) != max(shape2):
        raise ValueError("Given object(s) must be matrices")
    if shape1[0] != len(shape2):
        raise ValueError("Matrices are incompatible")
    res = []
    for i in range(len(shape1)):
        res.append([])
        for j in range(shape2[0]):
            res[i].append(0)
            for k in range(shape1[0]):
                res[i][j] += matrix1[i][k] * matrix2[k][j]
    return res
