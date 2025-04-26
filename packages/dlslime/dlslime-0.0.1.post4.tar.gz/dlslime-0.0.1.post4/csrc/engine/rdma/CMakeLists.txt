find_package(CUDAToolkit REQUIRED)

set(CMAKE_CUDA_ARCHITECTURES "70;80;90")

add_library(
    _slime_rdma
    SHARED
    memory_pool.cpp
    rdma_transport.cpp
    rdma_scheduler.cpp
)

target_link_libraries(_slime_rdma PUBLIC _slime_engine _slime_utils ibverbs cuda CUDA::cudart zmq)
