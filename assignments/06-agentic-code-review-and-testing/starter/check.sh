#!/usr/bin/env sh
# Run every guardrail. Exits non-zero on the first failure (same as CI).
set -e
cd "$(dirname "$0")"
echo "== ruff (lint)";   ruff check .
echo "== black (format)"; black --check .
echo "== pytest";        pytest
echo "All guardrails passed."
