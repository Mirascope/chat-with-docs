"""Markdown chunker for splitting documents by Content tags."""

import re
from pathlib import Path
from typing import NamedTuple


class Page(NamedTuple):
    """A page extracted from markdown content."""

    title: str
    content: str


def chunk_markdown_by_pages(markdown_content: str) -> list[Page]:
    """Chunk markdown content by Content tags.

    Args:
        markdown_content: The markdown content to chunk

    Returns:
        List of Page objects, each containing a title and content
    """
    # Pattern to match Content tags with title attribute and capture content until closing tag
    content_tag_pattern = r'<Content\s+title="([^"]+)"[^>]*>(.*?)</Content>'

    matches = re.findall(
        content_tag_pattern, markdown_content, re.DOTALL | re.IGNORECASE
    )

    pages = []
    for title, content in matches:
        # Clean up the content by removing leading/trailing whitespace
        cleaned_content = content.strip()
        pages.append(Page(title=title, content=cleaned_content))

    return pages


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing invalid characters.

    Args:
        filename: The filename to sanitize

    Returns:
        A sanitized filename safe for filesystem use
    """
    # Remove invalid characters and replace spaces with underscores
    sanitized = re.sub(r'[<>:"/\\|?*]', "", filename)
    sanitized = re.sub(r"\s+", "_", sanitized)
    return sanitized.strip("_")


def process_markdown_file(input_path: Path, output_dir: Path) -> None:
    """Process a markdown file and create individual page files.

    Args:
        input_path: Path to the input markdown file
        output_dir: Directory to output individual page files

    Raises:
        FileNotFoundError: If input file doesn't exist
        PermissionError: If unable to create output directory or files
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Read the markdown content
    markdown_content = input_path.read_text(encoding="utf-8")

    # Chunk the content
    pages = chunk_markdown_by_pages(markdown_content)

    # Write each page to a separate file
    for page in pages:
        filename = f"{sanitize_filename(page.title)}.md"
        output_path = output_dir / filename
        output_path.write_text(page.content, encoding="utf-8")
        print(f"Created: {output_path}")

    print(f"Processed {len(pages)} pages from {input_path}")
