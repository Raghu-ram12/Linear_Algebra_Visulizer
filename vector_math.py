import math

class Vector:
    all_vectors = []

    def __init__(self, components, vector_id=None,track=True):
        self.components = components
        self.dim = len(components)
        self.vector_id = vector_id
        self.color = "white"
        if track:
            Vector.all_vectors.append(self)


def add_vectors(a: Vector, b: Vector) -> Vector:

    max_len = max(a.dim, b.dim)
    result = []
    for i in range(max_len):
        val_a = a.components[i] if a.dim else 0
        val_b = b.components[i] if b.dim else 0
        result.append(val_a + val_b)

    return Vector(result)


def sub_vectors(a: Vector, b: Vector) -> Vector:

    max_len = max(a.dim, b.dim)
    result = []
    for i in range(max_len):
        val_a = a.components[i] if a.dim else 0
        val_b = b.components[i] if b.dim else 0
        result.append(val_a - val_b)

    return Vector(result)


def multiply_scaler(a: Vector, k: float) -> Vector:

    return Vector([a.components[i] * k for i in range(a.dim)])


def magnitude(a: Vector) -> float:

    return sum([a.components[i] ** 2 for i in range(a.dim)]) ** 0.5


def dot_product(a: Vector, b: Vector) -> float:

    min_len = min(a.dim, b.dim)
    result = []
    for i in range(min_len):
        result.append(a.components[i] * b.components[i])

    return sum(result)


def Vector_angle(a: Vector, b: Vector):

    d = dot_product(a, b)
    mag_a = magnitude(a)
    mag_b = magnitude(b)
    return math.acos(d / (mag_a * mag_b))


def normalize(a: Vector) -> Vector:

    mag = magnitude(a)

    return Vector([a.components[i] / mag for i in range(a.dim)])
