# TaskPilot (MVP)

TaskPilot is a minimal task-pipeline runner with resumability, logging, and language-agnostic task execution using Python modules.

This is a locked MVP, matching the exact implemented code — no extra features added.

## ✅ Features 

#### ✔ Run pipelines
`python taskpilot.py run <pipeline_name>`

#### ✔ Pipeline format
Placed in:
`pipelines/<name>.yaml`

A pipeline is a YAML list of steps(tasks):
~~~
- task: clean_data
  args:
    threshold: 10

- task: analyze
  args:
    factor: 3
~~~

#### ✔ Task format (Python-only in current MVP) 
Tasks live in:
`tasks/<task_name>.py`

Each task file must define a run() function:
`def run(input_data, threshold=5):
    ...
    return output`

#### ✔ Logging 
All logs go to:
`taskpilot.log`

Every step logs:
`starting task
completion
errors`

#### ✔ State / Checkpointing 
Saved to:
`.state/<pipeline>.json`

State file structure:
`{ "last_completed": 1 }` (`1` is the index of the `step` or `task` in the `pipeline`)

After a crash or interruption, TaskPilot automatically resumes from the next step.

#### ✔ Task input/output 
`input_data` is passed from one task to the next
only one input and one output is supported in MVP
output of task N becomes input of task N+1

## 📁 Project Structure
~~~
taskpilot.py
taskpilot.log
.state/
    example.json
tasks/
    clean_data.py
    analyze.py
pipelines/
    example.yaml
~~~

## 🧠 How It Works (Direct Mapping to Code)

#### 1. Load pipeline
`load_pipeline()` loads YAML.

#### 2. Load state
`load_state()` returns the last completed step index.

#### 3. Resume logic
~~~
if index <= last_done:
    continue
~~~

#### 4. Load task module
`load_task_module()` dynamically imports: `tasks/<task>.py`

#### 5. Execute task
`run_task()` calls: `mod.run(input_data, **args)`

#### 6. Save state
`save_state()` writes `JSON`.

## 📌 Limitations (Intentional for MVP)

Only Python tasks (.py) 
Each task must have a run() function 
Only single input + single output 
Pipelines cannot define env vars (not implemented) 
No argument parsing beyond run <pipeline> 
No listing pipelines or tasks 
No cross-language execution 
No platform abstractions

This README reflects the exact implementation as-is.

## 📦 Usage
~~~
Run a pipeline:
python taskpilot.py run example
~~~

Example directory:
~~~
pipelines/example.yaml
tasks/clean_data.py
tasks/analyze.py
~~~

## 🔧 Requirements
~~~
Python 3.8+
PyYAML
~~~

Install with:
`pip install pyyaml`

## 🧘 MVP Philosophy
### The code matches these principles -
small functions 
no hidden magic  
readable 
minimal 
easy to reason about 
low surface area