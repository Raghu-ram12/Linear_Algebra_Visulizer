from transformations import rotate_vector, scale_vector
from vector_math import Vector


def test_scale_vector_preserves_vector_metadata():
    v = Vector([1.0, 2.0], vector_id="v1")
    v.color = "red"

    scaled = scale_vector(v, 2.0, 3.0)

    assert scaled.components == [2.0, 6.0]
    assert scaled.dim == 2
    assert scaled.vector_id == "v1"
    assert scaled.color == "red"


def test_rotate_vector_after_scaling_keeps_scaled_components():
    v = Vector([2.0, 0.0], vector_id="v1")
    scaled = scale_vector(v, 2.0, 1.0)
    rotated = rotate_vector(scaled, 90)

    assert rotated.components == [0.0, 4.0]
    assert rotated.dim == 2
