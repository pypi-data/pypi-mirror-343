// -----------------------------------------------------------------------------
// src/genome_ninja/_cpp/fast_reader.hpp (API declaration)
// -----------------------------------------------------------------------------

#pragma once
#include <filesystem>
#include <vector>
#include <cstdint>

std::uint64_t uncompressed_bytes(const std::vector<std::filesystem::path>& files,
                                 unsigned threads = 8);
