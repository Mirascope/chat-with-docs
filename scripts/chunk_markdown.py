#!/usr/bin/env python3
"""Script to chunk markdown files by Content tags into individual page files."""

import argparse
import sys
from pathlib import Path

# Add the parent directory to Python path to import from chat_with_docs
sys.path.insert(0, str(Path(__file__).parent.parent))

from chat_with_docs.chunker import process_markdown_file


def main() -> None:
    """Main entry point for the chunking script."""
    parser = argparse.ArgumentParser(
        description="Chunk markdown file by Content tags into individual page files"
    )
    parser.add_argument("input_file", type=Path, help="Path to the input markdown file")
    parser.add_argument(
        "output_dir", type=Path, help="Directory to output individual page files"
    )

    args = parser.parse_args()

    try:
        process_markdown_file(args.input_file, args.output_dir)
        print("Chunking completed successfully!")
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        print(f"Permission error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
