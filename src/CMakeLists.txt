cmake_minimum_required (VERSION 2.6)
project (Handicap)

include_directories("${PROJECT_BINARY_DIR}")
include_directories ("${PROJECT_SOURCE_DIR}/db")
add_subdirectory (db)

add_executable(Handicap main.cpp)
target_link_libraries(Handicap db)