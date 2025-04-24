"""Bash backend for command execution."""

import os
import platform
import subprocess
import time
from typing import Dict, Tuple

from wish_models import CommandResult, CommandState, Wish
from wish_models.executable_collection import ExecutableCollection
from wish_models.system_info import SystemInfo

from wish_command_execution.backend.base import Backend
from wish_command_execution.system_info import SystemInfoCollector


class BashBackend(Backend):
    """Backend for executing commands using bash."""

    def __init__(self):
        """Initialize the bash backend."""
        self.running_commands: Dict[int, Tuple[subprocess.Popen, CommandResult, Wish]] = {}

    async def execute_command(self, wish: Wish, command: str, cmd_num: int, log_files) -> None:
        """Execute a command using bash.

        Args:
            wish: The wish to execute the command for.
            command: The command to execute.
            cmd_num: The command number.
            log_files: The log files to write output to.
        """
        # Create command result
        result = CommandResult.create(cmd_num, command, log_files)
        wish.command_results.append(result)

        # 変数置換を行う
        replaced_command = self._replace_variables(command, wish)

        with open(log_files.stdout, "w") as stdout_file, open(log_files.stderr, "w") as stderr_file:
            try:
                # 変数置換前後のコマンドをログに出力
                if command != replaced_command:
                    stdout_file.write(f"# Original command: {command}\n")
                    stdout_file.write(f"# Command after variable replacement: {replaced_command}\n\n")

                # Start the process (this is still synchronous, but the interface is async)
                process = subprocess.Popen(
                    replaced_command,
                    stdout=stdout_file,
                    stderr=stderr_file,
                    shell=True,
                    text=True
                )

                # Store in running commands dict
                self.running_commands[cmd_num] = (process, result, wish)

                # Wait for process completion (non-blocking return for UI)
                return

            except subprocess.SubprocessError as e:
                error_msg = f"Subprocess error: {str(e)}"
                stderr_file.write(error_msg)
                self._handle_command_failure(result, wish, 1, CommandState.OTHERS)

            except PermissionError:
                error_msg = f"Permission error: No execution permission for command '{command}'"
                stderr_file.write(error_msg)
                self._handle_command_failure(result, wish, 126, CommandState.OTHERS)

            except FileNotFoundError:
                error_msg = f"Command not found: '{command}'"
                stderr_file.write(error_msg)
                self._handle_command_failure(result, wish, 127, CommandState.COMMAND_NOT_FOUND)

            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                stderr_file.write(error_msg)
                self._handle_command_failure(result, wish, 1, CommandState.OTHERS)

    def _replace_variables(self, command: str, wish: Wish) -> str:
        """コマンド内の変数を置換する

        Args:
            command: 置換前のコマンド
            wish: Wishオブジェクト

        Returns:
            置換後のコマンド
        """
        if not command:
            print("Warning: Empty command provided for variable replacement")
            return command

        # 基本的な変数の置換
        replacements = {}

        # ターゲットIPとLHOSTの取得
        try:
            # wishオブジェクトから情報を取得
            if hasattr(wish, 'context') and wish.context:
                target_info = wish.context.get('target', {})
                attacker_info = wish.context.get('attacker', {})

                # ターゲットIP
                rhost = target_info.get('rhost', '')
                if rhost:
                    replacements['$TARGET_IP'] = rhost

                # 攻撃者IP
                lhost = attacker_info.get('lhost', '')
                if lhost:
                    replacements['$LHOST'] = lhost
        except Exception as e:
            print(f"Error extracting variables from wish: {str(e)}")

        # 変数置換の実行
        result = command
        for var, value in replacements.items():
            if var in result:
                if value:  # 値が存在する場合のみ置換
                    print(f"Replacing {var} with {value}")
                    result = result.replace(var, value)
                else:
                    print(f"Warning: Variable {var} found in command but no value available")

        return result

    def _handle_command_failure(
        self, result: CommandResult, wish: Wish, exit_code: int, state: CommandState
    ):
        """Common command failure handling."""
        result.finish(
            exit_code=exit_code,
            state=state
        )
        # Update the command result in the wish object
        # This is a workaround for Pydantic models that don't allow dynamic attribute assignment
        for i, cmd_result in enumerate(wish.command_results):
            if cmd_result.num == result.num:
                wish.command_results[i] = result
                break

    async def check_running_commands(self):
        """Check status of running commands and update their status."""
        for idx, (process, result, wish) in list(self.running_commands.items()):
            if process.poll() is not None:  # Process has finished
                # Mark the command as finished with exit code
                result.finish(
                    exit_code=process.returncode
                )

                # Update the command result in the wish object
                # This is a workaround for Pydantic models that don't allow dynamic attribute assignment
                for i, cmd_result in enumerate(wish.command_results):
                    if cmd_result.num == result.num:
                        wish.command_results[i] = result
                        break

                # Remove from running commands
                del self.running_commands[idx]

    async def cancel_command(self, wish: Wish, cmd_num: int) -> str:
        """Cancel a running command.

        Args:
            wish: The wish to cancel the command for.
            cmd_num: The command number to cancel.

        Returns:
            A message indicating the result of the cancellation.
        """
        if cmd_num in self.running_commands:
            process, result, _ = self.running_commands[cmd_num]

            # Try to terminate the process
            try:
                process.terminate()
                time.sleep(0.5)
                if process.poll() is None:  # Process still running
                    process.kill()  # Force kill
            except Exception:
                pass  # Ignore errors in termination

            # Mark the command as cancelled
            result.finish(
                exit_code=-1,  # Use -1 for cancelled commands
                state=CommandState.USER_CANCELLED
            )

            # Update the command result in the wish object
            # This is a workaround for Pydantic models that don't allow dynamic attribute assignment
            for i, cmd_result in enumerate(wish.command_results):
                if cmd_result.num == result.num:
                    wish.command_results[i] = result
                    break

            del self.running_commands[cmd_num]

            return f"Command {cmd_num} cancelled."
        else:
            return f"Command {cmd_num} is not running."

    async def get_executables(self, collect_system_executables: bool = False) -> ExecutableCollection:
        """Get executable files information from the local system.

        Args:
            collect_system_executables: Whether to collect executables from the entire system

        Returns:
            ExecutableCollection: Collection of executables
        """
        # Collect executables in PATH
        path_executables = SystemInfoCollector._collect_local_path_executables()

        # Optionally collect system-wide executables
        if collect_system_executables:
            system_executables = SystemInfoCollector._collect_local_system_executables()

            # Merge system executables into path executables
            for exe in system_executables.executables:
                path_executables.executables.append(exe)

        return path_executables

    async def get_system_info(self) -> SystemInfo:
        """Get system information from the local system.

        Args:
            collect_system_executables: Whether to collect executables from the entire system

        Returns:
            SystemInfo: Collected system information
        """
        # Basic information
        system = platform.system()
        info = SystemInfo(
            os=system,
            arch=platform.machine(),
            version=platform.version(),
            hostname=platform.node(),
            username=os.getlogin(),
            pid=os.getpid()
        )

        # Add UID and GID for Unix-like systems
        if system != "Windows":
            info.uid = str(os.getuid())
            info.gid = str(os.getgid())

        return info
