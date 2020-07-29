cmake_minimum_required(VERSION 3.13)

project(C2C CXX)

if(CMAKE_BUILD_TYPE STREQUAL "DEBUG")
	set(IS_DEBUG ON)
else(CMAKE_BUILD_TYPE STREQUAL "DEBUG")
	set(IS_DEBUG OFF)
endif(CMAKE_BUILD_TYPE STREQUAL "DEBUG")

option(C2C_LOG_AI "Enable AI Logging code" ${DEBUG})
option(C2C_FASSERT_ENABLE "Enable FAssert code" ${DEBUG})

# This is *such* bad form...
file(GLOB CvGameCoreDLL_SOURCES "${CMAKE_SOURCE_DIR}/Sources/*.cpp")

add_library(CvGameCoreDLL
	${CvGameCoreDLL_SOURCES}
)

target_compile_definitions(CvGameCoreDLL PUBLIC
	_USRDLL # Required to build a linkable DLL
	XERCES_STATIC_LIBRARY # Link XERCES staticly
	_MOD_FRACTRADE # Code breaks without this, no option for it unless fixed
	# Unsure if required or not, maybe make an option for the rest of these?
	_MOD_SENTRY
	_MOD_GOVWORKERS
)

if(C2C_LOG_AI)
	target_compile_definitions(CvGameCoreDLL PUBLIC LOG_AI)
endif(C2C_LOG_AI)

if(C2C_FASSERT_ENABLE)
	target_compile_definitions(CvGameCoreDLL_SOURCES PUBLIC FASSERT_ENABLE)
endif(C2C_FASSERT_ENABLE)

target_include_directories(CvGameCoreDLL SYSTEM BEFORE PUBLIC
	#set_property(TARGET CvGameCoreDLL PROPERTY INCLUDE_DIRECTORIES
	"${CMAKE_SOURCE_DIR}/Build/deps/Microsoft Visual C++ Toolkit 2003/include"
	"${CMAKE_SOURCE_DIR}/Build/deps/Microsoft SDKs/Windows/v6.0/Include"
	"${CMAKE_SOURCE_DIR}/Build/deps/Python24/include"
	"${CMAKE_SOURCE_DIR}/Build/deps/Boost-1.32.0/include"
	"${CMAKE_SOURCE_DIR}/Build/deps/Boost-1.55.0/include" # Yes really...
)

target_include_directories(CvGameCoreDLL PUBLIC
	"${CMAKE_SOURCE_DIR}/Sources"
	"${CMAKE_SOURCE_DIR}/Sources/include"
)

target_link_directories(CvGameCoreDLL PUBLIC
	"${CMAKE_SOURCE_DIR}/Build/deps/Microsoft Visual C++ Toolkit 2003/lib"
)

