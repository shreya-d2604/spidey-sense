#!/usr/bin/env python3
"""Re-indent a JSON file in place for readability."""
import json
import sys

path = sys.argv[1]
with open(path) as f:
    data = json.load(f)
with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
