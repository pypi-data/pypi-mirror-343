#ifndef __AIDGE_EXPORT_CPP_KERNELS_RESHAPE__
#define __AIDGE_EXPORT_CPP_KERNELS_RESHAPE__

#include "network/typedefs.hpp"

// Generic function for reshape and activation

template<int M,
         typename Input_T, typename Output_T>
__attribute__((always_inline)) inline
void reshape_forward (
    const Input_T* __restrict, // First input is useless as it only dictate the resulting layout of the reshape
    const Input_T* __restrict inputs2,
    Output_T* __restrict outputs)
{
    // If inputs and outputs pointers are the same, the memory manager has already optimized this function so it is a no-op !
    if (inputs2 == outputs)
        return;

    // A reshape in c++ world should equal to a Noop
    // We only need to copy the input buffer to the output
    for (int m = 0; m < M; ++m) {
        outputs[m] = inputs2[m];
    }
}

#endif  // __AIDGE_EXPORT_CPP_KERNELS_RESHAPE__