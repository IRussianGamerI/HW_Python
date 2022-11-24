import time
from typing import List, Any

from python_matrix import py_matmul
from c_matrix import c_matmul


def compare(matrices: List[List[List[float]]]) -> (float, float):
    c_time_start = time.time()
    c_result = matrices[0]
    for i in range(1, len(matrices)):
        c_result = c_matmul(c_result, matrices[i])
    c_time_end = time.time()

    py_time_start = time.time()
    py_result = matrices[0]
    for i in range(1, len(matrices)):
        py_result = py_matmul(py_result, matrices[i])
    py_time_end = time.time()

    return c_time_end - c_time_start, py_time_end - py_time_start, c_result, py_result


def repr_as_matrix(matrix: List[List[Any]]):
    return "[{}]".format("\n".join(str(row) for row in matrix))


if __name__ == "__main__":
    matrix_left = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    matrix_right = [[1], [2], [3]]  # На самом деле, вектор-столбец

    print("Сравнение времени выполнения операции умножения матриц.")
    print(f"Левый операнд:\n{repr_as_matrix(matrix_left)}")
    print(f"Правый операнд:\n{repr_as_matrix(matrix_right)}")

    c_time, py_time, c_res, py_res = compare([matrix_left, matrix_right])

    print(f"Результат умножения на C:\n{repr_as_matrix(c_res)}")
    print(f"Результат умножения на Python:\n{repr_as_matrix(py_res)}")

    print(f"Время выполнения на C: {'%.4f' % c_time} с")
    print(f"Время выполнения на Python: {'%.4e' % py_time} с")
