# TaskPilot MVP

Dead-simple task runner for automation workflows — one YAML, one log, zero headaches.

## 🚀 Overview

TaskPilot is a lightweight, file-based automation tool for solo developers and small teams.
It helps you:

Run sequences of commands/tasks

Respect optional dependencies between tasks

Keep logs and checkpoints in a single file

Resume tasks after failures

Avoid messy Bash scripts

Philosophy: Keep It Simple, Stupid (KISS) — minimal structure, maximum clarity.

## 📂 Project Structure
~~~
taskpilot_test/
│
├─ pipeline.yaml        # Define your tasks
├─ taskpilot.py         # TaskPilot executor
├─ setup_env.sh         # Mock bash task
├─ preprocess.py        # Mock Python task
├─ train.py             # Mock Python task
└─ evaluate.py          # Mock Python task
~~~
---

## ⚙️ pipeline.yaml Example
~~~ yaml
tasks:
  - name: setup_env
    cmd: bash setup_env.sh

  - name: preprocess
    cmd: python preprocess.py

  - name: train
    cmd: python train.py
    depends_on:
      - preprocess
      - setup_env

  - name: evaluate
    cmd: python evaluate.py
    depends_on:
      - train
    ignore_failed_dependencies: true
~~~

Notes:

`depends_on` → optional, can be a string or a list

`ignore_failed_dependencies`: true → task runs even if dependencies failed
---

## 💻 Usage
Run all tasks
~~~
python taskpilot.py run all
~~~

Run a single task
~~~
python taskpilot.py run <task_name>
~~~

Retry a task
~~~
python taskpilot.py retry <task_name>
~~~

Force re-run all tasks
~~~
python taskpilot.py run all --force
~~~

Show task status
~~~
python taskpilot.py status
~~~

Clear logs/checkpoints
~~~
python taskpilot.py clean
~~~
---
## 📋 Logs & Checkpoints

All logs and checkpoints are stored in taskpilot.log

Tracks: start time, end time, stdout, stderr, success/failure ✅❌

One file to rule them all — no extra folders
---

## 💡 Design Rationale

Minimal YAML + single log keeps workflow clear and maintainable

Dependencies are optional, not strict — sequence is mostly top-to-bottom

`ignore_failed_dependencies` gives flexibility for non-critical tasks

Pure Python, no extra dependencies
---

## 👍 Key Benefits

No over-engineered DAGs

Easy to add or modify tasks

Reproducible runs

Ideal for small scripts, ML experiments, automation workflows
