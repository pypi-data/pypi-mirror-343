import pytest
import os
import shutil
import logging # Import logging
from pathlib import Path
from pyfilechunker.FileChunker import chunk_preview, chunk_it

# Configure logging for tests (optional, but helps control output)
# logging.basicConfig(level=logging.DEBUG) # Can be configured via pytest command line

# Define standard record markers used in tests
RECORD_BEGIN = "<SUBBEGIN>"
RECORD_END = "<SUBEND>"

@pytest.fixture
def sample_file_content():
    """Provides sample file content with multiple records."""
    lines = []
    for i in range(10):
        lines.append(f"{RECORD_BEGIN}\n")
        lines.append(f"Record {i+1} line 1\n")
        lines.append(f"Record {i+1} line 2\n")
        lines.append(f"{RECORD_END}\n")
    return "".join(lines)

@pytest.fixture
def create_test_file(tmp_path, sample_file_content):
    """Creates a temporary test file with sample content."""
    file_path = tmp_path / "test_input.txt"
    file_path.write_text(sample_file_content, encoding='utf-8')
    logging.debug(f"Created test file: {file_path} (size: {file_path.stat().st_size})")
    return file_path

@pytest.fixture
def create_empty_file(tmp_path):
    """Creates an empty temporary test file."""
    file_path = tmp_path / "empty_input.txt"
    file_path.touch()
    logging.debug(f"Created empty test file: {file_path}")
    return file_path

@pytest.fixture
def huabiao_file_path():
    """Provides the path to the large example file."""
    # Assuming the test runs from the project root or tests directory
    path = Path(__file__).parent / "example.txt"
    logging.debug(f"Checking for example.txt at: {path}")
    if not path.exists():
        logging.warning(f"Test file not found: {path}, skipping test.")
        pytest.skip(f"Test file not found: {path}")
    logging.debug(f"Found example.txt (size: {path.stat().st_size})")
    return path

@pytest.fixture
def create_incomplete_file(tmp_path, sample_file_content):
    """Creates a temporary test file with the last end tag missing."""
    # Remove the last occurrence of RECORD_END
    incomplete_content = sample_file_content.rsplit(RECORD_END, 1)[0]
    file_path = tmp_path / "incomplete_input.txt"
    file_path.write_text(incomplete_content, encoding='utf-8')
    logging.debug(f"Created incomplete test file: {file_path} (size: {file_path.stat().st_size})")
    return file_path


# --- Tests for chunk_preview ---

def test_chunk_preview_basic(create_test_file):
    """Test chunk_preview with a standard file and chunk count."""
    file_path = create_test_file
    num_chunks = 3
    file_size = file_path.stat().st_size
    logging.debug(f"Testing chunk_preview_basic: file='{file_path}', size={file_size}, num_chunks={num_chunks}")

    boundaries = chunk_preview(str(file_path), num_chunks, RECORD_BEGIN, RECORD_END)
    logging.debug(f"Boundaries found: {boundaries}")

    expected_num_boundaries = num_chunks + 1
    logging.debug(f"Asserting len(boundaries) == {expected_num_boundaries}")
    assert len(boundaries) == expected_num_boundaries
    logging.debug(f"Asserting boundaries[0] == 0")
    assert boundaries[0] == 0
    logging.debug(f"Asserting boundaries[-1] == {file_size}")
    assert boundaries[-1] == file_size
    logging.debug(f"Asserting boundaries are strictly increasing")
    assert all(boundaries[i] < boundaries[i+1] for i in range(len(boundaries)-1))

def test_chunk_preview_one_chunk(create_test_file):
    """Test chunk_preview when only one chunk is requested."""
    file_path = create_test_file
    num_chunks = 1
    file_size = file_path.stat().st_size
    logging.debug(f"Testing chunk_preview_one_chunk: file='{file_path}', size={file_size}, num_chunks={num_chunks}")

    boundaries = chunk_preview(str(file_path), num_chunks, RECORD_BEGIN, RECORD_END)
    logging.debug(f"Boundaries found: {boundaries}")

    expected_boundaries = [0, file_size]
    logging.debug(f"Asserting boundaries == {expected_boundaries}")
    assert boundaries == expected_boundaries

def test_chunk_preview_empty_file(create_empty_file):
    """Test chunk_preview with an empty input file."""
    file_path = create_empty_file
    num_chunks = 5
    file_size = file_path.stat().st_size
    logging.debug(f"Testing chunk_preview_empty_file: file='{file_path}', size={file_size}, num_chunks={num_chunks}")
    assert file_size == 0 # Pre-check

    boundaries = chunk_preview(str(file_path), num_chunks, RECORD_BEGIN, RECORD_END)
    logging.debug(f"Boundaries found: {boundaries}")

    expected_boundaries = [0, 0]
    logging.debug(f"Asserting boundaries == {expected_boundaries}")
    assert boundaries == expected_boundaries

def test_chunk_preview_more_chunks_than_records(create_test_file):
    """Test chunk_preview when more chunks are requested than records."""
    file_path = create_test_file
    num_chunks = 15 # More chunks than the 10 records
    file_size = file_path.stat().st_size
    logging.debug(f"Testing chunk_preview_more_chunks_than_records: file='{file_path}', size={file_size}, num_chunks={num_chunks}")

    boundaries = chunk_preview(str(file_path), num_chunks, RECORD_BEGIN, RECORD_END)
    logging.debug(f"Boundaries found: {boundaries}")

    expected_num_boundaries = num_chunks + 1
    logging.debug(f"Asserting len(boundaries) == {expected_num_boundaries}")
    assert len(boundaries) == expected_num_boundaries
    logging.debug(f"Asserting boundaries[0] == 0")
    assert boundaries[0] == 0
    logging.debug(f"Asserting boundaries[-1] == {file_size}")
    assert boundaries[-1] == file_size
    logging.debug(f"Asserting boundaries are non-decreasing")
    assert all(boundaries[i] <= boundaries[i+1] for i in range(len(boundaries)-1)) # Use <= as some chunks might be empty

# --- Tests for chunk_it ---

def test_chunk_it_basic(create_test_file, tmp_path, sample_file_content):
    """Test basic chunk_it functionality: creates correct number of files."""
    file_path = create_test_file
    output_dir = tmp_path / "output_chunks"
    num_chunks = 4
    original_size = file_path.stat().st_size
    logging.debug(f"Testing chunk_it_basic: file='{file_path}', size={original_size}, num_chunks={num_chunks}, output='{output_dir}'")

    created_files = chunk_it(
        filename=str(file_path),
        num_chunks=num_chunks,
        record_begin=RECORD_BEGIN,
        record_end=RECORD_END,
        output_dir=str(output_dir)
    )
    logging.debug(f"chunk_it created files: {created_files}")

    # chunk_preview might adjust the actual number of chunks based on boundaries
    boundaries = chunk_preview(str(file_path), num_chunks, RECORD_BEGIN, RECORD_END)
    expected_num_files = len(boundaries) - 1
    logging.debug(f"Expected number of files based on preview: {expected_num_files}")

    logging.debug(f"Asserting output directory exists: {output_dir}")
    assert output_dir.exists()
    logging.debug(f"Asserting len(created_files) == {expected_num_files}")
    assert len(created_files) == expected_num_files
    found_files = list(output_dir.glob("*.part*"))
    logging.debug(f"Asserting len(found_files) == {expected_num_files}")
    assert len(found_files) == expected_num_files

    # Verify total size and content concatenation
    total_size = 0
    concatenated_content = b""
    created_files.sort()
    for chunk_file_path_str in created_files:
         chunk_file_path = Path(chunk_file_path_str)
         logging.debug(f"Checking chunk file: {chunk_file_path}")
         assert chunk_file_path.exists()
         size = chunk_file_path.stat().st_size
         total_size += size
         if size > 0:
             concatenated_content += chunk_file_path.read_bytes()
    logging.debug(f"Total size of chunks: {total_size}")

    original_content = file_path.read_bytes()
    logging.debug(f"Asserting total_size ({total_size}) == original_size ({len(original_content)})")
    assert total_size == len(original_content)
    # Content check is intensive, maybe log lengths instead if it fails
    logging.debug(f"Asserting concatenated content length ({len(concatenated_content)}) == original content length ({len(original_content)})")
    assert concatenated_content == original_content


def test_chunk_it_empty_file(create_empty_file, tmp_path):
    """Test chunk_it with an empty input file."""
    file_path = create_empty_file
    output_dir = tmp_path / "output_empty"
    num_chunks = 3
    original_size = file_path.stat().st_size
    logging.debug(f"Testing chunk_it_empty_file: file='{file_path}', size={original_size}, num_chunks={num_chunks}, output='{output_dir}'")
    assert original_size == 0

    created_files = chunk_it(
        filename=str(file_path),
        num_chunks=num_chunks,
        record_begin=RECORD_BEGIN,
        record_end=RECORD_END,
        output_dir=str(output_dir)
    )
    logging.debug(f"chunk_it created files: {created_files}")

    logging.debug(f"Asserting output directory exists: {output_dir}")
    assert output_dir.exists() # Directory should still be created
    expected_num_files = 0
    logging.debug(f"Asserting len(created_files) == {expected_num_files}")
    assert len(created_files) == expected_num_files # No chunk files should be created
    found_files = list(output_dir.glob("*.part*"))
    logging.debug(f"Asserting len(found_files) == {expected_num_files}")
    assert len(found_files) == expected_num_files

def test_chunk_it_output_dir_creation(create_test_file, tmp_path):
    """Test that chunk_it creates the output directory if it doesn't exist."""
    file_path = create_test_file
    output_dir = tmp_path / "new_output_dir"
    num_chunks = 2
    original_size = file_path.stat().st_size
    logging.debug(f"Testing chunk_it_output_dir_creation: file='{file_path}', size={original_size}, num_chunks={num_chunks}, output='{output_dir}'")

    logging.debug(f"Asserting output directory does NOT exist initially: {output_dir}")
    assert not output_dir.exists() # Ensure dir doesn't exist initially

    created_files = chunk_it(
        filename=str(file_path),
        num_chunks=num_chunks,
        record_begin=RECORD_BEGIN,
        record_end=RECORD_END,
        output_dir=str(output_dir)
    )
    logging.debug(f"chunk_it created files: {created_files}")

    logging.debug(f"Asserting output directory exists: {output_dir}")
    assert output_dir.exists()
    found_files = list(output_dir.glob("*.part*"))
    logging.debug(f"Asserting number of created files > 0")
    assert len(found_files) > 0 # Check that files were actually created

def test_chunk_it_example_total_size(huabiao_file_path, tmp_path):
    """Test chunk_it with the large example file and verify total size."""
    file_path = huabiao_file_path
    output_dir = tmp_path / "output_huabiao"
    num_chunks = 14 # As used in the original example script
    original_size = file_path.stat().st_size
    logging.debug(f"Testing chunk_it_example_total_size: file='{file_path}', size={original_size}, num_chunks={num_chunks}, output='{output_dir}'")

    created_files = chunk_it(
        filename=str(file_path),
        num_chunks=num_chunks,
        record_begin=RECORD_BEGIN, # Assuming default markers for this file
        record_end=RECORD_END,
        output_dir=str(output_dir)
    )
    logging.debug(f"chunk_it created files: {created_files}")

    logging.debug(f"Asserting output directory exists: {output_dir}")
    assert output_dir.exists()
    logging.debug(f"Asserting number of created files > 0")
    assert len(created_files) > 0 # Should create some chunks
    found_files = list(output_dir.glob("*.part*"))
    logging.debug(f"Asserting len(found_files) == len(created_files) ({len(created_files)})")
    assert len(found_files) == len(created_files)

    # Verify total size
    total_size = 0
    for chunk_file_path_str in created_files:
         chunk_file_path = Path(chunk_file_path_str)
         logging.debug(f"Checking chunk file: {chunk_file_path}")
         assert chunk_file_path.exists()
         total_size += chunk_file_path.stat().st_size
    logging.debug(f"Total size of chunks: {total_size}")

    logging.debug(f"Asserting total_size ({total_size}) == original_size ({original_size})")
    assert total_size == original_size

def test_chunk_it_incomplete_file(create_incomplete_file, tmp_path):
    """Test chunk_it with a file missing the final end tag."""
    file_path = create_incomplete_file
    output_dir = tmp_path / "output_incomplete"
    num_chunks = 3
    original_size = file_path.stat().st_size
    logging.debug(f"Testing chunk_it_incomplete_file: file='{file_path}', size={original_size}, num_chunks={num_chunks}, output='{output_dir}'")

    created_files = chunk_it(
        filename=str(file_path),
        num_chunks=num_chunks,
        record_begin=RECORD_BEGIN,
        record_end=RECORD_END,
        output_dir=str(output_dir)
    )
    logging.debug(f"chunk_it created files: {created_files}")

    logging.debug(f"Asserting output directory exists: {output_dir}")
    assert output_dir.exists()
    logging.debug(f"Asserting number of created files > 0")
    assert len(created_files) > 0

    # Verify total size - the chunker should include the trailing incomplete part
    total_size = 0
    created_files.sort() # Ensure order if needed for content check later
    for chunk_file_path_str in created_files:
         chunk_file_path = Path(chunk_file_path_str)
         logging.debug(f"Checking chunk file: {chunk_file_path}")
         assert chunk_file_path.exists()
         total_size += chunk_file_path.stat().st_size
    logging.debug(f"Total size of chunks: {total_size}")

    logging.debug(f"Asserting total_size ({total_size}) == original_size ({original_size})")
    assert total_size == original_size

    # Optional: Verify content if feasible - might be complex depending on boundary logic
    # concatenated_content = b""
    # for chunk_file_path_str in created_files:
    #     concatenated_content += Path(chunk_file_path_str).read_bytes()
    # original_content = file_path.read_bytes()
    # logging.debug(f"Asserting concatenated content length ({len(concatenated_content)}) == original content length ({len(original_content)})")
    # assert concatenated_content == original_content

