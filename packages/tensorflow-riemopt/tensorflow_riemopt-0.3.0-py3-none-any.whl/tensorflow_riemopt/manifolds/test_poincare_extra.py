import tensorflow as tf
import pytest

from tensorflow_riemopt.manifolds.poincare import Poincare


def test_poincare_geodesic_pairmean():
    p = Poincare()
    # pick two points inside unit ball
    x = tf.constant([[0.1, 0.0]], dtype=tf.float32)
    y = tf.constant([[0.0, 0.2]], dtype=tf.float32)
    # geodesic at t=0 returns x
    ge0 = p.geodesic(x, p.log(x, y), t=0.0)
    tf.debugging.assert_near(ge0, x)
    # pairmean should equal geodesic at t=0.5
    mid = p.pairmean(x, y)
    ge_half = p.geodesic(x, p.log(x, y), t=0.5)
    tf.debugging.assert_near(mid, ge_half, atol=1e-5)

def test_poincare_exp_log_inverse():
    p = Poincare()
    x = tf.constant([[0.1, 0.1]], dtype=tf.float64)
    u = tf.constant([[0.2, -0.1]], dtype=tf.float64)
    y = p.exp(x, u)
    u2 = p.log(x, y)
    tf.debugging.assert_near(u, u2, atol=1e-6)

def test_poincare_invalid_shape():
    p = Poincare()
    # invalid shape: last dim should >=1
    # check_shape should return False for invalid last-dimension shape
    assert not p.check_shape((1,))