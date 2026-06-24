from vector_math import Vector


class ShapeMismatch(Exception):
    pass


class Matrix:

    def __init__(self, data):

        self.data = [list(row) for row in data]
        self.rows = len(self.data)
        self.cols = len(self.data[0])
        self.shape = (self.rows, self.cols)


def add_matrices(a: Matrix, b: Matrix) -> Matrix:

    if a.shape == b.shape:
        result = []

        for i in range(a.rows):
            row = []

            for j in range(a.cols):
                row.append(a.data[i][j] + b.data[i][j])

            result.append(row)

        return Matrix(result)
    else:

        raise ShapeMismatch(
            f"matrix a is of shape {a.shape} Matrix b is of shape {b.shape}"
        )


def sub_matrices(a: Matrix, b: Matrix) -> Matrix:

    if a.shape == b.shape:
        result = []

        for i in range(a.rows):
            row = []

            for j in range(a.cols):
                row.append(a.data[i][j] - b.data[i][j])

            result.append(row)

        return Matrix(result)

    else:

        raise ShapeMismatch(
            f"matrix a is of shape {a.shape} Matrix b is of shape {b.shape}"
        )


def multiply_matrix_by_scaler(a: Matrix, k: float) -> Matrix:
    result = []
    for i in range(a.rows):
        row = []
        for j in range(a.cols):

            row.append(a.data[i][j] * k)

        result.append(row)

    return Matrix(result)


def matrix_mul(a: Matrix, b: Matrix) -> Matrix:

    if a.cols == b.rows:

        result = []

        for i in range(a.rows):

            row = []

            for j in range(b.cols):

                row.append(sum([a.data[i][k] * b.data[k][j] for k in range(a.cols)]))

            result.append(row)

        return Matrix(result)

    else:
        raise ShapeMismatch(
            f"matrix multiplication not possible {a.shape} and {b.shape}"
        )


def zero_matrix(n: int) -> Matrix:

    return Matrix([[0 for _ in range(n)] for _ in range(n)])


def identity_matrix(n: int) -> Matrix:

    result = []
    for i in range(n):
        row = []
        for j in range(n):

            if i == j:
                row.append(1)
            else:
                row.append(0)

        result.append(row)

    return Matrix(result)


def multiply_matrix_vector(v: Vector, m: Matrix) -> Vector:
    if v is None or m is None or not isinstance(v,Vector):
        print("invalid input")
        return None

    if v.dim != m.cols:
        raise ShapeMismatch(
            f"rows in vector {v.dim} not equal to columns in matrix {m.cols}"
        )

    result = []

    for i in range(m.rows):

        result.append(
            sum(round(m.data[i][j] * v.components[j], 4) for j in range(m.cols))
        )

    transformed = Vector(result, track=False)
    transformed.vector_id = v.vector_id
    transformed.color = v.color
    return transformed


def determinant_2x2(m: Matrix) -> float:

    return m.data[0][0] * m.data[1][1] - (m.data[1][0] * m.data[0][1])


def determinant_3X3(m: Matrix) -> float:

    if m.shape != (3, 3):
        raise ShapeMismatch("Please Give a 3x3 matrix")
        return

    matrix = m.data

    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]

    term1 = a * (e * i - f * h)
    term2 = b * (d * i - f * g)
    term3 = c * (d * h - e * g)

    return term1 - term2 + term3
