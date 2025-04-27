from __future__ import annotations

from polars_subclasses import __version__


def test_main() -> None:
    assert isinstance(__version__, str)
