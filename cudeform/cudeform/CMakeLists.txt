set(Headers
    cudeform3d.h)

set(Sources
	dummy.cpp)
	
set(CudaFiles
	cudeform3d.cu)

include_directories ("${PROJECT_SOURCE_DIR}")
cuda_include_directories ("${PROJECT_SOURCE_DIR}")

source_group ("CUDA Source Files" FILES ${CudaFiles})

CUDA_ADD_LIBRARY(cudeform STATIC 
	${Headers} 
	${Sources} 
	${CudaFiles}
)
