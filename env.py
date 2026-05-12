"""
# -*- coding: utf-8 -*-
# @Author: dr0n1
# @Link: https://www.dr0n.top/
# @Last Update: 2026/5/12
"""

import os
import shutil
import sqlite3
import subprocess
from collections.abc import Callable, Sequence

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
)

from styles import (
    apply_stylesheet,
    ENV_BUTTON_STYLE,
    ENV_CANCEL_BUTTON_STYLE,
    ENV_DIALOG_STYLE,
    ENV_GROUPBOX_STYLE,
    ENV_LINE_EDIT_STYLE,
    ENV_RADIO_BUTTON_STYLE,
    ENV_SAVE_BUTTON_STYLE,
    ENV_STATUS_LABEL_STYLE,
)
from db import DB_PATH

UNKNOWN_VERSION_MSG = "未知版本"
UNRECOGNIZED_VERSION_MSG = "未识别版本"
TIMEOUT_MSG = "检测超时"
NOT_DETECTED_MSG = "未检测到版本"
BUNDLED_RUNTIME_MSG = "使用内置环境变量"
SYSTEM_PYTHON_CHECK_MSG = "正在检测系统 Python..."
SYSTEM_JAVA_CHECK_MSG = "正在检测系统 Java..."
SYSTEM_PYTHON_MISSING_MSG = "未检测到系统 Python，请手动选择可执行文件"
SYSTEM_JAVA_MISSING_MSG = "未检测到系统 Java，请手动选择可执行文件"


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VersionArg = str | Sequence[str]


def _normalize_path(*parts: str) -> str:
    """Return an absolute project-local path with POSIX-style separators."""
    return os.path.abspath(os.path.join(BASE_DIR, *parts)).replace("\\", "/")


class Env:
    """Runtime executable paths used by tool launch commands."""

    def __init__(self) -> None:
        self.python3_path: str | None = None
        self.java8_path: str | None = None
        self.java11_path: str | None = None
        self.java16_path: str | None = None

    def load_env(self) -> None:
        """Load bundled runtime paths relative to the project root."""
        self.python3_path = _normalize_path("ENV", "python3.12.10", "python.exe")
        self.java8_path = _normalize_path("ENV", "Java_8", "bin", "java")
        self.java11_path = _normalize_path("ENV", "Java_11", "bin", "java")


env = Env()
env.load_env()


def _get_config_value(key: str, default: str = "") -> str:
    """Read one runtime config value, creating the table when needed."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS config "
            "(config_key TEXT PRIMARY KEY, config_value TEXT)"
        )
        cursor.execute("SELECT config_value FROM config WHERE config_key = ?", (key,))
        row = cursor.fetchone()
    return row[0] if row else default


def _save_config_values(values: dict[str, str]) -> None:
    """Persist runtime config values with upsert semantics."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS config "
            "(config_key TEXT PRIMARY KEY, config_value TEXT)"
        )
        cursor.executemany(
            "INSERT INTO config (config_key, config_value) VALUES (?, ?) "
            "ON CONFLICT(config_key) DO UPDATE "
            "SET config_value = excluded.config_value",
            values.items(),
        )
        conn.commit()


def _run_version(executable: str, arguments: VersionArg) -> str:
    """Run an executable version command and return the first output line."""
    candidates = arguments if isinstance(arguments, (list, tuple)) else (arguments,)
    last_message = UNKNOWN_VERSION_MSG

    for candidate in candidates:
        try:
            result = subprocess.run(
                [executable, candidate],
                capture_output=True,
                text=True,
                timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            output = (result.stdout or result.stderr).strip()
            if output:
                return output.splitlines()[0]
            last_message = UNKNOWN_VERSION_MSG
        except subprocess.TimeoutExpired:
            return TIMEOUT_MSG
        except Exception as exc:
            last_message = str(exc) or UNKNOWN_VERSION_MSG

    return last_message


class VersionWorker(QThread):
    """Background worker for runtime version detection."""

    result = Signal(str)

    def __init__(self, executable: str, arguments: VersionArg) -> None:
        super().__init__()
        self.executable = executable
        self.arguments = arguments

    def run(self) -> None:
        version = _run_version(self.executable, self.arguments) or ""
        self.result.emit(version)


def _track_worker(dialog: QDialog, worker: VersionWorker) -> None:
    """Keep a QThread alive until it emits finished."""
    worker.setParent(dialog)
    dialog._workers.append(worker)

    def _cleanup() -> None:
        try:
            dialog._workers.remove(worker)
        except ValueError:
            pass
        worker.deleteLater()

    worker.finished.connect(_cleanup)


def _version_message(version: str) -> str:
    """Map empty or failed version output to a display message."""
    if version and version not in (UNKNOWN_VERSION_MSG, TIMEOUT_MSG):
        return version
    return version or NOT_DETECTED_MSG


def _find_first_command(commands: Sequence[str]) -> str | None:
    """Return the first command found on PATH."""
    for command in commands:
        candidate = shutil.which(command)
        if candidate:
            return candidate
    return None


def show_env_dialog(parent: object, env_obj: Env | None = None) -> bool:
    """Show the runtime configuration dialog and persist accepted changes."""
    env_obj = env_obj or env

    dlg = QDialog(parent)
    dlg.setWindowTitle("环境配置")
    dlg.resize(700, 400)

    apply_stylesheet(dlg, ENV_DIALOG_STYLE)

    dlg._workers = []
    layout = QVBoxLayout(dlg)
    layout.setSpacing(20)
    layout.setContentsMargins(20, 20, 20, 20)

    py_group = QGroupBox("📦 Python3 配置", dlg)
    apply_stylesheet(py_group, ENV_GROUPBOX_STYLE)

    py_layout = QHBoxLayout(py_group)
    py_layout.setSpacing(12)

    py_builtin = QRadioButton("使用内置环境变量")
    py_custom = QRadioButton("使用系统环境变量")
    py_info = QLineEdit()
    py_info.setReadOnly(True)
    py_btn = QPushButton("🔍 自动识别/选择")

    apply_stylesheet(py_builtin, ENV_RADIO_BUTTON_STYLE)
    apply_stylesheet(py_custom, ENV_RADIO_BUTTON_STYLE)
    apply_stylesheet(py_info, ENV_LINE_EDIT_STYLE)
    apply_stylesheet(py_btn, ENV_BUTTON_STYLE)

    py_layout.addWidget(py_builtin)
    py_layout.addWidget(py_custom)
    py_layout.addWidget(py_info)
    py_layout.addWidget(py_btn)

    java_group = QGroupBox("☕ Java 配置", dlg)
    apply_stylesheet(java_group, ENV_GROUPBOX_STYLE)

    java_layout = QHBoxLayout(java_group)
    java_layout.setSpacing(12)

    java_builtin = QRadioButton("使用内置环境变量")
    java_custom = QRadioButton("使用系统环境变量")
    java_info = QLineEdit()
    java_info.setReadOnly(True)
    java_btn = QPushButton("🔍 自动识别/选择")

    apply_stylesheet(java_builtin, ENV_RADIO_BUTTON_STYLE)
    apply_stylesheet(java_custom, ENV_RADIO_BUTTON_STYLE)
    apply_stylesheet(java_info, ENV_LINE_EDIT_STYLE)
    apply_stylesheet(java_btn, ENV_BUTTON_STYLE)

    java_layout.addWidget(java_builtin)
    java_layout.addWidget(java_custom)
    java_layout.addWidget(java_info)
    java_layout.addWidget(java_btn)

    layout.addWidget(py_group)
    layout.addWidget(java_group)

    status_label = QLabel("")
    apply_stylesheet(status_label, ENV_STATUS_LABEL_STYLE)
    layout.addWidget(status_label)

    btn_layout = QHBoxLayout()
    btn_layout.setSpacing(12)
    btn_ok = QPushButton("✅ 保存")
    btn_cancel = QPushButton("❌ 取消")

    apply_stylesheet(btn_ok, ENV_SAVE_BUTTON_STYLE)
    apply_stylesheet(btn_cancel, ENV_CANCEL_BUTTON_STYLE)

    btn_layout.addStretch()
    btn_layout.addWidget(btn_ok)
    btn_layout.addWidget(btn_cancel)
    layout.addLayout(btn_layout)
    btn_cancel.clicked.connect(dlg.reject)

    use_py_builtin = _get_config_value("use_builtin_python", "true") == "true"
    use_java_builtin = _get_config_value("use_builtin_java", "true") == "true"
    py_custom_path = _get_config_value("python_custom_path", "")
    java_custom_path = _get_config_value("java_custom_path", "")

    py_status_text = ''
    java_status_text = ''

    def update_status() -> None:
        status_label.setText(f"{py_status_text} | {java_status_text}")

    def set_python_status(value: str) -> None:
        nonlocal py_status_text
        py_status_text = value

    def set_java_status(value: str) -> None:
        nonlocal java_status_text
        java_status_text = value

    def start_version_detection(
        executable: str,
        arguments: VersionArg,
        info_widget: QLineEdit,
        button: QPushButton,
        runtime_name: str,
        set_status: Callable[[str], None],
        empty_message: str | None = None,
    ) -> None:
        info_widget.setText("正在识别版本...")
        button.setEnabled(False)
        worker = VersionWorker(executable, arguments)

        def handle_result(version: str) -> None:
            if empty_message is not None and not version:
                message = empty_message
            else:
                message = _version_message(version)
            info_widget.setText(message)
            set_status(f"{runtime_name}: {message}")
            button.setEnabled(True)
            update_status()

        worker.result.connect(handle_result)
        _track_worker(dlg, worker)
        worker.start()

    py_builtin.setChecked(use_py_builtin)
    py_custom.setChecked(not use_py_builtin)
    java_builtin.setChecked(use_java_builtin)
    java_custom.setChecked(not use_java_builtin)

    if py_custom_path and not use_py_builtin:
        start_version_detection(
            py_custom_path,
            "--version",
            py_info,
            py_btn,
            "Python",
            set_python_status,
            empty_message=UNKNOWN_VERSION_MSG,
        )

    if java_custom_path and not use_java_builtin:
        start_version_detection(
            java_custom_path,
            ["-version", "--version"],
            java_info,
            java_btn,
            "Java",
            set_java_status,
            empty_message=UNRECOGNIZED_VERSION_MSG,
        )

    def update_py_controls() -> None:
        """Refresh Python controls after the source mode changes."""
        nonlocal py_status_text, py_custom_path

        if py_builtin.isChecked():
            py_info.setText(BUNDLED_RUNTIME_MSG)
            py_btn.setEnabled(False)
            py_status_text = f"Python: {BUNDLED_RUNTIME_MSG}"
            py_custom_path = ""
        else:
            if py_custom_path:
                start_version_detection(
                    py_custom_path,
                    "--version",
                    py_info,
                    py_btn,
                    "Python",
                    set_python_status,
                )
            else:
                py_info.setText(SYSTEM_PYTHON_CHECK_MSG)
                executable = _find_first_command(("python", "python3"))

                if not executable:
                    py_info.setText(SYSTEM_PYTHON_MISSING_MSG)
                    py_btn.setEnabled(True)
                    py_status_text = f"Python: {NOT_DETECTED_MSG}"
                    update_status()
                    return

                py_btn.setEnabled(False)
                start_version_detection(
                    executable,
                    "--version",
                    py_info,
                    py_btn,
                    "Python",
                    set_python_status,
                )

        update_status()

    def choose_python() -> None:
        nonlocal py_status_text, py_custom_path
        path, _ = QFileDialog.getOpenFileName(parent, "选择 python.exe", os.getcwd(), "可执行文件 (*.exe)")

        if path:
            py_custom_path = path
            start_version_detection(
                path,
                "--version",
                py_info,
                py_btn,
                "Python",
                set_python_status,
            )
        else:
            update_status()

    def update_java_controls() -> None:
        """Refresh Java controls after the source mode changes."""
        nonlocal java_status_text, java_custom_path

        if java_builtin.isChecked():
            java_info.setText(BUNDLED_RUNTIME_MSG)
            java_btn.setEnabled(False)
            java_status_text = f"Java: {BUNDLED_RUNTIME_MSG}"
            java_custom_path = ""
        else:
            if java_custom_path:
                start_version_detection(
                    java_custom_path,
                    ["-version", "--version"],
                    java_info,
                    java_btn,
                    "Java",
                    set_java_status,
                )
            else:
                java_info.setText(SYSTEM_JAVA_CHECK_MSG)
                executable = shutil.which("java")

                if not executable:
                    java_info.setText(SYSTEM_JAVA_MISSING_MSG)
                    java_btn.setEnabled(True)
                    java_status_text = f"Java: {NOT_DETECTED_MSG}"
                    update_status()
                    return

                java_btn.setEnabled(False)
                start_version_detection(
                    executable,
                    ["-version", "--version"],
                    java_info,
                    java_btn,
                    "Java",
                    set_java_status,
                )

        update_status()

    def choose_java() -> None:
        nonlocal java_status_text, java_custom_path
        path, _ = QFileDialog.getOpenFileName(parent, "选择 java.exe", os.getcwd(), "可执行文件 (*.exe)")

        if path:
            java_custom_path = path
            start_version_detection(
                path,
                ["-version", "--version"],
                java_info,
                java_btn,
                "Java",
                set_java_status,
            )
        else:
            update_status()

    py_builtin.toggled.connect(update_py_controls)
    py_custom.toggled.connect(update_py_controls)
    java_builtin.toggled.connect(update_java_controls)
    java_custom.toggled.connect(update_java_controls)
    py_btn.clicked.connect(choose_python)
    java_btn.clicked.connect(choose_java)

    update_py_controls()
    update_java_controls()

    def save_env() -> None:
        """Persist the selected runtime source and custom executable paths."""
        _save_config_values(
            {
                "use_builtin_python": "true" if py_builtin.isChecked() else "false",
                "use_builtin_java": "true" if java_builtin.isChecked() else "false",
                "python_custom_path": (
                    py_custom_path if py_custom.isChecked() and py_custom_path else ""
                ),
                "java_custom_path": (
                    java_custom_path if java_custom.isChecked() and java_custom_path else ""
                ),
            }
        )
        dlg.accept()

    btn_ok.clicked.connect(save_env)

    result = dlg.exec()
    return result == QDialog.Accepted


__all__ = ["Env", "env", "show_env_dialog"]
