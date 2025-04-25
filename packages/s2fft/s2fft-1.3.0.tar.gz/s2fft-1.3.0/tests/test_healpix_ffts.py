import healpy as hp
import jax
import numpy as np
import pytest
from numpy.testing import assert_allclose
from packaging.version import Version as _Version

from s2fft.sampling import s2_samples as samples
from s2fft.utils.healpix_ffts import (
    healpix_fft_cuda,
    healpix_fft_jax,
    healpix_fft_numpy,
    healpix_ifft_cuda,
    healpix_ifft_jax,
    healpix_ifft_numpy,
)

if _Version(jax.__version__) < _Version("0.4.32"):
    from jax.lib.xla_bridge import get_backend
else:
    from jax.extend.backend import get_backend

gpu_available = get_backend().platform == "gpu"

jax.config.update("jax_enable_x64", True)

nside_to_test = [4, 5]
reality_to_test = [False, True]


@pytest.mark.parametrize("nside", nside_to_test)
@pytest.mark.parametrize("reality", reality_to_test)
def test_healpix_fft_jax_numpy_consistency(flm_generator, nside, reality):
    L = 2 * nside
    # Generate a random bandlimited signal
    flm = flm_generator(L=L, reality=reality)
    flm_hp = samples.flm_2d_to_hp(flm, L)
    f = hp.sphtfunc.alm2map(flm_hp, nside, lmax=L - 1)
    # Test consistency
    assert np.allclose(
        healpix_fft_numpy(f, L, nside, reality), healpix_fft_jax(f, L, nside, reality)
    )


@pytest.mark.parametrize("nside", nside_to_test)
@pytest.mark.parametrize("reality", reality_to_test)
def test_healpix_ifft_jax_numpy_consistency(flm_generator, nside, reality):
    L = 2 * nside
    # Generate a random bandlimited signal
    flm = flm_generator(L=L, reality=reality)
    flm_hp = samples.flm_2d_to_hp(flm, L)
    f = hp.sphtfunc.alm2map(flm_hp, nside, lmax=L - 1)
    ftm = healpix_fft_numpy(f, L, nside, reality)
    ftm_copy = np.copy(ftm)
    # Test consistency
    assert np.allclose(
        healpix_ifft_numpy(ftm, L, nside, reality),
        healpix_ifft_jax(ftm_copy, L, nside, reality),
    )


@pytest.mark.skipif(not gpu_available, reason="GPU not available")
@pytest.mark.parametrize("nside", nside_to_test)
def test_healpix_fft_cuda(flm_generator, nside):
    L = 2 * nside
    # Generate a random bandlimited signal
    flm = flm_generator(L=L, reality=False)
    flm_hp = samples.flm_2d_to_hp(flm, L)
    f = hp.sphtfunc.alm2map(flm_hp, nside, lmax=L - 1)
    # Test consistency
    assert_allclose(
        healpix_fft_jax(f, L, nside, False),
        healpix_fft_cuda(f, L, nside, False),
        atol=1e-7,
        rtol=1e-7,
    )


@pytest.mark.skipif(not gpu_available, reason="GPU not available")
@pytest.mark.parametrize("nside", nside_to_test)
def test_healpix_ifft_cuda(flm_generator, nside):
    L = 2 * nside
    # Generate a random bandlimited signal
    flm = flm_generator(L=L, reality=False)
    flm_hp = samples.flm_2d_to_hp(flm, L)
    f = hp.sphtfunc.alm2map(flm_hp, nside, lmax=L - 1)
    ftm = healpix_fft_jax(f, L, nside, False)
    # Test consistency
    assert_allclose(
        healpix_ifft_jax(ftm, L, nside, False).flatten(),
        healpix_ifft_cuda(ftm, L, nside, False).flatten(),
        atol=1e-7,
        rtol=1e-7,
    )
