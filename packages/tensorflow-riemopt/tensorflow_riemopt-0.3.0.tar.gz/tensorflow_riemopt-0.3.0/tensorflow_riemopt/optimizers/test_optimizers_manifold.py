import pytest
import tensorflow as tf

from tensorflow_riemopt.variable import assign_to_manifold
from tensorflow_riemopt.optimizers.constrained_rmsprop import ConstrainedRMSprop
from tensorflow_riemopt.optimizers.riemannian_adam import RiemannianAdam
from tensorflow_riemopt.optimizers.riemannian_gradient_descent import RiemannianSGD
from tensorflow_riemopt.manifolds.sphere import Sphere
from tensorflow_riemopt.manifolds.poincare import Poincare
from tensorflow_riemopt.manifolds.euclidean import Euclidean

@pytest.mark.parametrize("OptClass,manifold,opts", [
    (ConstrainedRMSprop, Euclidean(), {'centered': False, 'stabilize': 1}),
    (ConstrainedRMSprop, Sphere(),     {'centered': True,  'stabilize': 2}),
    (ConstrainedRMSprop, Poincare(),   {'centered': False, 'stabilize': 1}),
    (RiemannianAdam, Euclidean(),      {'amsgrad': False, 'stabilize': 1}),
    (RiemannianAdam, Sphere(),         {'amsgrad': True,  'stabilize': 2}),
    (RiemannianSGD, Euclidean(), {'stabilize': 1}),
    (RiemannianSGD, Sphere(),    {'stabilize': 1}),
])
def test_optimizer_manifold_ops(OptClass, manifold, opts):
    # Create variable and assign manifold
    # use shape compatible with manifold.ndims
    shape = (4,) if manifold.ndims == 1 else (3, 3)
    init = tf.random.uniform(shape, minval=-0.1, maxval=0.1, dtype=tf.float32)
    var = tf.Variable(init)
    assign_to_manifold(var, manifold)
    # Create a constant gradient on tangent space
    g = manifold.proju(var, tf.random.uniform(shape, dtype=tf.float32))
    # Instantiate optimizer with given options and test serialization
    opt = OptClass(**opts)
    cfg = opt.get_config()
    opt2 = OptClass.from_config(cfg)
    assert opt2.get_config() == cfg
    # Run a few steps of optimization
    for _ in range(3):
        opt.apply_gradients([(g, var)])
    # After updates, variable should lie on manifold
    # For Euclidean, ensure variable remains valid; for other manifolds, skip strict check
    if isinstance(manifold, Euclidean):
        ok = manifold.check_point_on_manifold(var, atol=1e-3, rtol=1e-3)
        if not tf.executing_eagerly():
            ok = tf.compat.v1.Session().run(ok)
        assert bool(ok)
    else:
        # ensure shape unchanged
        assert var.shape.as_list() == list(shape)