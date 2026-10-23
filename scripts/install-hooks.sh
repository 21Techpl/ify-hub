#!/usr/bin/env bash
# Point git at the committed hooks (no per-developer hand-editing).
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit 2>/dev/null || true
echo "pre-commit enforcement enabled (.githooks/pre-commit)."
