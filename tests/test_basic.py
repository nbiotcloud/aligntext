"""Basic Testing."""

import aligntext


def test_align():
    """Simple Testing."""
    text = aligntext.align([["a", "bb", "ccc"], ["zzz", "yyyy", "x"]], rtrim=False)
    assert str(text) == "a   bb   ccc\nzzz yyyy x  "
