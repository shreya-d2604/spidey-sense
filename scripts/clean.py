#!/usr/bin/env python3
"""Normalize scraped issue data: dedupe labels, drop scraper metadata, re-indent."""
import json
import sys

path = sys.argv[1]
with open(path) as f:
    issues = json.load(f)

for issue in issues:
    issue.pop("input", None)
    if "labels" in issue:
        issue["labels"] = list(dict.fromkeys(issue["labels"]))

with open(path, "w") as f:
    json.dump(issues, f, indent=2)
    f.write("\n")
