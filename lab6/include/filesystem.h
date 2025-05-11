// include/filesystem.h
#pragma once

#include <string>
#include <filesystem>

class FileSystem
{
public:
    static std::string getPath(const std::string &relativePath)
    {
        return std::filesystem::current_path().string() + "/" + relativePath;
    }
};
