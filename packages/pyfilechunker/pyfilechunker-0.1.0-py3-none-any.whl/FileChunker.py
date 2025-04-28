import os
import mmap
import shutil # Add shutil import for file operations
from loguru import logger

def chunk_preview(filename: str, num_chunks: int, record_begin: str, record_end: str, log_queue=None) -> list[int]:
    def _log(message):
        if log_queue:
            log_queue.put(message)
        else:
            logger.info(message)

    file_size = os.path.getsize(filename)
    if file_size == 0:
        _log("Warning: Input file is empty.")
        return [0, 0]
    if num_chunks <= 0:
        _log("Warning: Number of chunks must be positive. Defaulting to 1 chunk.")
        num_chunks = 1
    if num_chunks == 1:
        return [0, file_size]

    boundaries = [0]
    target_positions = [i * (file_size // num_chunks) for i in range(1, num_chunks)]

    try:
        with open(filename, "r+b") as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                for target in target_positions:
                    window_size = min(20 * 1024 * 1024, file_size // num_chunks if num_chunks > 0 else file_size)
                    window_start = max(0, target - window_size // 2)
                    window_end = min(file_size, target + window_size)

                    rb_bytes = record_begin.encode('utf-8', errors='replace')
                    re_bytes = record_end.encode('utf-8', errors='replace')

                    search_area_before = mm[window_start:min(target + len(re_bytes), window_end)]
                    last_end_pos = search_area_before.rfind(re_bytes, 0, target - window_start + len(re_bytes))

                    if last_end_pos != -1:
                        safe_boundary = window_start + last_end_pos + len(re_bytes)
                        boundaries.append(safe_boundary)
                        _log(f"Boundary found after record_end near {target:,} at {safe_boundary:,}")
                        continue

                    search_area_after = mm[max(0, target - len(rb_bytes)):window_end]
                    first_begin_pos = search_area_after.find(rb_bytes)

                    if first_begin_pos != -1:
                        safe_boundary = max(0, target - len(rb_bytes)) + first_begin_pos
                        if safe_boundary > boundaries[-1]:
                            boundaries.append(safe_boundary)
                            _log(f"Boundary found at record_begin near {target:,} at {safe_boundary:,}")
                            continue
                        else:
                            _log(f"Warning: Found record_begin at {safe_boundary:,} but it's before previous boundary {boundaries[-1]:,}. Using target fallback.")
                            boundaries.append(max(target, boundaries[-1] + 1))
                            continue

                    _log(f"Warning: No safe boundary found near {target:,}. Using target fallback position.")
                    boundaries.append(max(target, boundaries[-1] + 1))

    except FileNotFoundError:
        logger.error(f"Error: Input file not found: {filename}")
        raise
    except Exception as e:
        logger.exception(f"Error finding boundaries: {e}")
        raise

    boundaries.append(file_size)
    boundaries = sorted(list(set(b for b in boundaries if 0 <= b <= file_size)))

    if not boundaries or boundaries[0] != 0:
        boundaries.insert(0, 0)
    if boundaries[-1] != file_size:
        boundaries.append(file_size)
    boundaries = sorted(list(set(boundaries)))

    _log(f"Previewed boundaries ({len(boundaries)-1} chunks): {boundaries}")
    return boundaries

def chunk_it(filename: str, num_chunks: int, record_begin: str, record_end: str, output_dir: str = ".", log_queue=None) -> list[str]:
    """
    Chunks the input file into smaller files based on record boundaries.

    Args:
        filename: Path to the input file.
        num_chunks: Desired number of chunks.
        record_begin: String marking the beginning of a record.
        record_end: String marking the end of a record.
        output_dir: Directory to save the chunk files. Defaults to current dir.
        log_queue: Optional queue for logging in multiprocessing scenarios.

    Returns:
        A list of paths to the created chunk files.
    """
    def _log(message):
        if log_queue:
            log_queue.put(message)
        else:
            logger.info(message)

    _log(f"Starting chunking process for '{filename}' into {num_chunks} chunks.")
    os.makedirs(output_dir, exist_ok=True) # Ensure output directory exists

    # 1. Get the boundaries using the preview function
    boundaries = chunk_preview(filename, num_chunks, record_begin, record_end, log_queue)
    actual_chunks = len(boundaries) - 1
    if actual_chunks <= 0:
        logger.warning(f"No valid chunks determined for '{filename}'. No files will be created.")
        return []

    _log(f"Determined {actual_chunks} actual chunks based on boundaries.")

    chunk_filenames = []
    base_filename = os.path.basename(filename)

    try:
        with open(filename, 'rb') as infile:
            for i in range(actual_chunks):
                start_pos = boundaries[i]
                end_pos = boundaries[i+1]
                chunk_size = end_pos - start_pos

                if chunk_size <= 0:
                    _log(f"Skipping empty chunk {i+1} (boundaries: {start_pos}-{end_pos}).")
                    continue

                # Construct output filename
                chunk_output_filename = os.path.join(output_dir, f"{base_filename}.part{i+1}")
                chunk_filenames.append(chunk_output_filename)
                _log(f"Writing chunk {i+1}/{actual_chunks} ({chunk_size:,} bytes) to '{chunk_output_filename}'")

                # Read the chunk and write to the new file
                infile.seek(start_pos)
                # Read in smaller blocks to avoid large memory usage for huge chunks
                buffer_size = 10 * 1024 * 1024 # 10MB buffer
                bytes_written = 0
                with open(chunk_output_filename, 'wb') as outfile:
                    while bytes_written < chunk_size:
                        bytes_to_read = min(buffer_size, chunk_size - bytes_written)
                        chunk_data = infile.read(bytes_to_read)
                        if not chunk_data:
                            break # Should not happen if boundaries are correct, but safety check
                        outfile.write(chunk_data)
                        bytes_written += len(chunk_data)

    except FileNotFoundError:
        logger.error(f"Error: Input file not found during chunking: {filename}")
        raise
    except Exception as e:
        logger.exception(f"Error during chunking process: {e}")
        # Clean up potentially partially written files? Maybe not, user might want them.
        raise

    _log(f"Finished chunking. Created {len(chunk_filenames)} files in '{output_dir}'.")
    return chunk_filenames

if __name__ == "__main__":
    filename = "example.txt"
    num_chunks = 14
    record_begin = "<SUBBEGIN>"
    record_end = "<SUBEND>"

    if not os.path.exists(filename):
        logger.error(f"Error: The file {filename} does not exist.")
    else:
        # Test chunk_preview (formerly find_boundaries)
        logger.info("--- Testing chunk_preview ---")
        boundaries = chunk_preview(filename, num_chunks, record_begin, record_end)
        logger.info(f"Previewed boundaries: {boundaries}")

        # Test chunk_it
        logger.info("\n--- Testing chunk_it ---")
        output_chunk_dir = "temp_file_chunks"
        if os.path.exists(output_chunk_dir):
             shutil.rmtree(output_chunk_dir) # Clean up previous test run
        logger.info(f"Creating chunks in directory: '{output_chunk_dir}'")
        try:
            created_files = chunk_it(filename, num_chunks, record_begin, record_end, output_dir=output_chunk_dir)
            if created_files:
                logger.info(f"Successfully created {len(created_files)} chunk files:")
            else:
                 logger.warning("chunk_it did not create any files.")
        except Exception as e:
            logger.error(f"chunk_it failed: {e}")