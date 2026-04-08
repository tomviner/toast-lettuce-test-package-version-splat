#!/usr/bin/env sh
set -eu

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  echo "Usage: $0 '<specifier>' [--pre]" >&2
  exit 1
fi

SPECIFIER=$1
ALLOW_PRE=${2:-}
PACKAGE_NAME=${PACKAGE_NAME:-toast-lettuce-test-package-version-splat}
INDEX_URL=${INDEX_URL:-https://test.pypi.org/simple}

if [ -n "$ALLOW_PRE" ] && [ "$ALLOW_PRE" != "--pre" ]; then
  echo "Only supported optional flag is --pre" >&2
  exit 1
fi

resolve_one() {
  resolution=$1

  if [ -n "$ALLOW_PRE" ]; then
    output=$(uv pip install --dry-run --no-deps --resolution "$resolution" \
      --index-url "$INDEX_URL" --pre "${PACKAGE_NAME}${SPECIFIER}" 2>&1)
  else
    output=$(uv pip install --dry-run --no-deps --resolution "$resolution" \
      --index-url "$INDEX_URL" "${PACKAGE_NAME}${SPECIFIER}" 2>&1)
  fi

  version=$(printf '%s\n' "$output" | sed -n "s/^ + ${PACKAGE_NAME}==//p" | tail -n 1)
  if [ -z "$version" ]; then
    printf '%s\n' "$output" >&2
    exit 1
  fi

  printf '%s=%s\n' "$resolution" "$version"
}

resolve_one lowest
resolve_one highest
