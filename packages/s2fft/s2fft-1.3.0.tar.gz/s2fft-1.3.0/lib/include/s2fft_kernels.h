#ifndef _S2FFT_KERNELS_H
#define _S2FFT_KERNELS_H

#include "hresult.h"
#include <cmath>  // has to be included before cuda/std/complex
#include <cstddef>
#include <cuda/std/complex>
#include "cufft.h"
#include <cufftXt.h>
typedef long long int int64;

namespace s2fftKernels {

template <typename complex>
HRESULT launch_spectral_folding(complex* data, complex* output, const int& nside, const int& L,
                                const bool& shift, cudaStream_t stream);
template <typename complex>
HRESULT launch_spectral_extension(complex* data, complex* output, const int& nside, const int& L,
                                  cudaStream_t stream);
}  // namespace s2fftKernels

#endif  // _S2FFT_KERNELS_H