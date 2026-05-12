"""
# -*- coding: utf-8 -*-
# @Author: dr0n1
# @Link: https://www.dr0n.top/
# @Last Update: 2025/11/29
"""

import os
import shutil
import sqlite3
import subprocess

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
TIMEOUT_MSG = "检测超时"
NOT_DETECTED_MSG = "未检测到版本"
BUNDLED_RUNTIME_MSG = "使用内置环境变量"
SYSTEM_PYTHON_CHECK_MSG = "正在检测系统 Python..."
SYSTEM_JAVA_CHECK_MSG = "正在检测系统 Java..."
SYSTEM_PYTHON_MISSING_MSG = "未检测到系统 Python，请手动选择可执行文件"
SYSTEM_JAVA_MISSING_MSG = "未检测到系统 Java，请手动选择可执行文件"


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _normalize_path(*parts):
    # 规范化并统一分隔符，生成相对项目根路径的绝对路径
    return os.path.abspath(os.path.join(BASE_DIR, *parts)).replace("\\", "/")


class Env:

    def __init__(self):
        self.python3_path = None
        self.java8_path = None
        self.java11_path = None

    def load_env(self):
        # 默认将运行时路径指向打包在项目下的内置 Python/Java
        self.python3_path = _normalize_path("ENV", "python3.12.10", "python.exe")
        self.java8_path = _normalize_path("ENV", "Java_8", "bin", "java")
        self.java11_path = _normalize_path("ENV", "Java_11", "bin", "java")


env = Env()
env.load_env()


def show_env_dialog(parent, env_obj=None):
    # 弹出环境配置对话框，允许选择内置或系统的 Python/Java 并写回配置
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

    def get_cfg(key, default=None):
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS config (config_key TEXT PRIMARY KEY, config_value TEXT)')
            c.execute('SELECT config_value FROM config WHERE config_key = ?', (key,))
            row = c.fetchone()
        return row[0] if row else default

    use_py_builtin = (get_cfg('use_builtin_python', 'true') == 'true')
    use_java_builtin = (get_cfg('use_builtin_java', 'true') == 'true')
    py_custom_path = get_cfg('python_custom_path', '')
    java_custom_path = get_cfg('java_custom_path', '')

    py_status_text = ''
    java_status_text = ''

    def update_status():
        status_label.setText(f"{py_status_text} | {java_status_text}")

    def run_version(exe, arg):
        # 以子进程调用给定可执行文件并返回首行版本输出，超时或异常时给出提示
        candidates = arg if isinstance(arg, (list, tuple)) else (arg,)
        last_message = UNKNOWN_VERSION_MSG

        for candidate in candidates:
            try:
                res = subprocess.run(
                    [exe, candidate],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                text = (res.stdout or res.stderr).strip()
                if text:
                    return text.splitlines()[0]
                last_message = UNKNOWN_VERSION_MSG
            except subprocess.TimeoutExpired:
                return TIMEOUT_MSG
            except Exception as exc:
                last_message = str(exc) or UNKNOWN_VERSION_MSG

        return last_message

    class VersionWorker(QThread):
        result = Signal(str)

        def __init__(self, exe, arg):
            super().__init__()
            self.exe = exe
            self.arg = arg

        def run(self):
            # 后台执行版本探测避免阻塞 UI 线程
            ver = run_version(self.exe, self.arg) or ""
            self.result.emit(ver)

    def _track_worker(worker):
        worker.setParent(dlg)
        dlg._workers.append(worker)

        def _cleanup():
            try:
                dlg._workers.remove(worker)
            except ValueError:
                pass
            worker.deleteLater()

        worker.finished.connect(_cleanup)

    py_builtin.setChecked(use_py_builtin)
    py_custom.setChecked(not use_py_builtin)
    java_builtin.setChecked(use_java_builtin)
    java_custom.setChecked(not use_java_builtin)

    if py_custom_path and not use_py_builtin:
        py_info.setText("正在识别版本...")
        py_btn.setEnabled(False)
        worker = VersionWorker(py_custom_path, "--version")

        def on_py_version(ver):
            nonlocal py_status_text
            if ver:
                py_info.setText(ver)
                py_status_text = f"Python: {ver}"
            else:
                py_info.setText(UNKNOWN_VERSION_MSG)
                py_status_text = f"Python: {UNKNOWN_VERSION_MSG}"
            py_btn.setEnabled(True)
            update_status()

        worker.result.connect(on_py_version)
        _track_worker(worker)
        worker.start()

    if java_custom_path and not use_java_builtin:
        java_info.setText("正在识别版本...")
        java_btn.setEnabled(False)
        worker = VersionWorker(java_custom_path, ["-version", "--version"])

        def on_java_version(ver):
            nonlocal java_status_text
            if ver:
                java_info.setText(ver)
                java_status_text = f"Java: {ver}"
            else:
                java_info.setText("未识别版本")
                java_status_text = "Java: 未识别版本"
            java_btn.setEnabled(True)
            update_status()

        worker.result.connect(on_java_version)
        _track_worker(worker)
        worker.start()

    def update_py_controls():
        # 根据选择的内置/系统模式刷新 Python 文本、探测状态与按钮可用性
        nonlocal py_status_text, py_custom_path

        if py_builtin.isChecked():
            py_info.setText(BUNDLED_RUNTIME_MSG)
            py_btn.setEnabled(False)
            py_status_text = f"Python: {BUNDLED_RUNTIME_MSG}"
            py_custom_path = ""
        else:
            def handle_result(ver):
                nonlocal py_status_text
                message = ver if ver and ver not in (UNKNOWN_VERSION_MSG, TIMEOUT_MSG) else (ver or NOT_DETECTED_MSG)
                if ver and ver not in (UNKNOWN_VERSION_MSG, TIMEOUT_MSG):
                    py_info.setText(ver)
                    py_status_text = f"Python: {ver}"
                else:
                    py_info.setText(message)
                    py_status_text = f"Python: {message}"
                py_btn.setEnabled(True)
                update_status()

            if py_custom_path:
                py_info.setText("正在识别版本...")
                py_btn.setEnabled(False)
                worker = VersionWorker(py_custom_path, "--version")
                worker.result.connect(handle_result)
                _track_worker(worker)
                worker.start()
            else:
                py_info.setText(SYSTEM_PYTHON_CHECK_MSG)
                exe = None
                for cmd in ("python", "python3"):
                    candidate = shutil.which(cmd)
                    if candidate:
                        exe = candidate
                        break

                if not exe:
                    py_info.setText(SYSTEM_PYTHON_MISSING_MSG)
                    py_btn.setEnabled(True)
                    py_status_text = f"Python: {NOT_DETECTED_MSG}"
                    update_status()
                    return

                py_btn.setEnabled(False)
                worker = VersionWorker(exe, "--version")
                worker.result.connect(handle_result)
                _track_worker(worker)
                worker.start()

        update_status()

    def choose_python():
        nonlocal py_status_text, py_custom_path
        path, _ = QFileDialog.getOpenFileName(parent, "选择 python.exe", os.getcwd(), "可执行文件 (*.exe)")

        if path:
            py_custom_path = path
            py_info.setText("正在识别版本...")
            py_btn.setEnabled(False)
            worker = VersionWorker(path, "--version")

            def on_py_version(ver):
                nonlocal py_status_text
                message = ver if ver and ver not in (UNKNOWN_VERSION_MSG, TIMEOUT_MSG) else (ver or NOT_DETECTED_MSG)
                if ver and ver not in (UNKNOWN_VERSION_MSG, TIMEOUT_MSG):
                    py_info.setText(ver)
                    py_status_text = f"Python: {ver}"
                else:
                    py_info.setText(message)
                    py_status_text = f"Python: {message}"
                py_btn.setEnabled(True)
                update_status()

            worker.result.connect(on_py_version)
            _track_worker(worker)
            worker.start()
        else:
            update_status()

    def update_java_controls():
        # 根据模式刷新 Java 显示内容并在需要时异步探测版本
        nonlocal java_status_text, java_custom_path

        if java_builtin.isChecked():
            java_info.setText(BUNDLED_RUNTIME_MSG)
            java_btn.setEnabled(False)
            java_status_text = f"Java: {BUNDLED_RUNTIME_MSG}"
            java_custom_path = ""
        else:
            def handle_result(ver):
                nonlocal java_status_text
                message = ver if ver and ver not in (UNKNOWN_VERSION_MSG, TIMEOUT_MSG) else (ver or NOT_DETECTED_MSG)
                if ver and ver not in (UNKNOWN_VERSION_MSG, TIMEOUT_MSG):
                    java_info.setText(ver)
                    java_status_text = f"Java: {ver}"
                else:
                    java_info.setText(message)
                    java_status_text = f"Java: {message}"
                java_btn.setEnabled(True)
                update_status()

            if java_custom_path:
                java_info.setText("正在识别版本...")
                java_btn.setEnabled(False)
                worker = VersionWorker(java_custom_path, ["-version", "--version"])
                worker.result.connect(handle_result)
                _track_worker(worker)
                worker.start()
            else:
                java_info.setText(SYSTEM_JAVA_CHECK_MSG)
                exe = shutil.which("java")

                if not exe:
                    java_info.setText(SYSTEM_JAVA_MISSING_MSG)
                    java_btn.setEnabled(True)
                    java_status_text = f"Java: {NOT_DETECTED_MSG}"
                    update_status()
                    return

                java_btn.setEnabled(False)
                worker = VersionWorker(exe, ["-version", "--version"])
                worker.result.connect(handle_result)
                _track_worker(worker)
                worker.start()

        update_status()

    def choose_java():
        nonlocal java_status_text, java_custom_path
        path, _ = QFileDialog.getOpenFileName(parent, "选择 java.exe", os.getcwd(), "可执行文件 (*.exe)")

        if path:
            java_custom_path = path
            java_info.setText("正在识别版本...")
            java_btn.setEnabled(False)
            worker = VersionWorker(path, ["-version", "--version"])

            def on_java_version(ver):
                nonlocal java_status_text
                message = ver if ver and ver not in (UNKNOWN_VERSION_MSG, TIMEOUT_MSG) else (ver or NOT_DETECTED_MSG)
                if ver and ver not in (UNKNOWN_VERSION_MSG, TIMEOUT_MSG):
                    java_info.setText(ver)
                    java_status_text = f"Java: {ver}"
                else:
                    java_info.setText(message)
                    java_status_text = f"Java: {message}"
                java_btn.setEnabled(True)
                update_status()

            worker.result.connect(on_java_version)
            _track_worker(worker)
            worker.start()
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

    def save_env():
        # 将当前选择的运行时模式与路径写入 config 表
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS config (config_key TEXT PRIMARY KEY, config_value TEXT)')

            def upsert(k, v):
                c.execute(
                    'INSERT INTO config (config_key, config_value) VALUES (?, ?) '
                    'ON CONFLICT(config_key) DO UPDATE SET config_value = excluded.config_value', (k, v))

            upsert('use_builtin_python', 'true' if py_builtin.isChecked() else 'false')
            upsert('use_builtin_java', 'true' if java_builtin.isChecked() else 'false')
            upsert('python_custom_path', py_custom_path if (py_custom.isChecked() and py_custom_path) else '')
            upsert('java_custom_path', java_custom_path if (java_custom.isChecked() and java_custom_path) else '')

            conn.commit()
        dlg.accept()

    btn_ok.clicked.connect(save_env)

    result = dlg.exec()
    return result == QDialog.Accepted


__all__ = ["Env", "env", "show_env_dialog"]
