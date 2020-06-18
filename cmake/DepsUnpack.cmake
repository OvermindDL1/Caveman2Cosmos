
# Deps are required before building, so run it now instead of with a target
if(NOT EXISTS "${CMAKE_CURRENT_LIST_DIR}/../Build/deps/deps.v4.txt")
	message("Deps not found, unpacking")
	file(MAKE_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}/../Build")
	execute_process(
		WORKING_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}/../Build"
		COMMAND "${CMAKE_COMMAND}" -E tar xf "${CMAKE_CURRENT_LIST_DIR}/../Tools/deps.exe"
		OUTPUT_FILE "${CMAKE_CURRENT_LIST_DIR}/../deps"
	)
endif()

if(NOT EXISTS "${CMAKE_CURRENT_LIST_DIR}/../Build/deps/deps.v4.txt")
	message(FATAL_ERROR "Failed to extract v4 of deps")
endif()

