#!/usr/bin/env bash
set -euo pipefail

openclaw agents list --json >/dev/null
openclaw agent --agent planner --message "ECC smoke test: ping" --json >/dev/null

echo "OK: OpenClaw CLI reachable"
