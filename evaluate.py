#!/usr/bin/env python3
"""Evaluation script for processing query files."""

import argparse
import asyncio
from pathlib import Path

from pydantic import BaseModel

from chat_with_docs.main import bot_response


class Query(BaseModel):
    id: str
    content: str


def load_queries(queries_dir: str) -> list[Query]:
    """Load all markdown files from the queries directory into a JSON structure.

    Args:
        queries_dir: Path to directory containing markdown query files

    Returns:
        List of dictionaries with 'id' and 'content' keys
    """
    queries_path = Path(queries_dir)
    if not queries_path.exists():
        raise FileNotFoundError(f"Queries directory not found: {queries_dir}")

    queries = []

    for md_file in sorted(queries_path.glob("*.md")):
        # Extract ID from filename (e.g., "0.md" -> "0")
        query_id = md_file.stem

        # Read file content
        content = md_file.read_text(encoding="utf-8").strip()

        queries.append(Query(id=query_id, content=content))

    return queries


async def evaluate_queries(queries_dir: str) -> list[str]:
    """Load queries and process each one through bot_response.

    Args:
        queries_dir: Path to directory containing markdown query files
    """
    try:
        queries = load_queries(queries_dir)
        print(f"Loaded {len(queries)} queries from {queries_dir}")
        tasks = [bot_response(query.content) for query in queries]
        results = await asyncio.gather(*tasks)
        return results

    except Exception as e:
        print(f"Error during evaluation: {e}")
        raise


def main() -> None:
    """Main entry point for the evaluation script."""
    parser = argparse.ArgumentParser(description="Evaluate queries from markdown files")
    parser.add_argument("queries_dir", help="Directory containing markdown query files")

    args = parser.parse_args()
    asyncio.run(evaluate_queries(args.queries_dir))


if __name__ == "__main__":
    main()
