// -----------------------------------------------------------------------------
// src/genome_ninja/_cpp/fast_reader.cpp (implementation skeleton)
// -----------------------------------------------------------------------------
#include "fast_reader.hpp"
#include <zlib.h>
#include <future>

static std::uint64_t one_file(const std::filesystem::path& p) {
    gzFile fp = gzopen(p.string().c_str(), "rb");
    if (!fp) return 0;
    char buf[1 << 20];
    std::uint64_t total = 0;
    int n;
    while ((n = gzread(fp, buf, sizeof buf)) > 0) total += n;
    gzclose(fp);
    return total;
}

std::uint64_t uncompressed_bytes(const std::vector<std::filesystem::path>& files,
                                 unsigned threads) {
    std::vector<std::future<std::uint64_t>> fut;
    for (auto& f : files) {
        fut.emplace_back(std::async(std::launch::async, one_file, f));
    }
    std::uint64_t sum = 0;
    for (auto& r : fut) sum += r.get();
    return sum;
}
