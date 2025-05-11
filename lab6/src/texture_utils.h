#pragma once
#include <glad/glad.h>
#include <vector>
#include <string>

unsigned int loadTexture(const char* path, bool gammaCorrection = false);
unsigned int loadCubemap(const std::vector<std::string>& faces);
