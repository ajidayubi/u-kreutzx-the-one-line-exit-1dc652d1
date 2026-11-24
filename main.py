#!/usr/bin/env python3
"""The One-Line Exit: write one funny one-line resignation letter.

The program holds a single fixed resignation line, checks it against the
bounty's gate (UTF-8 text, 1 to 140 characters, exactly one line, not only
white space), writes it to entry.txt in the output directory, and verifies
the file round-trips byte for byte.

Usage:
    python3 main.py

The output directory is $MAKEFUN_OUTPUT_DIR when set, else /output.
The program takes no input, makes no network calls, uses no randomness
and no clock, so every run writes the same bytes.
"""

import os
import sys

# The resignation letter, exactly one line. A lighthouse keeper hands in
# his notice: the ships ignore his light, the seagulls have taken over HR,
# and the fog has taken his parking space. Three grievances, each more
# absurd than the last, in the voice of a real letter someone could send.
LINE = (
    "I hereby resign as lighthouse keeper: the ships ignore my light, "
    "the seagulls now run HR, and the fog took my parking space."
)

MAX_CHARS = 140


def validate(line):
    """Check the line against the bounty's gate; return an error or None."""
    if not isinstance(line, str):
        return "line is not text"
    if not line.strip():
        return "line is only white space"
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        return "line is not valid UTF-8"
    if len(line) < 1 or len(line) > MAX_CHARS:
        return "line is %d characters, gate allows 1 to %d" % (
            len(line),
            MAX_CHARS,
        )
    if "\n" in line or "\r" in line:
        return "line spans more than one line"
    return None


def main():
    error = validate(LINE)
    if error is not None:
        print("invalid entry: %s" % error, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)
    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        print("entry.txt did not round-trip byte for byte", file=sys.stderr)
        return 1
    print(LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
