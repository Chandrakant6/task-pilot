# 🧭 TaskPilot

**TaskPilot** is a minimal, modular, and checkpoint-based task automation framework built with **Python** and **Bash**, primarily for **Linux** systems. It helps automate workflows, resume from checkpoints, and log every step — perfect for ML pipelines, automation scripts, or data workflows. Cross-platform support will be added in the future.

---

## ⚙️ Features

* Modular task structure (`modules/`)
* Hybrid Python + Bash execution
* Checkpoint-based resume system
* Transparent logs for debugging
* Config-driven workflows (`config.yaml`)

---

## 🚀 Usage

```bash
git clone https://github.com/yourusername/TaskPilot.git
cd TaskPilot
chmod +x taskpilot.sh
./taskpilot.sh         # Start workflow
./taskpilot.sh --resume  # Resume from checkpoint
```

---

## 🧩 Structure

```
TaskPilot/
├── taskpilot.sh        # Entry script
├── main.py             # Core logic
├── modules/            # Task modules
├── checkpoints/        # State tracking
├── logs/               # Run logs
└── config.yaml         # Workflow config
```

---

## 🧠 Example Config

```yaml
workflow:
  - preprocessing
  - training
  - evaluation
venv_path: ".venv"
logging: true
```

---

## 📜 License

MIT © 2025 Chandrakant Turkar
