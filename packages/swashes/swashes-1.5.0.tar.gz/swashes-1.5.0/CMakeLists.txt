# Minimum CMake version required (FetchContent needs >= 3.11, using 3.18 as per pyproject)
cmake_minimum_required(VERSION 3.18)

# Set recommended policies
cmake_policy(SET CMP0135 NEW) # Use extraction time for FetchContent timestamps

# Define the project name (can be different from the Python package name)
project(swashes_build LANGUAGES CXX C) # Assuming C/C++ needed by upstream

# Include the FetchContent module for downloading external dependencies
include(FetchContent)

# --- Fetch Upstream SWASHES Source ---
message(STATUS "Declaring FetchContent for SWASHES")
FetchContent_Declare(
    swashes_upstream # Name for this dependency in CMake
    URL https://sourcesup.renater.fr/frs/download.php/file/6718/SWASHES-1.05.00.zip
    # Optional: Add URL_HASH SHA256=... for checksum verification if known
)

# Make the content available (downloads and extracts if not already done)
# This populates swashes_upstream_SOURCE_DIR and swashes_upstream_BINARY_DIR
# By default, source is extracted to: ${CMAKE_BINARY_DIR}/_deps/swashes_upstream-src
# We specify SOURCE_DIR to potentially place it elsewhere if needed, but default is fine.
message(STATUS "Making FetchContent available for SWASHES")
FetchContent_MakeAvailable(swashes_upstream)

# Check if the source directory variable is populated (should be)
if(NOT swashes_upstream_SOURCE_DIR)
    message(FATAL_ERROR "swashes_upstream_SOURCE_DIR is not defined after FetchContent_MakeAvailable")
endif()
message(STATUS "SWASHES source directory: ${swashes_upstream_SOURCE_DIR}")

# --- Define SWASHES Build Target Directly ---
message(STATUS "Defining SWASHES executable target from upstream sources")

# Glob the source files from the downloaded directory
file(GLOB SWASHES_SOURCES "${swashes_upstream_SOURCE_DIR}/Sources/*.cpp")

# Define the executable target using the collected source files
add_executable(swashes ${SWASHES_SOURCES})

# Specify the include directory for headers
target_include_directories(swashes PUBLIC ${swashes_upstream_SOURCE_DIR}/Headers)

# --- Install the Built Executable ---
message(STATUS "Installing SWASHES executable target to bin directory")

# Install the 'swashes' target built by CMake.
install(
    TARGETS swashes
    RUNTIME DESTINATION bin # Install executables to <prefix>/bin
    COMPONENT swashes_runtime # Optional component name
)

message(STATUS "CMake configuration for SWASHES wrapper finished.")