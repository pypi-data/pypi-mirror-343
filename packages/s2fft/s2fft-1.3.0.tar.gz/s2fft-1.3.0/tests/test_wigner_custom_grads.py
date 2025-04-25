import jax
import jax.numpy as jnp
import pytest
from jax.test_util import check_grads

from s2fft.recursions.price_mcewen import generate_precomputes_wigner_jax
from s2fft.transforms import wigner

jax.config.update("jax_enable_x64", True)

L_to_test = [6]
N_to_test = [3]
L_lower_to_test = [1]
sampling_to_test = ["mw", "mwss", "dh", "gl"]
reality_to_test = [False, True]


@pytest.mark.parametrize("L", L_to_test)
@pytest.mark.parametrize("N", N_to_test)
@pytest.mark.parametrize("L_lower", L_lower_to_test)
@pytest.mark.parametrize("sampling", sampling_to_test)
@pytest.mark.parametrize("reality", reality_to_test)
@pytest.mark.filterwarnings("ignore::RuntimeWarning")
def test_inverse_wigner_custom_gradients(
    flmn_generator,
    L: int,
    N: int,
    L_lower: int,
    sampling: str,
    reality: bool,
):
    precomps = generate_precomputes_wigner_jax(
        L, N, sampling, None, False, reality, L_lower
    )

    flmn = flmn_generator(L=L, N=N, L_lower=L_lower, reality=reality)
    flmn_target = flmn_generator(L=L, N=N, L_lower=L_lower, reality=reality)
    f_target = wigner.inverse_jax(
        flmn_target, L, N, None, sampling, reality, precomps, L_lower
    )

    def func(flmn):
        f = wigner.inverse_jax(flmn, L, N, None, sampling, reality, precomps, L_lower)
        return jnp.sum(jnp.abs(f - f_target) ** 2)

    check_grads(func, (flmn,), order=1, modes=("rev"))


@pytest.mark.parametrize("L", L_to_test)
@pytest.mark.parametrize("N", N_to_test)
@pytest.mark.parametrize("L_lower", L_lower_to_test)
@pytest.mark.parametrize("sampling", sampling_to_test)
@pytest.mark.parametrize("reality", reality_to_test)
@pytest.mark.filterwarnings("ignore::RuntimeWarning")
def test_forward_wigner_custom_gradients(
    flmn_generator,
    L: int,
    N: int,
    L_lower: int,
    sampling: str,
    reality: bool,
):
    precomps = generate_precomputes_wigner_jax(
        L, N, sampling, None, True, reality, L_lower
    )

    flmn_target = flmn_generator(L=L, N=N, L_lower=L_lower, reality=reality)
    flmn = flmn_generator(L=L, N=N, L_lower=L_lower, reality=reality)
    f = wigner.inverse_jax(flmn, L, N, None, sampling, reality, None, L_lower)

    def func(f):
        flmn = wigner.forward_jax(f, L, N, None, sampling, reality, precomps, L_lower)
        return jnp.sum(jnp.abs(flmn - flmn_target) ** 2)

    check_grads(func, (f,), order=1, modes=("rev"))


@pytest.mark.parametrize("L", L_to_test)
@pytest.mark.parametrize("N", N_to_test)
@pytest.mark.parametrize("L_lower", L_lower_to_test)
@pytest.mark.parametrize("sampling", sampling_to_test)
@pytest.mark.parametrize("reality", reality_to_test)
@pytest.mark.parametrize("_ssht_backend", [0, 1])
@pytest.mark.filterwarnings("ignore::RuntimeWarning")
def test_ssht_c_backend_inverse_wigner_custom_gradients(
    flmn_generator,
    L: int,
    N: int,
    L_lower: int,
    sampling: str,
    reality: bool,
    _ssht_backend: int,
):
    if sampling.lower() == "dh" and _ssht_backend == 1:
        pytest.skip("Driscoll Healy ducc0 backend gradient calculation tempremental.")

    flmn = flmn_generator(L=L, N=N, L_lower=L_lower, reality=reality)
    flmn_target = flmn_generator(L=L, N=N, L_lower=L_lower, reality=reality)
    f_target = wigner.inverse_jax(
        flmn_target, L, N, None, sampling, reality, None, L_lower
    )

    def func(flmn):
        f = wigner.inverse(
            jnp.array(flmn),
            L,
            N,
            None,
            sampling,
            "jax_ssht",
            reality,
            L_lower=L_lower,
            _ssht_backend=_ssht_backend,
        )
        return jnp.sum(jnp.abs(f - f_target) ** 2)

    check_grads(func, (flmn,), order=1, modes=("rev"))


@pytest.mark.parametrize("L", L_to_test)
@pytest.mark.parametrize("N", N_to_test)
@pytest.mark.parametrize("L_lower", L_lower_to_test)
@pytest.mark.parametrize("sampling", sampling_to_test)
@pytest.mark.parametrize("reality", reality_to_test)
@pytest.mark.parametrize("_ssht_backend", [0, 1])
@pytest.mark.filterwarnings("ignore::RuntimeWarning")
def test_ssht_c_backend_forward_wigner_custom_gradients(
    flmn_generator,
    L: int,
    N: int,
    L_lower: int,
    sampling: str,
    reality: bool,
    _ssht_backend: int,
):
    if sampling.lower() == "dh" and _ssht_backend == 1:
        pytest.skip("Driscoll Healy ducc0 backend gradient calculation tempremental.")

    flmn_target = flmn_generator(L=L, N=N, L_lower=L_lower, reality=reality)
    flmn = flmn_generator(L=L, N=N, L_lower=L_lower, reality=reality)
    f = wigner.inverse_jax(flmn, L, N, None, sampling, reality, None, L_lower)

    def func(f):
        flmn = wigner.forward(
            f,
            L,
            N,
            None,
            sampling,
            "jax_ssht",
            reality,
            L_lower=L_lower,
            _ssht_backend=_ssht_backend,
        )
        return jnp.sum(jnp.abs(flmn - flmn_target) ** 2)

    check_grads(func, (jnp.array(f),), order=1, modes=("rev"))
