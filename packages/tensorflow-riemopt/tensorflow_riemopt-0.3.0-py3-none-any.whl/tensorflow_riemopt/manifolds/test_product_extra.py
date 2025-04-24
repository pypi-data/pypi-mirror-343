import pytest
import tensorflow as tf

from tensorflow_riemopt.manifolds.product import Product
from tensorflow_riemopt.manifolds.euclidean import Euclidean

def test_product_repr_and_invalid():
    # valid product
    m = Product((Euclidean(), (2,)), (Euclidean(), (3,)))
    r = repr(m)
    assert 'Euclidean(2' in r and 'Euclidean(3' in r

    # invalid manifold in constructor
    with pytest.raises(ValueError):
        Product((42, (2,)))

    # invalid shape in constructor
    with pytest.raises(ValueError):
        Product((Euclidean(), (2,)), (Euclidean(), (4,)))

    # invalid get_slice index
    x = tf.random.uniform((5,))
    with pytest.raises(ValueError):
        m._get_slice(x, 2)

def test_random_and_dist_inner():
    m = Product((Euclidean(), (2,)), (Euclidean(), (1,)))
    # test random with correct shape
    x = m.random((4, 3))
    assert x.shape == (4, 3)

    # test random invalid shape
    with pytest.raises(ValueError):
        m.random((4, 4))

    # test dist and inner
    x = tf.constant([[1.0, 2.0, 3.0]])
    y = tf.constant([[4.0, 6.0, 3.0]])
    d = m.dist(x, y)
    # expected Euclidean dist = sqrt((1-4)^2 + (2-6)^2 + 0)
    assert pytest.approx(5.0, rel=1e-6) == d.numpy()[0]
    # inner should be sum of squared differences
    diff = y - x
    i = m.inner(x, diff, diff)
    assert pytest.approx(25.0, rel=1e-6) == i.numpy()[0]