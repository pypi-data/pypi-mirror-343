import pytest
import tensorflow as tf

from tensorflow_riemopt.manifolds.approximate_mixin import ApproximateMixin


class FakeManifold(ApproximateMixin):
    def __init__(self):
        # dummy attributes
        self.name = "Fake"
        self.ndims = 1

    def log(self, x, y):
        return y - x

    def exp(self, x, u):
        return x + u

    def transp(self, x, y, v):
        # delegate to mixin
        return self.ladder_ptransp(x, y, v, method=self._method, n_steps=self._steps)

    # implement required abstract methods
    def _check_point_on_manifold(self, x, atol, rtol):
        return True

    def _check_vector_on_tangent(self, x, u, atol, rtol):
        return True

    dist = exp
    inner = log
    proju = exp
    projx = lambda self, x: x
    retr = exp
    ptransp = transp
    geodesic = exp
    pairmean = log


def test_invalid_method():
    fm = FakeManifold()
    x = tf.constant([0.0])
    y = tf.constant([1.0])
    v = tf.constant([0.5])
    fm._method = 'invalid'
    fm._steps = 1
    with pytest.raises(ValueError):
        fm.ladder_ptransp(x, y, v, method='bad', n_steps=1)

def test_invalid_n_steps():
    fm = FakeManifold()
    x = tf.constant([0.0])
    y = tf.constant([1.0])
    v = tf.constant([0.5])
    with pytest.raises(ValueError):
        fm.ladder_ptransp(x, y, v, method='pole', n_steps=0)