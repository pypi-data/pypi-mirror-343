#include "zarrv2.array.writer.hh"

#include "definitions.hh"
#include "macros.hh"
#include "sink.hh"
#include "zarr.common.hh"

#include <nlohmann/json.hpp>

#include <latch>
#include <semaphore>
#include <stdexcept>

namespace {
[[nodiscard]]
bool
sample_type_to_dtype(ZarrDataType t, std::string& t_str)

{
    const std::string dtype_prefix =
      std::endian::native == std::endian::big ? ">" : "<";

    switch (t) {
        case ZarrDataType_uint8:
            t_str = dtype_prefix + "u1";
            break;
        case ZarrDataType_uint16:
            t_str = dtype_prefix + "u2";
            break;
        case ZarrDataType_uint32:
            t_str = dtype_prefix + "u4";
            break;
        case ZarrDataType_uint64:
            t_str = dtype_prefix + "u8";
            break;
        case ZarrDataType_int8:
            t_str = dtype_prefix + "i1";
            break;
        case ZarrDataType_int16:
            t_str = dtype_prefix + "i2";
            break;
        case ZarrDataType_int32:
            t_str = dtype_prefix + "i4";
            break;
        case ZarrDataType_int64:
            t_str = dtype_prefix + "i8";
            break;
        case ZarrDataType_float32:
            t_str = dtype_prefix + "f4";
            break;
        case ZarrDataType_float64:
            t_str = dtype_prefix + "f8";
            break;
        default:
            LOG_ERROR("Unsupported sample type: ", t);
            return false;
    }

    return true;
}
} // namespace

zarr::ZarrV2ArrayWriter::ZarrV2ArrayWriter(
  const ArrayWriterConfig& config,
  std::shared_ptr<ThreadPool> thread_pool)
  : ArrayWriter(config, thread_pool)
{
}

zarr::ZarrV2ArrayWriter::ZarrV2ArrayWriter(
  const ArrayWriterConfig& config,
  std::shared_ptr<ThreadPool> thread_pool,
  std::shared_ptr<S3ConnectionPool> s3_connection_pool)
  : ArrayWriter(config, thread_pool, s3_connection_pool)
{
}

std::string
zarr::ZarrV2ArrayWriter::data_root_() const
{
    return config_.store_path + "/" + std::to_string(config_.level_of_detail) +
           "/" + std::to_string(append_chunk_index_);
}

std::string
zarr::ZarrV2ArrayWriter::metadata_path_() const
{
    return config_.store_path + "/" + std::to_string(config_.level_of_detail) +
           "/.zarray";
}

const DimensionPartsFun
zarr::ZarrV2ArrayWriter::parts_along_dimension_() const
{
    return chunks_along_dimension;
}

void
zarr::ZarrV2ArrayWriter::make_buffers_()
{
    LOG_DEBUG("Creating chunk buffers");

    const size_t n_chunks = config_.dimensions->number_of_chunks_in_memory();
    data_buffers_.resize(n_chunks); // no-op if already the correct size

    const auto n_bytes = bytes_to_allocate_per_chunk_();

    for (auto& buf : data_buffers_) {
        buf.resize(n_bytes);
        std::fill(buf.begin(), buf.end(), std::byte(0));
    }
}

BytePtr
zarr::ZarrV2ArrayWriter::get_chunk_data_(uint32_t index)
{
    return data_buffers_[index].data();
}

bool
zarr::ZarrV2ArrayWriter::compress_and_flush_data_()
{
    // construct paths to chunk sinks
    CHECK(data_paths_.empty());
    make_data_paths_();

    const auto n_chunks = data_buffers_.size();
    CHECK(data_paths_.size() == n_chunks);

    const auto compression_params = config_.compression_params;
    const auto bytes_of_raw_chunk = config_.dimensions->bytes_per_chunk();
    const auto bytes_per_px = bytes_of_type(config_.dtype);
    const auto bucket_name = config_.bucket_name;
    auto connection_pool = s3_connection_pool_;

    // create parent directories if needed
    const auto is_s3 = is_s3_array_();
    if (!is_s3) {
        const auto parent_paths = get_parent_paths(data_paths_);
        CHECK(make_dirs(parent_paths, thread_pool_));
    }

    std::atomic<char> all_successful = 1;
    std::latch latch(n_chunks);
    {
        std::scoped_lock lock(buffers_mutex_);
        std::counting_semaphore<MAX_CONCURRENT_FILES> semaphore(
          MAX_CONCURRENT_FILES);

        for (auto i = 0; i < n_chunks; ++i) {
            EXPECT(thread_pool_->push_job(
                     std::move([bytes_per_px,
                                bytes_of_raw_chunk,
                                &compression_params,
                                is_s3,
                                &data_path = data_paths_[i],
                                chunk_ptr = get_chunk_data_(i),
                                &bucket_name,
                                connection_pool,
                                &semaphore,
                                &latch,
                                &all_successful](std::string& err) {
                         bool success = true;
                         if (!all_successful) {
                             latch.count_down();
                             return false;
                         }

                         auto bytes_of_chunk = bytes_of_raw_chunk;

                         try {
                             // compress the chunk
                             if (compression_params) {
                                 const int nb = compress_buffer_in_place(
                                   chunk_ptr,
                                   bytes_of_raw_chunk + BLOSC_MAX_OVERHEAD,
                                   bytes_of_chunk,
                                   *compression_params,
                                   bytes_per_px);

                                 EXPECT(nb > 0, "Failed to compress chunk.");
                                 bytes_of_chunk = nb;
                             }

                             // create a new sink
                             std::unique_ptr<Sink> sink;
                             semaphore.acquire();

                             if (is_s3) {
                                 sink = make_s3_sink(
                                   *bucket_name, data_path, connection_pool);
                             } else {
                                 sink = make_file_sink(data_path);
                             }

                             // write the chunk to the sink
                             std::span chunk_data(chunk_ptr, bytes_of_chunk);
                             if (!sink->write(0, chunk_data)) {
                                 err = "Failed to write chunk";
                                 success = false;
                             }
                             EXPECT(finalize_sink(std::move(sink)),
                                    "Failed to finalize sink at path ",
                                    data_path);

                             semaphore.release();
                             latch.count_down();
                         } catch (const std::exception& exc) {
                             semaphore.release();
                             latch.count_down();
                             err = exc.what();

                             success = false;
                         }

                         all_successful.fetch_and(static_cast<char>(success));
                         return success;
                     })),
                   "Failed to push job to thread pool");
        }
    }

    latch.wait();
    return static_cast<bool>(all_successful);
}

bool
zarr::ZarrV2ArrayWriter::write_array_metadata_()
{
    if (!make_metadata_sink_()) {
        return false;
    }

    using json = nlohmann::json;

    std::string dtype;
    if (!sample_type_to_dtype(config_.dtype, dtype)) {
        return false;
    }

    std::vector<size_t> array_shape, chunk_shape;

    size_t append_size = frames_written_;
    for (auto i = config_.dimensions->ndims() - 3; i > 0; --i) {
        const auto& dim = config_.dimensions->at(i);
        const auto& array_size_px = dim.array_size_px;
        CHECK(array_size_px);
        append_size = (append_size + array_size_px - 1) / array_size_px;
    }
    array_shape.push_back(append_size);

    chunk_shape.push_back(config_.dimensions->final_dim().chunk_size_px);
    for (auto i = 1; i < config_.dimensions->ndims(); ++i) {
        const auto& dim = config_.dimensions->at(i);
        array_shape.push_back(dim.array_size_px);
        chunk_shape.push_back(dim.chunk_size_px);
    }

    json metadata;
    metadata["zarr_format"] = 2;
    metadata["shape"] = array_shape;
    metadata["chunks"] = chunk_shape;
    metadata["dtype"] = dtype;
    metadata["fill_value"] = 0;
    metadata["order"] = "C";
    metadata["filters"] = nullptr;
    metadata["dimension_separator"] = "/";

    if (config_.compression_params) {
        const BloscCompressionParams bcp = *config_.compression_params;
        metadata["compressor"] = json{ { "id", "blosc" },
                                       { "cname", bcp.codec_id },
                                       { "clevel", bcp.clevel },
                                       { "shuffle", bcp.shuffle } };
    } else {
        metadata["compressor"] = nullptr;
    }

    std::string metadata_str = metadata.dump(4);
    std::span data{ reinterpret_cast<std::byte*>(metadata_str.data()),
                    metadata_str.size() };
    return metadata_sink_->write(0, data);
}

void
zarr::ZarrV2ArrayWriter::close_sinks_()
{
    data_paths_.clear();
}

bool
zarr::ZarrV2ArrayWriter::should_rollover_() const
{
    return true;
}
