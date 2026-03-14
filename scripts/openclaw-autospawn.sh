#!/usr/bin/env bash
set -euo pipefail

python3 integrations/openclaw/openclaw_autospawn.py --config integrations/openclaw/autospawn.json "$@"
