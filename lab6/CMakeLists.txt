cmake_minimum_required(VERSION 3.10)
project(OpenGL_Project)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Homebrew 默认前缀（Apple Silicon 如无特殊情况保持 /opt/homebrew）
set(BREW_PREFIX "/opt/homebrew")

# ---------------------------------------------------------------------------
# 头文件 / 库路径
# ---------------------------------------------------------------------------
include_directories(
    ${PROJECT_SOURCE_DIR}/include          # glad、stb_image、etc.
    ${PROJECT_SOURCE_DIR}/learnopengl      # camera.h / shader_m.h / model.h
    ${BREW_PREFIX}/include                 # glfw3, glm, assimp
)

link_directories(${BREW_PREFIX}/lib)

# ---------------------------------------------------------------------------
# 查找系统 / 第三方库
# ---------------------------------------------------------------------------
find_library(OPENGL_LIBRARY OpenGL)
find_package(PkgConfig REQUIRED)
pkg_search_module(GLFW REQUIRED glfw3)
find_library(ASSIMP_LIBRARY assimp HINTS ${BREW_PREFIX}/lib)


file(GLOB SRC_FILES
     ${PROJECT_SOURCE_DIR}/src/*.cpp
     ${PROJECT_SOURCE_DIR}/src/glad.c
     ${PROJECT_SOURCE_DIR}/src/stb_image.h
     ${PROJECT_SOURCE_DIR}/src/texture_utils.cpp)   
add_definitions(-DGL_SILENCE_DEPRECATION)

add_executable(OpenGL_Project ${SRC_FILES})

# ---------------------------------------------------------------------------
# 运行目录下需要的资源：模型 / 着色器 / 纹理 / 天空盒
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# 链接库
# ---------------------------------------------------------------------------
target_link_libraries(OpenGL_Project
    ${OPENGL_LIBRARY}
    ${GLFW_LIBRARIES}
    ${ASSIMP_LIBRARY})
