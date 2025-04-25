#pragma once

#include <span>
#include <vector>

using ByteVector = std::vector<std::byte>;
using BytePtr = std::byte*;

using ByteSpan = std::span<std::byte>;
using ConstByteSpan = std::span<const std::byte>;

constexpr int MAX_CONCURRENT_FILES = 256;
