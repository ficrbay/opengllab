cmake_minimum_required(VERSION 3.10)
project(OpenGL_Project)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(BREW_PREFIX "/opt/homebrew")

include_directories(
    ${PROJECT_SOURCE_DIR}/include
    ${PROJECT_SOURCE_DIR}/learnopengl
    ${BREW_PREFIX}/include
)

link_directories(${BREW_PREFIX}/lib)

find_library(OPENGL_LIBRARY OpenGL)
find_package(PkgConfig REQUIRED)
pkg_search_module(GLFW REQUIRED glfw3)
find_library(ASSIMP_LIBRARY assimp HINTS ${BREW_PREFIX}/lib)

file(GLOB SRC_FILES
     ${PROJECT_SOURCE_DIR}/src/*.cpp
     ${PROJECT_SOURCE_DIR}/src/glad.c
     ${PROJECT_SOURCE_DIR}/src/texture_utils.cpp)  # 加载纹理辅助函数

add_definitions(-DGL_SILENCE_DEPRECATION)

add_executable(OpenGL_Project ${SRC_FILES})

add_custom_command(TARGET OpenGL_Project POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
            ${PROJECT_SOURCE_DIR}/backpack
            $<TARGET_FILE_DIR:OpenGL_Project>/backpack)

add_custom_command(TARGET OpenGL_Project POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
            ${PROJECT_SOURCE_DIR}/shaders
            $<TARGET_FILE_DIR:OpenGL_Project>/shaders)

add_custom_command(TARGET OpenGL_Project POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
            ${PROJECT_SOURCE_DIR}/textures
            $<TARGET_FILE_DIR:OpenGL_Project>/textures)

add_custom_command(TARGET OpenGL_Project POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
            ${PROJECT_SOURCE_DIR}/skybox
            $<TARGET_FILE_DIR:OpenGL_Project>/skybox)

target_link_libraries(OpenGL_Project
    ${OPENGL_LIBRARY}
    ${GLFW_LIBRARIES}
    ${ASSIMP_LIBRARY})
