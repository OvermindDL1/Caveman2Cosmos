# This toolchain requires the dependencies to already be extracted
include("${CMAKE_CURRENT_LIST_DIR}/DepsUnpack.cmake")

set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_SYSTEM_PROCESSOR x86)

# No sysroot
# No staging prefix

set(CMAKE_CXX_COMPILER "${CMAKE_CURRENT_LIST_DIR}/bin/cl.exe")
set(CMAKE_CXX_COMPILER_ID MSVC)
set(CMAKE_LINKER "${CMAKE_CURRENT_LIST_DIR}/bin/link.exe")
set(CMAKE_CXX_IMPLICIT_LINK_DIRECTORIES
	"${CMAKE_CURRENT_LIST_DIR}/../Build/deps/Microsoft Visual C++ Toolkit 2003/lib"
)

set(CMAKE_CXX_LINK_EXECUTABLE "'${CMAKE_CURRENT_LIST_DIR}/bin/link.exe' <FLAGS> <CMAKE_CXX_LINK_FLAGS> <LINK_FLAGS> <OBJECTS>  -o <TARGET> <LINK_LIBRARIES>")

