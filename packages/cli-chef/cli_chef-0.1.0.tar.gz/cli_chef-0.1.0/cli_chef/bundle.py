# bundle.py
import click
import sys
from pathlib import Path
from typing import Tuple # Import Tuple for type hinting

# Default constants (used in decorators)
DEFAULT_OUTPUT_FILENAME = "bundle.txt"
DEFAULT_EXTENSIONS = ('.py',) # Tuple for default

def bundle_files(input_dir_path: str, output_filepath: str, extensions_to_bundle: Tuple[str, ...]):
    """
    Finds all files with the specified extensions recursively within the input directory,
    concatenates their content into the output file, prepending each file's
    content with a comment indicating its relative path.

    Args:
        input_dir_path: The resolved absolute path to the directory to scan.
        output_filepath: The path to the file where the bundled content will be written.
        extensions_to_bundle: A tuple of file extensions (e.g., ('.py', '.txt')) to bundle.
    """
    # Convert input_dir_path string back to Path object for processing
    input_dir = Path(input_dir_path)

    click.echo(f"Starting bundling process...")
    click.echo(f"Input directory: '{input_dir_path}'") # Show the path click resolved
    click.echo(f"Output file: '{output_filepath}'")
    click.echo(f"File extensions to bundle: {extensions_to_bundle}")

    # --- Input Validation (Existence and Directory check is done by click.Path) ---
    # Click's type=click.Path(exists=True, file_okay=False) handles these checks.

    # --- File Discovery and Bundling ---
    files_bundled_count = 0
    all_files_to_process = set() # Use a set to avoid duplicates if patterns overlap

    try:
        # Iterate through each requested extension and find matching files
        for ext in extensions_to_bundle:
            # Ensure the extension starts with a dot for consistency
            normalized_ext = ext if ext.startswith('.') else f".{ext}"
            click.echo(f"Searching for files ending with '{normalized_ext}'...")
            # Use rglob for recursive search
            # Path.rglob is generally case-sensitive on POSIX and case-insensitive on Windows
            found_files = input_dir.rglob(f"*{normalized_ext}")
            all_files_to_process.update(found_files)

        # Sort the collected files for deterministic output order
        sorted_files_to_process = sorted(list(all_files_to_process))
        click.echo(f"Found {len(sorted_files_to_process)} potential files matching specified extensions.")

        # Open the output file for writing.
        with open(output_filepath, "w", encoding="utf-8") as outfile:
            click.echo(f"Opened '{output_filepath}' for writing.")

            for file_path in sorted_files_to_process:
                # Ensure we are only processing files, not directories
                if not file_path.is_file():
                    continue

                try:
                    # Calculate the relative path for the header comment
                    relative_path = file_path.relative_to(input_dir)
                    header = f"# {relative_path.as_posix()}\n" # Use '/' separator

                    click.echo(f"  Bundling: {relative_path.as_posix()}")

                    # Write the header
                    outfile.write(header)

                    # Read and write the file content
                    with open(file_path, "r", encoding="utf-8", errors='replace') as infile:
                        # Using errors='replace' for robustness against potential decoding errors
                        content = infile.read()
                        outfile.write(content)

                    # Add separation between files
                    outfile.write("\n\n")
                    files_bundled_count += 1

                except (IOError, OSError) as e:
                    click.echo(f"  Warning: Could not read file '{file_path}'. Error: {e}. Skipping.", err=True)
                except UnicodeDecodeError as e: # Less likely with errors='replace' but kept for clarity
                    click.echo(f"  Warning: Could not decode file '{file_path}' as UTF-8. Error: {e}. Skipping.", err=True)
                except Exception as e:  # Catch unexpected errors during file processing
                    click.echo(f"  Warning: An unexpected error occurred processing file '{file_path}'. Error: {e}. Skipping.", err=True)


    except (IOError, OSError) as e:
        click.echo(f"\nError: Could not write to output file '{output_filepath}'. Error: {e}", err=True)
        sys.exit(1)
    except PermissionError as e:
        click.echo(f"\nError: Permission denied. Check read/write permissions. Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:  # Catch unexpected errors during setup or file walking
        click.echo(f"\nAn unexpected error occurred: {e}", err=True)
        sys.exit(1)

    click.echo(f"\nFinished bundling.")
    click.echo(f"Total files bundled: {files_bundled_count}")
    click.echo(f"Output written to: '{output_filepath}'")


@click.command()
@click.argument(
    "input_dir",
    default=".",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True, resolve_path=True),
)
@click.option(
    "-o", "--output",
    default=DEFAULT_OUTPUT_FILENAME,
    type=click.Path(dir_okay=False, writable=True, resolve_path=True), # Ensure we can write to the output path
    help=f"Output file path. Defaults to '{DEFAULT_OUTPUT_FILENAME}' in the current directory."
)
@click.option(
    "-e", "--extension",
    multiple=True, # Allows specifying the option multiple times
    default=DEFAULT_EXTENSIONS,
    help=f"File extension(s) to include (e.g., '.py', 'txt'). Can be used multiple times. Defaults to {DEFAULT_EXTENSIONS}."
)
def main(input_dir: str, output: str, extension: Tuple[str, ...]):
    """
    Bundles files with specified extensions recursively into a single output file.

    This tool scans the SOURCE_DIRECTORY for files matching the given EXTENSIONs
    (defaulting to '.py') and concatenates their content into the OUTPUT file
    (defaulting to 'bundle.txt'). Each bundled file's content is preceded by a
    comment indicating its original relative path.

    Arguments:
      SOURCE_DIRECTORY: Path to the directory to scan for files.
                        If omitted, defaults to the current working directory ('.').
    """
    try:
        # Pass the validated and resolved paths, and the tuple of extensions
        bundle_files(input_dir, output, extension)
    except (FileNotFoundError, NotADirectoryError, IOError, PermissionError) as e:
        # Some errors might still occur within bundle_files despite click's checks
        click.echo(f"\nBundling failed. Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"\nAn unexpected critical error occurred: {e}", err=True)
        sys.exit(1)


# --- Script Entry Point ---
if __name__ == "__main__":
    main()
