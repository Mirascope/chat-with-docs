"""Main entry point for the chat-with-docs application."""

import functools

import bm25s
import lilypad
from dotenv import load_dotenv
from mirascope import llm, prompt_template
from mirascope.core.base import BaseDynamicConfig
from rich.console import Console

load_dotenv()
lilypad.configure(auto_llm=True)

console = Console()

EXAMPLE_MIRASCOPE_PROGRAM = """from mirascope import llm, prompt_template
from pydantic import BaseModel


class Book(BaseModel):
    \"\"\"An extracted book.\"\"\"
 
    title: str
    author: str


@llm.call(
    provider="openai", 
    model="gpt-4o-mini", 
    response_model=Book
) 
@prompt_template("Extract {text}")
def extract_book(text: str): ...


book: Book = extract_book("The Name of the Wind by Patrick Rothfuss")
print(book)
# Output: title='The Name of the Wind' author='Patrick Rothfuss'"""

PROMPT_TEMPLATE = """
SYSTEM: You are a helpful assistant that can answer questions about the Mirascope library. Below is an example of a basic
mirascope program:

```python
{example_mirascope_program}
```

Below is some relevant documentation for the library for you to use:

---
{docs_rendered}
---

You should answer the user's question about mirascope, using everything you know about the library.

USER: {user_message}
"""


@lilypad.trace(versioning="automatic")
@llm.call(
    provider="openai",
    model="gpt-4o",
)
@prompt_template(PROMPT_TEMPLATE)
def bot_response_with_docs(
    user_message: str, docs: list[str] | None = None
) -> BaseDynamicConfig:
    docs = docs or []
    docs_rendered = "---\n".join(docs)
    return {
        "computed_fields": {
            "example_mirascope_program": EXAMPLE_MIRASCOPE_PROGRAM,
            "docs_rendered": docs_rendered,
        }
    }


@functools.lru_cache(maxsize=1)
def load_index() -> bm25s.BM25:
    return bm25s.BM25.load("mirascope_index", load_corpus=True)


@lilypad.trace(versioning="automatic")
def get_docs(user_message: str, k: int = 3) -> list[str]:
    index = load_index()
    query_tokens = bm25s.tokenize(user_message)
    results, _ = index.retrieve(query_tokens, k=k)
    docs = [x["text"] for x in results[0].tolist()]
    return docs


@lilypad.trace(versioning="automatic")
async def bot_response(user_message: str) -> str:
    docs = get_docs(user_message)
    return bot_response_with_docs(user_message, docs).content


def main() -> None:
    """Run the chat-with-docs application."""
    console.print("[bold green]Welcome to Chat with Docs![/bold green]")
    console.print("Type 'quit' to exit the chat.\n")

    while True:
        user_input = input("Enter your message: ")

        if user_input.lower() == "quit":
            console.print("[bold red]Goodbye![/bold red]")
            break

        console.print(f"[blue]User:[/blue] {user_input}")

        bot_reply = bot_response(user_input)
        console.print(f"[green]Bot:[/green] {bot_reply}")
        console.print()


if __name__ == "__main__":
    main()
