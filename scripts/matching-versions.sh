#!/usr/bin/env sh
set -eu

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  echo "Usage: $0 '<specifier>' [list|minmax]" >&2
  exit 1
fi

SPECIFIER=$1
MODE=${2:-list}
PACKAGE_NAME=${PACKAGE_NAME:-toast-lettuce-test-package-version-splat}
INDEX_URL=${INDEX_URL:-https://test.pypi.org}

if [ "$MODE" != "list" ] && [ "$MODE" != "minmax" ]; then
  echo "Mode must be 'list' or 'minmax'" >&2
  exit 1
fi

export SPECIFIER MODE PACKAGE_NAME INDEX_URL

uv run --with packaging python -c '
import json
import os
import sys
import urllib.request
from packaging.specifiers import SpecifierSet
from packaging.version import Version

package_name = os.environ["PACKAGE_NAME"]
specifier = SpecifierSet(os.environ["SPECIFIER"])
mode = os.environ["MODE"]
index_url = os.environ["INDEX_URL"].rstrip("/")

with urllib.request.urlopen(f"{index_url}/pypi/{package_name}/json") as response:
    data = json.load(response)

versions = sorted(
    Version(version)
    for version in data["releases"]
    if specifier.contains(version, prereleases=True)
)

if not versions:
    print("<no matches>")
    sys.exit(0)

if mode == "minmax":
    print(f"min={versions[0]}")
    print(f"max={versions[-1]}")
else:
    print("\n".join(str(version) for version in versions))
'
