#!/usr/bin/env python3
"""Validate scraped issue data. Exit non-zero if any target fails."""
import json
import sys
from pathlib import Path


def validate_file(path: Path) -> list[str]:
    """Return a list of error messages for this file (empty = valid)."""
    try:
        text = path.read_text()
    except FileNotFoundError:
        return [f"file not found: {path}"]

    try:
        issues = json.loads(text)
    except json.JSONDecodeError as e:
        return [f"invalid JSON: {e}"]

    if not isinstance(issues, list) or len(issues) == 0:
        return ["expected a non-empty array of issues"]

    errors = []
    for i, issue in enumerate(issues):
        if not issue.get("title"):
            errors.append(f"issue {i}: missing title")
        if not issue.get("url"):
            errors.append(f"issue {i}: missing url")
        if not issue.get("labels"):
            errors.append(f"issue {i}: missing labels")
    return errors


def main():
    if len(sys.argv) > 1:
        paths = [Path(sys.argv[1])]
    else:
        paths = sorted(Path("data").glob("*.json"))

    failed = False
    for path in paths:
        errors = validate_file(path)
        if errors:
            failed = True
            print(f"{path}: FAILED")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"{path}: OK")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
