# Command Executor

A powerful command-line tool that helps you execute multiple commands sequentially or in parallel, with beautiful output display.

## Features

- Support executing single or multiple commands
- Support sequential and parallel execution
- Support file/directory condition-based execution
- Support commands containing double quotes
- Support reading commands from text file
- Support error handling and recovery
- Beautiful command execution progress display
- Clear success/failure status display
- Detailed command output information

## Output Display Examples

### Sequential Execution
```
╭─────────────────╮
│ Start Commands  │
╰─────────────────╯
Executing commands sequentially... ━━━━━━━━━━━━━━━━━━━━━━━━━━━   0% -:--:--
Executing command: echo "Hello, World!"
╭─────────────── Success ────────────────╮
│ Command 'echo "Hello, World!"' Success │
│                                        │
│ Hello, World!                          │
│                                        │
╰────────────────────────────────────────╯
Executing commands sequentially... ━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
╭───────────────────────╮
│ All Commands Success  │
╰───────────────────────╯
```

### Parallel Execution
```
╭─────────────────╮
│ Start Commands  │
╰─────────────────╯
Executing commands in parallel...
╭──────────────── Success ─────────────────────╮
│ Command 'sleep 2 && echo "Command1 Done"'    │
│                                              │
│ Command1 Done                                │
│                                              │
╰──────────────────────────────────────────────╯
╭───────────── Success ────────────────╮
│ Command 'echo "Command2 Done"'       │
│                                      │
│ Command2 Done                        │
│                                      │
╰──────────────────────────────────────╯
```

### Error Handling
```
╭─────────────────╮
│ Start Commands  │
╰─────────────────╯
Executing commands sequentially... ━━━━━━━━━━━━━━━━━━━━━━━━━━━   0% -:--:--
Executing command: echo "Normal Command"
╭─────────────── Success ────────────────╮
│ Command 'echo "Normal Command"' Success│
│                                       │
│ Normal Command                        │
│                                       │
╰───────────────────────────────────────╯
╭─────────────── Failed ──────────────╮
│ Command 'nonexistent_command' Failed │
│                                      │
│ Error:                               │
│ Command 'nonexistent_command' not found│
╰──────────────────────────────────────╯
Stopping execution due to error (use --continue-on-error to continue)
╭────────────────────────────╮
│ Execution completed with errors │
╰────────────────────────────╯
```

### File Check
```
╭────────────────────────╮
│ Checking: test.txt     │
╰────────────────────────╯
File 'test.txt' meets conditions
╭─────────────────╮
│ Start Commands  │
╰─────────────────╯
Executing commands sequentially... ━━━━━━━━━━━━━━━━━━━━━━━━━━━   0% -:--:--
Executing command: cat test.txt
╭────────── Success ───────────╮
│ Command 'cat test.txt'       │
│                              │
│ File content                 │
│                              │
╰──────────────────────────────╯
```

## Installation

1. Ensure Python 3.7+ is installed
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Sequential Execution
```bash
python main.py execute "ls -l" "pwd" "echo hello"
```

### Parallel Execution
```bash
python main.py execute --parallel "sleep 2" "echo hello" "date"
```

### Commands with Double Quotes
```bash
# Use single quotes to wrap commands containing double quotes
python main.py execute 'echo "Hello, World!"'
python main.py execute 'python -c "print(\"Hello\")"'
```

### Error Handling
```bash
# By default, execution stops on error
python main.py execute "echo 'Normal Command'" "nonexistent_command" "echo 'Won't Execute'"

# Use --continue-on-error to continue execution
python main.py execute --continue-on-error "echo 'Normal Command'" "nonexistent_command" "echo 'Will Execute'"
```

### File/Directory Condition-Based Execution
```bash
# Check file condition
python main.py execute --check-file "test.txt" --check-minutes 5 'echo "File condition met"'

# Check directory condition
python main.py execute --check-dir "test_dir" --check-minutes 10 'echo "Directory condition met"'

# File check in parallel mode
python main.py execute --parallel --check-file "test.txt" --check-minutes 5 'echo "Command1"' 'echo "Command2"'

# Directory check in parallel mode
python main.py execute --parallel --check-dir "test_dir" --check-minutes 5 'echo "Command1"' 'echo "Command2"'
```

### Reading Commands from File
```bash
# Execute commands from file
python main.py execute --from-file commands.txt

# Execute commands from file in parallel
python main.py execute --from-file commands.txt --parallel

# Example commands.txt format:
# echo "Hello, World!"
# ls -l
# pwd
# date
```

## Command Line Arguments

- `--sequential/--parallel`: Choose sequential or parallel execution (default: sequential)
- `--check-file`: Specify file path to check
- `--check-dir`: Specify directory path to check
- `--check-minutes`: Specify time threshold in minutes (default: 5)
- `--from-file`: Specify path to file containing commands
- `--continue-on-error/--stop-on-error`: Whether to continue execution on error (default: stop)
- Commands: Support any number of commands

## Notes

- Each command must be wrapped in quotes
- Use single quotes for commands containing double quotes
- When reading from file, one command per line, empty lines are ignored
- In parallel mode, all commands start simultaneously
- In parallel mode, file/directory checks are performed before all commands
- `--check-file` and `--check-dir` cannot be used together
- Command failures show detailed error messages
- By default, execution stops on command failure
- Use `--continue-on-error` to continue execution after command failures 