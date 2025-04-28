import typer
from typing_extensions import Annotated
from pathlib import Path
from .FileChunker import chunk_it # Import chunk_it function

app = typer.Typer()

@app.command()
def run_chunker(
    file_path: Annotated[Path, typer.Argument(help="The path to the file to chunk.", exists=True, file_okay=True, dir_okay=False, readable=True)],
    num_chunks: Annotated[int, typer.Option(help="The desired number of chunks.")] = 5, # Added num_chunks option
    record_begin: Annotated[str, typer.Option(help="String marking the beginning of a record.")] = "<SUBBEGIN>", # Added record_begin option
    record_end: Annotated[str, typer.Option(help="String marking the end of a record.")] = "<SUBEND>", # Added record_end option
    output_dir: Annotated[Path, typer.Option(help="The directory to save the chunks.", file_okay=False, dir_okay=True, writable=True)] = Path("."),
):
    """Splits a large file into smaller chunks based on record boundaries."""
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        # Call the chunk_it function with the provided arguments
        created_files = chunk_it(
            filename=str(file_path.resolve()),
            num_chunks=num_chunks,
            record_begin=record_begin,
            record_end=record_end,
            output_dir=str(output_dir.resolve())
        )
        if created_files:
            typer.echo(f"Successfully created {len(created_files)} chunk files in '{output_dir}'.")
        else:
            typer.echo(f"No chunk files were created for '{file_path.name}'. Check logs or input parameters.")
    except Exception as e:
        typer.echo(f"An error occurred during chunking: {e}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
