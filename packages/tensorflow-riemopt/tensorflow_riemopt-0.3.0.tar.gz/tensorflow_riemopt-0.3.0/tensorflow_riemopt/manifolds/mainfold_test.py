import tensorflow as tf
from tensorflow_riemopt.manifolds.manifold import Manifold


class DummyManifold2(Manifold):
    """Minimal manifold to exercise default pairmean and random."""

    name = "Dummy2"
    ndims = 0

    def _check_point_on_manifold(self, x, atol, rtol):
        return tf.constant(True)

    def _check_vector_on_tangent(self, x, u, atol, rtol):
        return tf.constant(True)

    def log(self, x, y):
        return y - x

    def exp(self, x, u):
        return x + u

    def proju(self, x, u):
        return u

    def projx(self, x):
        return x

    def dist(self, x, y, keepdims=False):
        return tf.zeros_like(x)

    def inner(self, x, u, v, keepdims=False):
        return tf.zeros_like(u[..., :1])

    def retr(self, x, u):
        return self.exp(x, u)

    def geodesic(self, x, u, t):
        return x + t * u

    def transp(self, x, y, v):
        return v


def test_pairmean_default():
    m = DummyManifold2()
    x = tf.constant([1.0, 3.0], dtype=tf.float32)
    y = tf.constant([5.0, 7.0], dtype=tf.float32)
    pm = m.pairmean(x, y)
    tf.debugging.assert_near(pm, (x + y) / 2.0)


def test_random_default():
    m = DummyManifold2()
    shape = (4, 2)
    x = m.random(shape, dtype=tf.float64)
    assert isinstance(x, tf.Tensor)
    assert x.shape.as_list() == list(shape)
    assert x.dtype == tf.float64
