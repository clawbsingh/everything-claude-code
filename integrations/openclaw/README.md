# OpenClaw Integration (Auto‑spawn Agents)

This integration lets **Everything Claude Code** trigger OpenClaw agents automatically from a simple JSON config. Use it to spin up planner/builder/reviewer agents for projects, batch tasks, and run repeatable workflows.

## Prereqs
- OpenClaw CLI installed and authenticated
- OpenClaw gateway running
- Agents configured in OpenClaw (`openclaw agents list`)

## Quick start
```bash
# from repo root
python3 integrations/openclaw/openclaw_autospawn.py \
  --config integrations/openclaw/autospawn.json
```

## Config
Edit `integrations/openclaw/autospawn.json`:
```json
{
  "session_id": "ops-canvas-auto",
  "deliver": false,
  "tasks": [
    {
      "agent": "planner",
      "message": "Define approach and steps for the new project"
    },
    {
      "agent": "builder",
      "message": "Implement the plan in the repo"
    },
    {
      "agent": "reviewer",
      "message": "Audit and suggest fixes"
    }
  ]
}
```

### Options
- `session_id` (string): a stable session id to keep a consistent thread
- `deliver` (bool): if `true`, send replies to the default channel (otherwise CLI output only)
- `tasks`: ordered list of `{ agent, message, thinking?, timeout? }`

## Usage patterns
- **Project kickoff**: run planner → builder → reviewer in sequence.
- **Batch runs**: use multiple tasks with different agents.
- **Daily ops**: wire to cron for scheduled runs.

## Smoke test
```bash
scripts/openclaw-smoke-test.sh
```

## Notes
- For cost control, avoid high thinking levels unless necessary.
- If you hit rate limits, retry after a short delay.
