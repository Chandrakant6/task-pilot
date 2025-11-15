import os
import json
import yaml
import importlib.util
import sys

LOG_FILE = "taskpilot.log"
STATE_DIR = ".state"


def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(msg + "\n")
    print(msg)


def load_pipeline(path):
    with open(path) as f:
        return yaml.safe_load(f)


def load_state(path):
    if not os.path.exists(path):
        return -1
    with open(path) as f:
        return json.load(f).get("last_completed", -1)


def save_state(path, index):
    with open(path, "w") as f:
        json.dump({"last_completed": index}, f)


def load_task_module(task_name):
    path = f"tasks/{task_name}.py"
    spec = importlib.util.spec_from_file_location(task_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_task(mod, input_data, args):
    return mod.run(input_data, **args)


def run_pipeline(name):
    pipeline_path = f"pipelines/{name}.yaml"
    state_path = f"{STATE_DIR}/{name}.json"

    pipeline = load_pipeline(pipeline_path)
    last_done = load_state(state_path)

    input_data = None

    for index, step in enumerate(pipeline):
        if index <= last_done:
            continue

        task_name = step["task"]
        args = step.get("args", {})

        log(f"Running task {task_name}")

        mod = load_task_module(task_name)

        try:
            output = run_task(mod, input_data, args)
        except Exception as e:
            log(f"Error in task {task_name}: {e}")
            return

        input_data = output
        save_state(state_path, index)

        log(f"Completed task {task_name}")

    log("Pipeline completed.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python taskpilot.py run <pipeline>")
        sys.exit(1)

    cmd = sys.argv[1]
    name = sys.argv[2]

    if cmd == "run":
        run_pipeline(name)
