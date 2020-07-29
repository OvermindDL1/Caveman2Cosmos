set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_SYSTEM_PROCESSOR x86)

# No sysroot
# No staging prefix

#set(tools "${CMAKE_SOURCE_DIR}/Build/deps/Microsoft Visual C++ Toolkit 2003")
set(tools "${CMAKE_SOURCE_DIR}/cmake")
#set(CMAKE_C_COMPILER "${tools}/bin/cl.exe
set(CMAKE_CXX_COMPILER "${tools}/bin/cl.exe")
set(CMAKE_CXX_COMPILER_ID MSVC)
set(CMAKE_LINKER "${tools}/bin/link.exe")
set(CMAKE_CXX_IMPLICIT_LINK_DIRECTORIES
	"${CMAKE_SOURCE_DIR}/Build/deps/Microsoft Visual C++ Toolkit 2003/lib"
)

set(CMAKE_CXX_LINK_EXECUTABLE "'${tools}/bin/link.exe' <FLAGS> <CMAKE_CXX_LINK_FLAGS> <LINK_FLAGS> <OBJECTS>  -o <TARGET> <LINK_LIBRARIES>")

message("Using WINE-MSVC-2002 toolchain")
