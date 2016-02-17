cmake_minimum_required (VERSION 2.6) 
project (cudeform)

#Set binary dir
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/bin)

# add cmake find modules
set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake) 

# Use folders in MSVC
set_property(GLOBAL PROPERTY USE_FOLDERS true)

# Export compile for YCM
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Add test project
enable_testing ()
add_definitions(-DCTEST_OUTPUT_ON_FAILURE)

# Add cuda
find_package(CUDA QUIET REQUIRED)

# Pass options to NVCC
set(CUDA_COMPUTE "52" CACHE STRING "Cuda compute capability to compile for")
set(CUDA_NVCC_FLAGS ${CUDA_NVCC_FLAGS};-gencode arch=compute_${CUDA_COMPUTE},code=sm_${CUDA_COMPUTE})

# Enable fast math
option(CUDA_USE_FAST_MATH "Enable fast math in cuda (can decrease precision)" TRUE)
if(CUDA_USE_FAST_MATH)
	set(CUDA_NVCC_FLAGS ${CUDA_NVCC_FLAGS};-use_fast_math)
endif()

# C++ flags
if (MSVC)
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /wd4251")
    
    #Set warning level 3
    if(CMAKE_CXX_FLAGS MATCHES "/W[0-4]")
        string(REGEX REPLACE "/W[0-4]" "/W3" CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")
    else()
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W3")
    endif()
else()
	include(CheckCXXCompilerFlag)
	CHECK_CXX_COMPILER_FLAG("-std=c++11" COMPILER_SUPPORTS_CXX11)
	CHECK_CXX_COMPILER_FLAG("-std=c++0x" COMPILER_SUPPORTS_CXX0X)
	if(COMPILER_SUPPORTS_CXX11)
		set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
	elseif()
		set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
	else()
		message(STATUS "The compiler ${CMAKE_CXX_COMPILER} has no C++11 support. Please use a different C++ compiler.")
	endif()

    #Position independent code is needed to link shared-static
    set(CMAKE_POSITION_INDEPENDENT_CODE TRUE)    

    #Set proper flag propagation for cuda
	set(CUDA_PROPAGATE_HOST_FLAGS OFF)

    #Enable c++11
	set(CUDA_NVCC_FLAGS ${CUDA_NVCC_FLAGS}; -std=c++11 -Xcompiler -fPIC)
endif()


# Python bindings
option(PYTHON_ENABLED "Create python bindings" FALSE)
if(PYTHON_ENABLED)
	set(Boost_USE_SHARED_LIBS   ON)
	set(Boost_USE_MULTITHREADED ON)
	find_package(Boost COMPONENTS
                 python
				 REQUIRED)
	include_directories(${Boost_INCLUDE_DIRS})
	link_directories(${Boost_LIBRARY_DIRS})
	
	# Find python
	find_package(PythonLibs REQUIRED)
	include_directories(${PYTHON_INCLUDE_DIRS})
	
	# Find numpy
	find_package(Numpy REQUIRED)
	include_directories(${PYTHON_NUMPY_INCLUDE_DIR})
	
	link_directories(${PYTHON_LIBRARIES})

    #disable old
    add_definitions(-DNPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION)
endif(PYTHON_ENABLED)

# Dependencies
if(NOT EXISTS "${CMAKE_SOURCE_DIR}/odl-cpp-utils/CMakeLists.txt")
    message(SEND_ERROR "odl-cpp-utils not initialized. Run 'git submodule update --init'." )
endif()
add_subdirectory(odl-cpp-utils)

# Add sub directories as needed
add_subdirectory(cudeform)
