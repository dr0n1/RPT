"""Runtime command helpers shared by the application entry points."""

import os
import shlex
import shutil
from collections.abc import Sequence


def split_command_arguments(arguments: str | None) -> list[str]:
    """Split a user-provided argument string while preserving Windows quoting."""
    if not arguments:
        return []
    try:
        return shlex.split(arguments, posix=False)
    except ValueError:
        return arguments.split()


def resolve_configured_executable(
    configured_path: str | None,
    executable_name: str,
    fallback_commands: Sequence[str],
) -> str:
    """Resolve a configured executable path, directory, command, or fallback."""
    executable_path = (configured_path or "").strip()

    if _is_shell_command(executable_path):
        located = shutil.which(executable_path)
        return _normalize_path(located) if located else executable_path

    if executable_path:
        executable_path = _resolve_filesystem_executable(
            executable_path,
            executable_name,
        )

    if executable_path:
        return _normalize_path(executable_path)

    for command in fallback_commands:
        located = shutil.which(command)
        if located:
            return _normalize_path(located)

    return ""


def resolve_relative_executable(
    command: Sequence[str] | str,
    working_dir: str,
) -> str:
    """Resolve a command executable only when it is file-like."""
    if isinstance(command, str) or not command:
        return ""

    candidate = command[0]
    if not candidate:
        return ""
    if os.path.isabs(candidate):
        return candidate

    separators = (os.path.sep, os.path.altsep) if os.path.altsep else (os.path.sep,)
    if all(separator not in candidate for separator in separators):
        return ""

    return os.path.join(working_dir, candidate)


def escape_cmd_echo(command_text: str) -> str:
    """Escape command text so cmd.exe can echo it before execution."""
    replacements = {
        "^": "^^",
        "&": "^&",
        "|": "^|",
        ">": "^>",
        "<": "^<",
        '"': '""',
    }
    escaped = command_text
    for char, replacement in replacements.items():
        escaped = escaped.replace(char, replacement)
    return escaped


def _is_shell_command(candidate: str) -> bool:
    """Return True for command names without path separators."""
    if not candidate or os.path.isabs(candidate):
        return False
    return all(separator not in candidate for separator in ("/", "\\"))


def _resolve_filesystem_executable(path: str, executable_name: str) -> str:
    """Resolve a configured file or directory to an executable file."""
    normalized_path = os.path.normpath(path)

    if os.path.isdir(normalized_path):
        candidate = os.path.join(normalized_path, executable_name)
        if os.path.isfile(candidate):
            normalized_path = candidate

    if (
        normalized_path
        and os.name == "nt"
        and not normalized_path.lower().endswith(".exe")
    ):
        candidate = f"{normalized_path}.exe"
        if os.path.isfile(candidate):
            normalized_path = candidate

    return normalized_path if os.path.isfile(normalized_path) else ""


def _normalize_path(path: str) -> str:
    """Normalize path separators for command display and subprocess calls."""
    return path.replace("\\", "/")
