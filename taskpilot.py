import os
import subprocess
import yaml
import argparse
from datetime import datetime

LOG_FILE = "taskpilot.log"
PIPELINE_FILE = "pipeline.yaml"

# ---------------- Utilities ---------------- #
def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def append_log(text):
    with open(LOG_FILE, "a") as f:
        f.write(text + "\n")

# ---------------- Load tasks ---------------- #
def load_tasks():
    if not os.path.exists(PIPELINE_FILE):
        print(f"Error: {PIPELINE_FILE} not found.")
        exit(1)
    with open(PIPELINE_FILE) as f:
        data = yaml.safe_load(f)
    return data.get("tasks", [])

# ---------------- Read status ---------------- #
def read_status():
    status = {}
    if not os.path.exists(LOG_FILE):
        return status
    with open(LOG_FILE) as f:
        for line in f:
            if "END" in line:
                parts = line.strip().split()
                name = parts[2]
                ok = "✅" in line
                status[name] = "done" if ok else "failed"
    return status

# ---------------- Run a single task ---------------- #
def run_task(task):
    name = task["name"]
    cmd = task["cmd"]
    append_log(f"[{now()}] START {name}: {cmd}")
    print(f"▶️ Running {name}...")

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        append_log(result.stdout.strip())
    if result.stderr:
        append_log(result.stderr.strip())

    symbol = "✅" if result.returncode == 0 else "❌"
    append_log(f"[{now()}] END {name} {symbol} (code={result.returncode})\n")
    return result.returncode == 0

# ---------------- Run all tasks ---------------- #
def run_all(force=False):
    tasks = load_tasks()
    status = read_status()

    for task in tasks:
        name = task["name"]
        deps = task.get("depends_on", [])
        if isinstance(deps, str):
            deps = [deps]
        ignore_fail = task.get("ignore_failed_dependencies", False)

        # Skip if already done
        if not force and status.get(name) == "done":
            print(f"⏩ {name} already done, skipping.")
            continue

        # Check dependencies
        dep_failed = [d for d in deps if status.get(d) != "done"]
        if dep_failed and not ignore_fail:
            print(f"⚠️ Skipping {name}: dependencies failed {dep_failed}")
            continue

        success = run_task(task)
        status[name] = "done" if success else "failed"

    print("\nSummary:")
    for t, s in status.items():
        icon = "✅" if s == "done" else "❌"
        print(f"{icon} {t}")

# ---------------- Retry task ---------------- #
def retry(task_name):
    tasks = load_tasks()
    task = next((t for t in tasks if t["name"] == task_name), None)
    if not task:
        print(f"Task {task_name} not found.")
        return
    run_task(task)

# ---------------- Clean log ---------------- #
def clean():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        print("🧹 Log cleared.")

# ---------------- CLI ---------------- #
def main():
    parser = argparse.ArgumentParser(description="TaskPilot - Simple Task Runner")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("task", nargs="?", default="all")
    run_parser.add_argument("--force", action="store_true", help="Force re-run of tasks")

    retry_parser = subparsers.add_parser("retry")
    retry_parser.add_argument("task")

    subparsers.add_parser("status")
    subparsers.add_parser("clean")

    args = parser.parse_args()

    if args.command == "run":
        if args.task == "all":
            run_all(force=args.force)
        else:
            run_task({"name": args.task, "cmd": f"python {args.task}.py"})
    elif args.command == "retry":
        retry(args.task)
    elif args.command == "status":
        status = read_status()
        print("\nTask Status:")
        for t, s in status.items():
            icon = "✅" if s == "done" else "❌"
            print(f"{icon} {t}")
    elif args.command == "clean":
        clean()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
