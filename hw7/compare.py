import time
from typing import List

from python_matrix import py_mul_mat
from c_matrix import c_mul_mat


def compare(matrices: List[List[List[int]]]) -> (float, float):
    c_time_start = time.time()
    c_res = matrices[0]
    for i in range(1, len(matrices)):
        c_res = c_mul_mat(c_res, matrices[i])
    print(c_res)
    c_time_end = time.time()

    py_time_start = time.time()
    py_res = matrices[0]
    for i in range(1, len(matrices)):
        py_res = py_mul_mat(py_res, matrices[i])
    print(py_res)
    py_time_end = time.time()

    return c_time_end - c_time_start, py_time_end - py_time_start


if __name__ == "__main__":
    print(compare([
        [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]],

        [[1],
         [2],
         [3]]]
    ))
