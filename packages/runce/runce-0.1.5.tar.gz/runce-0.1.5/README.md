# Runce

# 🚀 The One-and-Done Process Wrangler

> _"Runce and done! No repeats, no retreats!"_ 🏃‍♂️💨  
> 🔒 **Guaranteed Singleton Execution** • 📊 **Process Tracking** • ⏱️ **Lifecycle Management**

## Features ✨

- 🚫 **No Duplicates**: Each command runs exactly once per unique ID
- 📝 **Process Tracking**: View all managed processes with status
- ⏱️ **Execution Time**: Track how long processes have been running
- 📂 **Log Management**: Automatic stdout/stderr capture
- 🛑 **Clean Termination**: Proper process killing

## Installation 📦

```bash
pip install runce
```

## Usage 🛠️

```bash
# Run a singleton process
runce run --id my-process -- python script.py

# List all processes
runce list

# View output
runce tail my-process -n 20

# Stop a process
runce kill my-process

# Restart a process
runce restart my-process

# Clean dead processes
runce clean
```

## Examples 💡

### 1. Running a Background Service

```bash
runce run --id api-server -- python api.py
```

### 2. Checking Running Processes

```bash
$ runce list
PID     NAME        STATUS      ELAPSED    COMMAND
1234    api-server  ✅ Running  01:23:45   python api.py
5678    worker      ❌ Stopped  00:45:30   python worker.py
```

### 3. Preventing Duplicates

```bash
$ runce run --id daily-job -- python daily.py
🚀 Started: PID:5678(✅ Running) daily-job

$ runce run --id daily-job -- python daily.py
🚨 Already running: PID:5678(✅ Running) daily-job
```

## How It Works ⚙️

1. **Process Locking**: Each `--id` creates a lock file
2. **PID Tracking**: Running processes are tracked in JSON files
3. **Singleton Enforcement**: Duplicate execution prevented
4. **Cleanup**: Dead processes can be automatically cleaned

## Development 🏗️

```bash
# Install in development mode
pip install -e .

# Run tests
pytest

# Lint code
flake8 runce
```

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
