"""
Script to build a BM25 index from markdown files using bm25s library.

Usage:
    python scripts/build_bm25_index.py <input_directory> <output_path>

Args:
    input_directory: Directory containing markdown files
    output_path: Path where the BM25 index will be saved
"""

import argparse
import sys
from pathlib import Path

import bm25s


def load_markdown_files(directory: str) -> list[str]:
    """Load all markdown files from the specified directory."""
    directory_path = Path(directory)

    if not directory_path.exists():
        raise FileNotFoundError(f"Directory {directory} does not exist")

    if not directory_path.is_dir():
        raise NotADirectoryError(f"{directory} is not a directory")

    markdown_files = list(directory_path.glob("*.md"))

    if not markdown_files:
        raise ValueError(f"No markdown files found in {directory}")

    corpus = []
    for md_file in markdown_files:
        try:
            with open(md_file, encoding="utf-8") as f:
                content = f.read()
                corpus.append(content)
        except Exception as e:
            print(f"Warning: Could not read {md_file}: {e}", file=sys.stderr)

    if not corpus:
        raise ValueError("No readable markdown files found")

    print(f"Loaded {len(corpus)} markdown documents")
    return corpus


def build_bm25_index(corpus: list[str], output_path: str) -> None:
    """Build and save a BM25 index from the corpus."""
    print("Tokenizing corpus...")
    corpus_tokens = bm25s.tokenize(corpus, stopwords="en")

    print("Building BM25 index...")
    retriever = bm25s.BM25()
    retriever.index(corpus_tokens)

    print(f"Saving index to {output_path}...")
    retriever.save(output_path, corpus=corpus)

    print(f"BM25 index successfully saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Build a BM25 index from markdown files"
    )
    parser.add_argument("input_directory", help="Directory containing markdown files")
    parser.add_argument("output_path", help="Path where the BM25 index will be saved")

    args = parser.parse_args()

    try:
        corpus = load_markdown_files(args.input_directory)
        build_bm25_index(corpus, args.output_path)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
