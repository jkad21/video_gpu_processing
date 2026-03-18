cmake_minimum_required(VERSION 3.10)
project(VideoGPUProcessing CUDA CXX)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CUDA_STANDARD 14)

# Find CUDA
find_package(CUDA REQUIRED)

# CUDA settings
set(CUDA_NVCC_FLAGS "${CUDA_NVCC_FLAGS} -arch=sm_35")

# Include directories
include_directories(${CUDA_INCLUDE_DIRS})

# Source files
set(CUDA_SOURCES
    cuda_kernels.cu
)

# Create CUDA library
cuda_add_library(cuda_kernels SHARED ${CUDA_SOURCES})

# Link CUDA runtime
target_link_libraries(cuda_kernels ${CUDA_LIBRARIES})

# Installation
install(TARGETS cuda_kernels DESTINATION lib)

# Python binding support
message(STATUS "CUDA Capability: ${CMAKE_CUDA_ARCHITECTURES}")
message(STATUS "CUDA Libraries: ${CUDA_LIBRARIES}")
