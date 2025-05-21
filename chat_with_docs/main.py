"""Main entry point for the chat-with-docs application."""

from rich.console import Console

console = Console()


def main() -> None:
    """Run the chat-with-docs application."""
    console.print("[bold green]Welcome to Chat with Docs![/bold green]")
    console.print("This application is currently under development.")


if __name__ == "__main__":
    main()
