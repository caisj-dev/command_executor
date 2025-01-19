# Command Executor / 命令行执行工具

[English](#command-executor) | [中文](#命令行执行工具)

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

---

# 命令行执行工具

这是一个强大的命令行工具，可以帮助你按顺序或并行执行多条命令，并提供美观的输出展示。

## 功能特点

- 支持执行单条或多条命令
- 支持顺序执行和并行执行
- 支持基于文件或目录条件的执行控制
- 支持命令中包含双引号
- 支持从文本文件读取命令
- 支持错误处理和错误恢复
- 美观的命令执行进度展示
- 清晰的成功/失败状态显示
- 详细的命令输出信息

## 输出效果展示

### 顺序执行效果
```
╭──────────────╮
│ 开始执行命令 │
╰──────────────╯
按顺序执行命令中... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   0% -:--:--
执行命令: echo "Hello, World!"
╭─────────────── 执行成功 ────────────────╮
│ 命令 'echo "Hello, World!"' 执行成功    │
│                                         │
│ Hello, World!                           │
│                                         │
╰─────────────────────────────────────────╯
按顺序执行命令中... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
╭──────────────────╮
│ 所有命令执行成功 │
╰──────────────────╯
```

### 并行执行效果
```
╭──────────────╮
│ 开始执行命令 │
╰──────────────╯
并行执行所有命令...
╭───────────────── 执行成功 ──────────────────╮
│ 命令 'sleep 2 && echo "命令1完成"' 执行成功 │
│                                             │
│ 命令1完成                                   │
│                                             │
╰─────────────────────────────────────────────╯
╭────────────── 执行成功 ──────────────╮
│ 命令 'echo "命令2立即完成"' 执行成功 │
│                                      │
│ 命令2立即完成                        │
│                                      │
╰──────────────────────────────────────╯
```

### 错误处理效果
```
╭──────────────╮
│ 开始执行命令 │
╰──────────────╯
按顺序执行命令中... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   0% -:--:--
执行命令: echo "正常命令"
╭─────────── 执行成功 ────────────╮
│ 命令 'echo "正常命令"' 执行成功 │
│                                 │
│ 正常命令                        │
│                                 │
╰─────────────────────────────────╯
╭───────────── 执行失败 ──────────────╮
│ 命令 'nonexistent_command' 执行失败 │
│                                     │
│ 错误信息:                           │
│ 命令 'nonexistent_command' 不存在   │
╰─────────────────────────────────────╯
由于命令执行失败且未设置 --continue-on-error，停止执行后续命令
╭────────────────────────────╮
│ 执行完成，但有命令执行失败 │
╰────────────────────────────╯
```

### 文件检查效果
```
╭────────────────────────╮
│ 检查路径条件: test.txt │
╰────────────────────────╯
文件 'test.txt' 符合条件
╭──────────────╮
│ 开始执行命令 │
╰──────────────╯
按顺序执行命令中... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   0% -:--:--
执行命令: cat test.txt
╭────────── 执行成功 ───────────╮
│ 命令 'cat test.txt' 执行成功  │
│                               │
│ 文件内容                      │
│                               │
╰───────────────────────────────╯
```

## 安装

1. 确保你已安装 Python 3.7+
2. 安装依赖包：
```bash
pip install -r requirements.txt
```

## 使用方法

### 顺序执行命令
```bash
python main.py execute "ls -l" "pwd" "echo hello"
```

### 并行执行命令
```bash
python main.py execute --parallel "sleep 2" "echo hello" "date"
```

### 执行包含双引号的命令
```bash
# 使用单引号包裹包含双引号的命令
python main.py execute 'echo "Hello, World!"'
python main.py execute 'python -c "print(\"Hello\")"'
```

### 错误处理
```bash
# 默认情况下，遇到错误会停止执行
python main.py execute "echo '正常命令'" "nonexistent_command" "echo '不会执行'"

# 使用 --continue-on-error 选项继续执行
python main.py execute --continue-on-error "echo '正常命令'" "nonexistent_command" "echo '会继续执行'"
```

### 基于文件或目录条件执行命令
```bash
# 检查文件条件
python main.py execute --check-file "test.txt" --check-minutes 5 'echo "文件条件满足"'

# 检查目录条件
python main.py execute --check-dir "test_dir" --check-minutes 10 'echo "目录条件满足"'

# 并行模式下的文件检查
python main.py execute --parallel --check-file "test.txt" --check-minutes 5 'echo "命令1"' 'echo "命令2"'

# 并行模式下的目录检查
python main.py execute --parallel --check-dir "test_dir" --check-minutes 5 'echo "命令1"' 'echo "命令2"'
```

### 从文件读取命令
```bash
# 从文件中读取命令列表执行
python main.py execute --from-file commands.txt

# 从文件读取并并行执行
python main.py execute --from-file commands.txt --parallel

# 文件格式示例 (commands.txt):
# echo "Hello, World!"
# ls -l
# pwd
# date
```

## 命令行参数

- `--sequential/--parallel`: 选择是否按顺序执行命令（默认为顺序执行）
- `--check-file`: 指定需要检查的文件路径
- `--check-dir`: 指定需要检查的目录路径
- `--check-minutes`: 指定修改时间阈值，单位为分钟（默认为5分钟）
- `--from-file`: 指定包含命令列表的文本文件路径
- `--continue-on-error/--stop-on-error`: 命令执行失败时是否继续执行（默认为停止）
- 命令参数支持任意数量的命令

## 注意事项

- 每个命令都需要用引号括起来
- 如果命令本身包含双引号，请使用单引号包裹整个命令
- 从文件读取命令时，每行一条命令，空行会被忽略
- 并行执行时，所有命令会同时启动
- 在并行模式下，文件或目录检测会在所有命令执行前进行
- `--check-file` 和 `--check-dir` 不能同时使用
- 命令执行失败会显示详细的错误信息
- 默认情况下，命令执行失败会停止后续命令的执行
- 使用 `--continue-on-error` 可以在命令失败时继续执行后续命令 