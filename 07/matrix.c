#include <malloc.h>
#include <math.h>
#include <stdint.h>

#include "matrix.h"

// Creations and basic operations implementations
Matrix *create_matrix_from_file(const char *path_file) {
    FILE *input = fopen(path_file, "r");
    if (!input) {
        return NULL;
    }
    size_t rows, cols;
    if (fscanf(input, "%zu%zu", &rows, &cols) != SIZES_NEEDED) {
        fclose(input);
        return NULL;
    }
    Matrix *matrix = create_matrix(rows, cols);
    if (!matrix) {
        fclose(input);
        return NULL;
    }
    for (size_t i = 0; i < matrix->rows; ++i) {
        for (size_t j = 0; j < matrix->cols; ++j) {
            if (fscanf(input, "%lf", &matrix->array[i][j]) != 1) {
                fclose(input);
                free_matrix(matrix);
                return NULL;
            }
        }
    }
    fclose(input);
    return matrix;
}

Matrix *create_matrix(size_t rows, size_t cols) {
    if (!(rows && cols)) {
        return NULL;
    }
    Matrix *matrix = calloc(1, sizeof(Matrix));
    if (!matrix) {
        return NULL;
    }
    matrix->array = malloc(rows * sizeof(double *));
    if (!matrix->array) {
        free(matrix);
        return NULL;
    }
    for (size_t i = 0; i < rows; ++i) {
        matrix->array[i] = calloc(cols, sizeof(double));
        if (!matrix->array[i]) {
            free_matrix(matrix);
            return NULL;
        }
    }
    matrix->rows = rows;
    matrix->cols = cols;
    return matrix;
}

int free_matrix(Matrix *matrix) {
    if (!matrix) {
        return NO_MATRIX;
    }
    for (size_t i = 0; i < matrix->rows; ++i) {
        free(matrix->array[i]);
    }
    free(matrix->array);
    free(matrix);
    return SUCCESS;
}

int get_rows(const Matrix *matrix, size_t *rows) {
    if (!matrix) {
        return NO_MATRIX;
    }
    if (!rows) {
        return BAD_PTR;
    }
    *rows = matrix->rows;
    return SUCCESS;
}

int get_cols(const Matrix *matrix, size_t *cols) {
    if (!matrix) {
        return NO_MATRIX;
    }
    if (!cols) {
        return BAD_PTR;
    }
    *cols = matrix->cols;
    return SUCCESS;
}

int get_elem(const Matrix *matrix, size_t row, size_t col, double *val) {
    if (!matrix) {
        return NO_MATRIX;
    }
    if (row >= matrix->rows || col >= matrix->cols) {
        return NO_ELEMENT;
    }
    if (!val) {
        return BAD_PTR;
    }
    *val = matrix->array[row][col];
    return SUCCESS;
}

int set_elem(Matrix *matrix, size_t row, size_t col, double val) {
    if (!matrix) {
        return NO_MATRIX;
    }
    if (row >= matrix->rows || col >= matrix->cols) {
        return NO_ELEMENT;
    }
    matrix->array[row][col] = val;
    return SUCCESS;
}

// Math operations implementations
Matrix *mul_scalar(const Matrix *matrix, double val) {
    if (!matrix) {
        return NULL;
    }
    Matrix *res = create_matrix(matrix->rows, matrix->cols);
    if (!res) {
        return NULL;
    }
    for (size_t i = 0; i < res->rows; ++i) {
        for (size_t j = 0; j < res->cols; ++j) {
            res->array[i][j] = val * matrix->array[i][j];
        }
    }
    return res;
}

Matrix *transp(const Matrix *matrix) {
    if (!matrix) {
        return NULL;
    }
    Matrix *res = create_matrix(matrix->cols, matrix->rows);
    if (!res) {
        return NULL;
    }
    for (size_t i = 0; i < res->rows; ++i) {
        for (size_t j = 0; j < res->cols; ++j) {
            res->array[i][j] = matrix->array[j][i];
        }
    }
    return res;
}

Matrix *sum(const Matrix *l, const Matrix *r) {
    if (!(l && r)) {
        return NULL;
    }
    Matrix *res = create_matrix(l->rows, l->cols);
    if (!res) {
        return NULL;
    }
    for (size_t i = 0; i < res->rows; ++i) {
        for (size_t j = 0; j < res->cols; ++j) {
            res->array[i][j] = l->array[i][j] + r->array[i][j];
        }
    }
    return res;
}

Matrix *sub(const Matrix *l, const Matrix *r) {
    if (!(l && r)) {
        return NULL;
    }
    Matrix *res = create_matrix(l->rows, l->cols);
    if (!res) {
        return NULL;
    }
    for (size_t i = 0; i < res->rows; ++i) {
        for (size_t j = 0; j < res->cols; ++j) {
            res->array[i][j] = l->array[i][j] - r->array[i][j];
        }
    }
    return res;
}

Matrix *mul(const Matrix *l, const Matrix *r) {
    if (!(l && r)) {
        return NULL;
    }
    if (l->cols != r->rows) {
        return NULL;
    }
    Matrix *res = create_matrix(l->rows, r->cols);
    if (!res) {
        return NULL;
    }
    for (size_t i = 0; i < res->rows; ++i) {
        for (size_t j = 0; j < res->cols; ++j) {
            for (size_t k = 0; k < l->cols; ++k) {
                res->array[i][j] += l->array[i][k] * r->array[k][j];
            }
        }
    }
    return res;
}

// Extra operations
void swap(double **pDouble, double **pDouble1) {
    *pDouble = (double *) ((uintptr_t) *pDouble ^ (uintptr_t) *pDouble1);
    *pDouble1 = (double *) ((uintptr_t) *pDouble ^ (uintptr_t) *pDouble1);
    *pDouble = (double *) ((uintptr_t) *pDouble ^ (uintptr_t) *pDouble1);
}

int det(const Matrix *matrix, double *val) {
    if (!matrix) {
        return NO_MATRIX;
    }
    if (!val) {
        return BAD_PTR;
    }
    if (!matrix->rows || matrix->rows != matrix->cols) {
        return DOES_NOT_EXIST;
    }
    Matrix *cpy = create_matrix(matrix->rows, matrix->cols);
    if (!cpy) {
        return NO_MATRIX;
    }
    for (size_t i = 0; i < cpy->rows; ++i) {
        for (size_t j = 0; j < cpy->cols; ++j) {
            cpy->array[i][j] = matrix->array[i][j];
        }
    }

    *val = 1;
    double temp;
    for (size_t k = 0; k < matrix->rows; ++k) {
        if (fabs(cpy->array[k][k]) < EPS) {
            for (size_t i = k + 1; i < cpy->rows; ++i) {
                if (fabs(cpy->array[i][k]) >= EPS) {
                    swap(&cpy->array[i], &cpy->array[k]);
                    *val *= -1;
                    break;
                }
            }
        }

        if (fabs(cpy->array[k][k]) < EPS) {
            *val = 0;
            free_matrix(cpy);
            return SUCCESS;
        }

        for (size_t i = k + 1; i < cpy->rows; ++i) {
            temp = cpy->array[i][k] / cpy->array[k][k];
            cpy->array[i][k] = 0;
            for (size_t j = k + 1; j < cpy->cols; ++j) {
                cpy->array[i][j] -= temp * cpy->array[k][j];
            }
        }
    }

    for (size_t k = 0; k < cpy->rows; ++k) {
        *val *= cpy->array[k][k];
    }
    free_matrix(cpy);
    return SUCCESS;
}

Matrix *adj(const Matrix *matrix) {
    if (!matrix) {
        return NULL;
    }
    double d;
    if (det(matrix, &d) != SUCCESS) {
        return NULL;
    }
    Matrix *src = inv(matrix);
    if (!src) {
        return NULL;
    }
    Matrix *res = mul_scalar(src, d);
    free_matrix(src);
    return res;
}

Matrix *inv(const Matrix *matrix) {
    if (!matrix) {
        return NULL;
    }
    if (!matrix->rows || matrix->rows != matrix->cols) {
        return NULL;
    }

    Matrix *cpy = create_matrix(matrix->rows, matrix->cols);
    if (!cpy) {
        return NULL;
    }
    Matrix *res = create_matrix(matrix->rows, matrix->cols);
    if (!res) {
        free_matrix(cpy);
        return NULL;
    }
    cpy->rows = matrix->rows;
    cpy->cols = matrix->cols;
    res->rows = matrix->rows;
    res->cols = matrix->cols;

    for (size_t i = 0; i < res->rows; ++i) {
        for (size_t j = 0; j < cpy->cols; ++j) {
            cpy->array[i][j] = matrix->array[i][j];
        }
        res->array[i][i] = 1;
    }

    double temp;
    for (size_t k = 0; k < res->rows; ++k) {
        if (fabs(cpy->array[k][k]) < EPS) {
            for (size_t i = k + 1; i < cpy->rows; ++i) {
                if (fabs(cpy->array[i][k]) >= EPS) {
                    swap(&res->array[i], &res->array[k]);
                    swap(&cpy->array[i], &cpy->array[k]);
                    break;
                }
            }
        }

        if (fabs(cpy->array[k][k]) < EPS) {
            free_matrix(cpy);
            free_matrix(res);
            return NULL;
        }

        temp = cpy->array[k][k];
        for (size_t j = 0; j < res->cols; ++j) {
            cpy->array[k][j] /= temp;
            res->array[k][j] /= temp;
        }

        for (size_t i = k + 1; i < res->rows; ++i) {
            temp = cpy->array[i][k];
            for (size_t j = 0; j < res->cols; ++j) {
                res->array[i][j] -= res->array[k][j] * temp;
                cpy->array[i][j] -= cpy->array[k][j] * temp;
            }
        }
    }

    double d = cpy->array[0][0];
    for (size_t i = 1; i < cpy->rows; ++i) {
        d *= cpy->array[i][i];
    }
    if (fabs(d) < EPS) {
        free_matrix(res);
        free_matrix(cpy);
        return NULL;
    }

    for (size_t k = res->rows - 1; k != 0; --k) {
        for (size_t i = 0; i < k; ++i) {
            temp = cpy->array[i][k];
            for (size_t j = 0; j < res->cols; ++j) {
                cpy->array[i][j] -= cpy->array[k][j] * temp;
                res->array[i][j] -= res->array[k][j] * temp;
            }
        }
    }
    free_matrix(cpy);
    return res;
}
