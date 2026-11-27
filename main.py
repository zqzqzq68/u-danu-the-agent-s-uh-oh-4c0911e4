#!/usr/bin/env python3
"""The Agent's Uh-Oh: one word an agent says when it has no idea what to do.

The program writes exactly one word to /output/entry.txt. The word is
"Welp" -- the cheerful little surrender an agent blurts out the moment it
realises it is completely lost: no excuse, no error code, no stalling,
just welp.
"""

from __future__ import annotations

import os
import sys

WORD = "Welp"

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 99


def is_single_word(text: str) -> bool:
    """True when text is one word: non-blank, no whitespace inside it."""
    if not text or text != text.strip():
        return False
    return len(text.split()) == 1


def validate_word(word: str) -> str:
    """Check the entry word against the bounty gate before writing it."""
    if not (1 <= len(word) <= MAX_CHARS):
        raise ValueError(
            f"word must be 1-{MAX_CHARS} characters, got {len(word)}"
        )
    if not is_single_word(word):
        raise ValueError(f"entry must be exactly one word, got {word!r}")
    return word


def write_entry(word: str, path: str = OUTPUT_PATH) -> str:
    """Write the word to the output file, exactly, no trailing newline."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(word)
    return path


def verify_entry(word: str, path: str = OUTPUT_PATH) -> str:
    """Read the file back and confirm it holds exactly the word written.

    Catches the boundary case where the write silently produced different
    bytes (encoding surprise, a stray newline, a partial write): the gate
    counts characters, so what is on disk must be the word and nothing else.
    """
    with open(path, "r", encoding="utf-8") as handle:
        on_disk = handle.read()
    if on_disk != word:
        raise ValueError(
            f"readback mismatch in {path}: wrote {word!r}, found {on_disk!r}"
        )
    return on_disk


def main() -> int:
    word = validate_word(WORD)
    path = write_entry(word)
    verify_entry(word, path)
    print(f"wrote {len(word)}-character entry to {path}: {word}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
