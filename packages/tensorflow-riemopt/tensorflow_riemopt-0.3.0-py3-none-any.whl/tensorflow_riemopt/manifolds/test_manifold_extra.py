import tensorflow as tf
import pytest

from tensorflow_riemopt.manifolds.manifold import Manifold
from tensorflow_riemopt.manifolds.euclidean import Euclidean


class DummyManifold(Manifold):
    name = "Dummy"
    ndims = 1

    def _check_point_on_manifold(self, x, atol, rtol):
        return tf.constant(True)

    def _check_vector_on_tangent(self, x, u, atol, rtol):
        return tf.constant(True)

    def dist(self, x, y, keepdims=False):
        raise NotImplementedError

    def inner(self, x, u, v, keepdims=False):
        raise NotImplementedError

    def proju(self, x, u):
        raise NotImplementedError

    def projx(self, x):
        raise NotImplementedError

    def retr(self, x, u):
        raise NotImplementedError

    def exp(self, x, u):
        raise NotImplementedError

    def log(self, x, y):
        raise NotImplementedError

    def transp(self, x, y, v):
        return v

    def geodesic(self, x, u, t):
        raise NotImplementedError


def test_repr_and_defaults():
    m = DummyManifold()
    # repr should include name and ndims
    s = repr(m)
    assert "Dummy (ndims=1) manifold" in s

    # default check_shape uses _check_shape(True) and length >= ndims
    assert m.check_shape((5,))
    assert m.check_shape(tf.constant([1, 2, 3]))

    # test norm method via Euclidean
    e = Euclidean(ndims=2)
    x = tf.constant([[1.0, 2.0], [3.0, 4.0]])
    u = tf.constant([[0.5, -0.5], [1.0, -1.0]])
    # inner and norm
    inner = e.inner(x, u, u)
    norm = e.norm(x, u)
    assert tf.reduce_all(inner >= 0)
    assert tf.abs(norm - tf.sqrt(inner)) < 1e-6

    # pairmean
    a = tf.constant([1.0, 3.0])
    b = tf.constant([5.0, 7.0])
    mean = e.pairmean(a, b)
    assert tf.reduce_all(mean == tf.constant([3.0, 5.0]))