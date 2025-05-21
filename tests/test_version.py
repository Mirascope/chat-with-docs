"""Test version import."""

from chat_with_docs import __version__


def test_version() -> None:
    """Test that version is a string."""
    assert isinstance(__version__, str)
