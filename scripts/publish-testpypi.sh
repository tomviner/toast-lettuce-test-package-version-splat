#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
cd "$REPO_ROOT"

TOKEN_FILE=${TEST_PYPI_TOKEN_FILE:-token.test-pypi}
PUBLISH_URL=${TEST_PYPI_PUBLISH_URL:-https://test.pypi.org/legacy/}
CHECK_URL=${TEST_PYPI_CHECK_URL:-https://test.pypi.org/simple/}
KEEP_LAST_VERSION=${KEEP_LAST_VERSION:-0}

if [ ! -f "$TOKEN_FILE" ]; then
  echo "Missing token file: $TOKEN_FILE" >&2
  exit 1
fi

token=$(tr -d '\r\n' < "$TOKEN_FILE")
if [ -z "$token" ]; then
  echo "Token file is empty: $TOKEN_FILE" >&2
  exit 1
fi

original_version=$(uv version --short)
tmp_versions=$(mktemp)
cleanup() {
  rm -f "$tmp_versions"
  if [ "$KEEP_LAST_VERSION" != "1" ]; then
    uv version --frozen "$original_version" >/dev/null
  fi
}
trap cleanup EXIT INT TERM

uv run canonical-version-matrix > "$tmp_versions"
total=$(wc -l < "$tmp_versions" | tr -d ' ')
count=0

while IFS= read -r version; do
  count=$((count + 1))
  echo "[$count/$total] $version"
  uv version --frozen "$version"
  uv build --clear
  uv publish \
    --publish-url "$PUBLISH_URL" \
    --check-url "$CHECK_URL" \
    --token "$token" \
    --no-attestations \
    "$@"
done < "$tmp_versions"
