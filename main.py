#!/usr/bin/env python3
import click
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
import time
import os
import shlex
from datetime import datetime, timedelta
import shutil

console = Console()

def check_path_condition(path, minutes=5, check_type="both"):
    """检查文件或文件夹是否存在且是最近指定分钟内修改的
    
    Args:
        path: 要检查的路径
        minutes: 时间阈值（分钟）
        check_type: 检查类型，可选值：'file'（仅文件）, 'dir'（仅目录）, 'both'（文件或目录）
    """
    # 检查路径是否存在
    if not os.path.exists(path):
        return False, f"路径 '{path}' 不存在"
    
    # 检查路径类型
    is_dir = os.path.isdir(path)
    is_file = os.path.isfile(path)
    
    if check_type == 'file' and not is_file:
        return False, f"路径 '{path}' 不是一个文件"
    elif check_type == 'dir' and not is_dir:
        return False, f"路径 '{path}' 不是一个目录"
    elif check_type == 'both' and not (is_file or is_dir):
        return False, f"路径 '{path}' 既不是文件也不是目录"
    
    # 检查修改时间
    path_mtime = datetime.fromtimestamp(os.path.getmtime(path))
    time_threshold = datetime.now() - timedelta(minutes=minutes)
    
    if path_mtime < time_threshold:
        path_type = "目录" if is_dir else "文件"
        return False, f"{path_type} '{path}' 不是在最近 {minutes} 分钟内修改的"
    
    path_type = "目录" if is_dir else "文件"
    return True, f"{path_type} '{path}' 符合条件"

def _safe_split_command(cmd):
    """安全地分割命令，保留引号内的内容"""
    try:
        return shlex.split(cmd)
    except ValueError as e:
        console.print(f"[red]命令格式错误: {e}[/red]")
        return None

def read_commands_from_file(file_path):
    """从文件中读取命令列表"""
    try:
        if not os.path.exists(file_path):
            console.print(f"[red]错误: 文件 '{file_path}' 不存在[/red]")
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            # 读取所有行，去除空行和首尾空白
            commands = [line.strip() for line in f.readlines() if line.strip()]
            
        if not commands:
            console.print("[red]错误: 命令文件为空[/red]")
            return None
            
        return commands
    except Exception as e:
        console.print(f"[red]读取命令文件时出错: {str(e)}[/red]")
        return None

def _check_command_exists(cmd):
    """检查命令是否存在"""
    cmd_name = shlex.split(cmd)[0]
    return shutil.which(cmd_name) is not None

def _execute_command_with_check(cmd, check_path=None, check_minutes=5, check_type="both"):
    """执行带有路径检查的命令"""
    if check_path:
        console.print(Panel.fit(f"检查路径条件: {check_path}", style="yellow"))
        condition_met, message = check_path_condition(check_path, check_minutes, check_type)
        console.print(message)
        if not condition_met:
            return False, "", "路径条件不满足"
    
    # 检查命令是否存在
    try:
        cmd_parts = shlex.split(cmd)
        if not _check_command_exists(cmd_parts[0]):
            return False, "", f"命令 '{cmd_parts[0]}' 不存在"
    except Exception:
        pass  # 如果命令解析失败，让它继续执行，错误会在实际执行时显示
    
    console.print(f"\n[cyan]执行命令:[/cyan] {cmd}")
    try:
        process = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        )
        return True, process.stdout, process.stderr
    except subprocess.SubprocessError as e:
        return False, "", f"执行出错: {str(e)}"
    except Exception as e:
        return False, "", f"未知错误: {str(e)}"

@click.group()
def cli():
    """命令行执行工具 - 可以执行多条命令并展示漂亮的输出"""
    pass

@cli.command()
@click.argument('commands', nargs=-1)
@click.option('--sequential/--parallel', default=True, help='是否按顺序执行命令')
@click.option('--check-file', help='检查的文件路径')
@click.option('--check-dir', help='检查的目录路径')
@click.option('--check-minutes', default=5, help='文件修改时间阈值（分钟）')
@click.option('--from-file', help='从文件中读取命令列表')
@click.option('--continue-on-error/--stop-on-error', default=False, help='命令出错时是否继续执行')
def execute(commands, sequential, check_file, check_dir, check_minutes, from_file, continue_on_error):
    """执行一个或多个shell命令

    示例:
    \b
    python main.py execute "ls -l" "pwd" "echo hello"
    python main.py execute --parallel "sleep 2" "echo hello"
    python main.py execute 'echo "包含双引号的命令"'
    python main.py execute --check-file "test.txt" --check-minutes 5 'echo "文件存在且最近修改"'
    python main.py execute --check-dir "test_dir" --check-minutes 5 'echo "目录存在且最近修改"'
    python main.py execute --parallel --check-file "test.txt" --check-minutes 5 'echo "并行模式下的文件检查"'
    python main.py execute --from-file commands.txt
    python main.py execute --continue-on-error "valid_cmd" "invalid_cmd" "valid_cmd"
    """
    # 从文件读取命令
    if from_file:
        file_commands = read_commands_from_file(from_file)
        if file_commands is None:
            return
        commands = file_commands
    
    if not commands:
        console.print("[red]请提供至少一条命令[/red]")
        return

    console.print(Panel.fit("开始执行命令", style="blue"))

    # 确定检查类型和路径
    check_path = None
    check_type = "both"
    if check_file:
        check_path = check_file
        check_type = "file"
    elif check_dir:
        check_path = check_dir
        check_type = "dir"

    error_occurred = False
    if sequential:
        for cmd in track(commands, description="按顺序执行命令中..."):
            success, stdout, stderr = _execute_command_with_check(cmd, check_path, check_minutes, check_type)
            if success:
                _display_result(cmd, 0, stdout, stderr)
            else:
                error_occurred = True
                _display_result(cmd, 1, stdout, stderr)
                if not continue_on_error:
                    console.print("[red]由于命令执行失败且未设置 --continue-on-error，停止执行后续命令[/red]")
                    break
    else:
        processes = []
        console.print("[yellow]并行执行所有命令...[/yellow]")
        
        # 如果有路径检查，先进行检查
        if check_path:
            console.print(Panel.fit(f"检查路径条件: {check_path}", style="yellow"))
            condition_met, message = check_path_condition(check_path, check_minutes, check_type)
            console.print(message)
            if not condition_met:
                return

        # 所有命令并行执行
        for cmd in commands:
            try:
                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                processes.append((cmd, process))
            except Exception as e:
                error_occurred = True
                _display_result(cmd, 1, "", str(e))
                if not continue_on_error:
                    console.print("[red]由于命令执行失败且未设置 --continue-on-error，停止执行后续命令[/red]")
                    return

        for cmd, process in processes:
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                error_occurred = True
            _display_result(cmd, process.returncode, stdout, stderr)

    if error_occurred:
        console.print(Panel.fit("执行完成，但有命令执行失败", style="red"))
    else:
        console.print(Panel.fit("所有命令执行成功", style="green"))

def _display_result(cmd, return_code, stdout, stderr):
    """显示命令执行结果"""
    if return_code == 0:
        console.print(Panel.fit(
            f"命令 [green]'{cmd}'[/green] 执行成功\n\n{stdout}",
            title="执行成功",
            style="green"
        ))
    else:
        console.print(Panel.fit(
            f"命令 [red]'{cmd}'[/red] 执行失败\n\n错误信息:\n{stderr}",
            title="执行失败",
            style="red"
        ))

if __name__ == '__main__':
    cli() 