#!/usr/bin/env python3
"""Find Unicode control and format characters without printing the characters."""

import argparse
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ALLOWED_CONTROLS = {"\t", "\r", "\n"}


def inspect(path):
    counts = Counter()
    locations = {}

    with path.open(encoding="utf-8-sig", errors="strict", newline="") as source:
        for line_number, line in enumerate(source, 1):
            for column, character in enumerate(line, 1):
                category = unicodedata.category(character)
                if character in ALLOWED_CONTROLS:
                    continue
                if category not in {"Cc", "Cf", "Cs"}:
                    continue

                counts[ord(character)] += 1
                positions = locations.setdefault(ord(character), [])
                if len(positions) < 5:
                    positions.append(f"{line_number}:{column}")

    return counts, locations


def main():
    parser = argparse.ArgumentParser(
        description="Report Unicode control and format characters without showing file contents."
    )
    parser.add_argument("files", nargs="+", type=Path, help="UTF-8 text files to inspect")
    args = parser.parse_args()
    findings = False
    read_failed = False

    for path in args.files:
        try:
            counts, locations = inspect(path)
        except (OSError, UnicodeError) as error:
            print(f"invis-scan: {path}: cannot read UTF-8 text: {error}", file=sys.stderr)
            read_failed = True
            continue

        if not counts:
            print(f"{path}: no control or format characters found")
            continue

        findings = True
        print(f"{path}:")
        for codepoint in sorted(counts):
            character = chr(codepoint)
            name = unicodedata.name(character, "UNNAMED")
            category = unicodedata.category(character)
            first = ", ".join(locations[codepoint])
            more = " ..." if counts[codepoint] > len(locations[codepoint]) else ""
            print(
                f"  U+{codepoint:04X} {name} category={category} "
                f"count={counts[codepoint]} first={first}{more}"
            )

    if read_failed:
        return 2
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
