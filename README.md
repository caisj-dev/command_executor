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