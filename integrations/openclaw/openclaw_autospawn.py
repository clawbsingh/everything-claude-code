import argparse
import json
import subprocess
import sys
import time


def run(cmd):
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def main():
    parser = argparse.ArgumentParser(description="Auto-spawn OpenClaw agents from config")
    parser.add_argument("--config", required=True, help="Path to autospawn JSON config")
    parser.add_argument("--dry-run", action="store_true", help="Print commands only")
    parser.add_argument("--attempts", type=int, default=1)
    parser.add_argument("--backoff", type=int, default=5)
    args = parser.parse_args()

    with open(args.config, "r") as f:
        cfg = json.load(f)

    session_id = cfg.get("session_id")
    deliver = cfg.get("deliver", False)
    tasks = cfg.get("tasks", [])

    if not tasks:
        print("No tasks found in config")
        return 1

    for i, task in enumerate(tasks, start=1):
        agent = task.get("agent")
        message = task.get("message")
        thinking = task.get("thinking")
        timeout = task.get("timeout")

        if not agent or not message:
            print(f"Task {i} missing agent/message")
            return 1

        cmd = ["openclaw", "agent", "--agent", agent, "--message", message]
        if session_id:
            cmd += ["--session-id", session_id]
        if deliver:
            cmd += ["--deliver"]
        if thinking:
            cmd += ["--thinking", thinking]
        if timeout:
            cmd += ["--timeout", str(timeout)]

        if args.dry_run:
            print("DRY RUN:", " ".join(cmd))
            continue

        attempt = 0
        while attempt < args.attempts:
            attempt += 1
            code, out, err = run(cmd)
            if code == 0:
                print(out)
                break
            if attempt >= args.attempts:
                print(err, file=sys.stderr)
                return code
            time.sleep(args.backoff)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
