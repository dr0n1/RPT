"""
# -*- coding: utf-8 -*-
# @Author: dr0n1
# @Link: https://www.dr0n.top/
# @Last Update: 2025/11/29
"""

import os
import shlex
import shutil
import sqlite3
import subprocess
import sys
import webbrowser
from functools import partial

from PySide6.QtCore import Qt, QTimer, QDateTime, QEvent, QPoint
from PySide6.QtGui import QIcon, QShortcut, QColor, QPainter, QPen, QPainterPath
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from db import DB_PATH, create_db, restore_database_defaults as db_restore_database_defaults, show_database_dialog, upgrade_db
from env import env, show_env_dialog
from styles import *
from styles.ui_main import Ui_MainWindow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class RoundedToolTip(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.ToolTip | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setObjectName("RoundedToolTip")
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAutoFillBackground(False)

        self._bg_color = QColor("#ffffff")
        self._border_color = QColor("#dbeafe")
        self._radius = 10
        self._shadow_margin = 6

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            self._shadow_margin,
            self._shadow_margin,
            self._shadow_margin,
            self._shadow_margin,
        )
        self._label = QLabel(self)
        self._label.setWordWrap(True)
        self._label.setMaximumWidth(360)
        layout.addWidget(self._label)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        outer = self.rect()
        inner = outer.adjusted(
            self._shadow_margin,
            self._shadow_margin,
            -self._shadow_margin,
            -self._shadow_margin,
        )

        # Soft shadow with rounded corners (no square halo).
        for i, alpha in enumerate((28, 18, 10), start=1):
            shadow_rect = inner.adjusted(-i, -i, i, i).translated(0, 1)
            shadow_path = QPainterPath()
            shadow_path.addRoundedRect(
                shadow_rect, self._radius + i, self._radius + i
            )
            painter.fillPath(shadow_path, QColor(15, 23, 42, alpha))

        path = QPainterPath()
        path.addRoundedRect(inner, self._radius, self._radius)
        painter.fillPath(path, self._bg_color)
        pen = QPen(self._border_color)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawPath(path)

    def show_text(self, text, global_pos):
        if not text:
            self.hide()
            return
        self._label.setText(text)
        self.adjustSize()
        offset = QPoint(12, 16)
        self.move(global_pos + offset)
        self.show()
        self.raise_()


def check_and_init_db():
    # 确保 tools.db 存在且表结构可用，异常或缺失时重建并执行升级逻辑
    if not os.path.exists(DB_PATH):
        create_db()
        return

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='modules'")
            table_exists = cursor.fetchone()
        if not table_exists:
            try:
                os.remove(DB_PATH)
            except OSError:
                pass
            create_db()
            return
        upgrade_db()
    except Exception:
        try:
            os.remove(DB_PATH)
        except OSError:
            pass
        create_db()


def create_module_directories():
    # 根据 modules 表中的目录字段创建对应的本地文件夹，保证工具路径可用
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT directory FROM modules')
            module_directories = [row[0] for row in c.fetchall()]

        for directory in module_directories:
            full_path = os.path.join(BASE_DIR, directory)
            os.makedirs(full_path, exist_ok=True)
    except Exception:
        pass


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._setup_main_styles()
        self._setup_widget_styles()
        self._setup_tooltip()
        self._configure_menus()
        self._setup_fonts()
        self._setup_window_icon()
        self._bind_events()
        self._initialize_data()
        self._setup_status_bar()
        self._update_status_bar_style()
        self._setup_timer()
        self._setup_layout()
        self._setup_shortcuts()

    def _setup_main_styles(self):
        app = QApplication.instance()
        if app is not None:
            # Apply globally so QToolTip (top-level) gets rounded corners.
            app.setStyleSheet(MAIN_WINDOW_STYLE)
        else:
            self.setStyleSheet(MAIN_WINDOW_STYLE)

    def _setup_widget_styles(self):
        self.ui.groupBox.setStyleSheet(GROUPBOX_STYLE)
        self.ui.listWidget.setStyleSheet(LISTWIDGET_STYLE)
        self.ui.listWidget.setAttribute(Qt.WA_StyledBackground, True)
        # Let stylesheet handle rounded background; avoid palette autofill.
        self.ui.listWidget.setAutoFillBackground(False)
        if self.ui.listWidget.viewport() is not None:
            self.ui.listWidget.viewport().setAutoFillBackground(False)
        self.ui.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.listWidget.setSpacing(4)
        self.ui.listWidget.setContentsMargins(8, 8, 8, 8)
        self.ui.listWidget.setTextElideMode(Qt.ElideNone)
        self.ui.listWidget.setWordWrap(False)

    def _setup_tooltip(self):
        self._tooltip = RoundedToolTip(self)
        self._tooltip.setStyleSheet(CUSTOM_TOOLTIP_STYLE)

    def _setup_fonts(self):
        font = self.ui.listWidget.font()
        font.setPointSize(11)
        font.setBold(True)
        self.ui.listWidget.setFont(font)

    def _setup_window_icon(self):
        icon_path = os.path.abspath(os.path.join(BASE_DIR, 'styles', 'logo.png'))
        self.setWindowIcon(QIcon(icon_path))

    def _bind_events(self):
        self.ui.listWidget.itemClicked.connect(self.on_module_clicked)
        self.ui.action_about.triggered.connect(self.show_about_toolbox)
        self.ui.action_env.triggered.connect(self.env)
        self.ui.action_database.triggered.connect(self.database)

    def _initialize_data(self):
        self.load_modules()
        self.load_config_env()
        if self.ui.listWidget.count() > 0:
            first_item = self.ui.listWidget.item(0)
            self.ui.listWidget.setCurrentItem(first_item)
            self.on_module_clicked(first_item)

    def _setup_status_bar(self):
        self.statusBar().showMessage("⌛...")
        self.statusBar().setStyleSheet("QStatusBar::item {border: none;}")
        self.copyright_label = QLabel("⌛...")
        self.statusBar().addWidget(self.copyright_label, 1)
        self.time_label = QLabel()
        self.statusBar().addPermanentWidget(self.time_label)

    def _update_status_bar_style(self):
        status_style = """
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #ffffff, stop:1 #f8fafc);
                border-top: 1px solid #e2e8f0;
                padding: 4px;
            }
            QStatusBar::item {
                border: none;
                padding: 4px 8px;
            }
        """
        self.statusBar().setStyleSheet(status_style)

    def _setup_timer(self):
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.update_time()

    def _setup_layout(self):
        self.ui.groupBox.setContentsMargins(10, 10, 10, 10)
        # Remove designer max-height caps so both panels can stretch equally.
        self.ui.groupBox.setMaximumHeight(16777215)
        self.ui.listWidget.setMaximumHeight(16777215)
        # Use layout to keep both panels the same height automatically.
        if self.ui.centralwidget.layout() is None:
            layout = QHBoxLayout(self.ui.centralwidget)
            layout.setContentsMargins(12, 18, 12, 18)
            layout.setSpacing(16)
            # Wrap the list in a styled container to ensure visible rounded corners.
            self._list_container = QWidget(self.ui.centralwidget)
            self._list_container.setObjectName("listContainer")
            self._list_container.setAttribute(Qt.WA_StyledBackground, True)
            inner_layout = QVBoxLayout(self._list_container)
            inner_layout.setContentsMargins(0, 0, 0, 0)
            inner_layout.setSpacing(0)
            self.ui.listWidget.setParent(self._list_container)
            self.ui.listWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            # Center horizontally, allow full height.
            inner_layout.addWidget(self.ui.listWidget, 1, Qt.AlignHCenter)
            self._list_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            self._list_container.setMaximumWidth(16777215)
            self._list_container.setMinimumWidth(self.ui.listWidget.sizeHint().width() + 16)
            self._list_container.setStyleSheet(LIST_CONTAINER_STYLE)
            self.ui.groupBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            layout.addWidget(self._list_container)
            layout.addWidget(self.ui.groupBox, 1)
        else:
            # Ensure margins stay in sync if layout already exists.
            self.ui.centralwidget.layout().setContentsMargins(12, 18, 12, 18)
            self.ui.centralwidget.layout().setSpacing(16)
            if hasattr(self, "_list_container"):
                self._list_container.setStyleSheet(LIST_CONTAINER_STYLE)
        self._resize_panels()
        self._adjust_list_width()

    def _setup_shortcuts(self):
        self._search_shortcut = QShortcut("Ctrl+F", self)
        self._search_shortcut.activated.connect(self.show_search_dialog)

        app = QApplication.instance()
        if app is not None:
            app.installEventFilter(self)

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.time_label.setText(current_time)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._resize_panels()

    def _resize_panels(self):
        # If a layout is set, it keeps both panels aligned; just ensure margins stay consistent.
        layout = self.ui.centralwidget.layout()
        if layout is not None:
            layout.setContentsMargins(10, 20, 10, 20)
            return

    def _configure_menus(self):
        for menu in self.menuBar().findChildren(QMenu):
            self._prepare_menu(menu)

    def _prepare_menu(self, menu):
        if menu.property("_polished_menu"):
            return
        menu.setProperty("_polished_menu", True)
        self._apply_menu_flags(menu)
        menu.aboutToShow.connect(lambda m=menu: self._on_menu_about_to_show(m))

    def _apply_menu_flags(self, menu):
        menu.setWindowFlag(Qt.FramelessWindowHint, True)
        menu.setWindowFlag(Qt.NoDropShadowWindowHint, True)
        menu.setAttribute(Qt.WA_TranslucentBackground, True)
        menu.setContentsMargins(0, 0, 0, 0)
        effect = menu.graphicsEffect()
        if effect is not None:
            effect.setEnabled(False)
            menu.setGraphicsEffect(None)
        shadow = menu.findChild(QWidget, "qt_menu_shadow")
        if shadow is not None:
            shadow.hide()
            shadow.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            shadow.deleteLater()

    def _on_menu_about_to_show(self, menu):
        self._apply_menu_flags(menu)
        for sub_menu in menu.findChildren(QMenu):
            self._prepare_menu(sub_menu)

    def show_about_toolbox(self):
        self._show_about_dialog()

    def _show_about_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("About Toolbox")
        dialog.resize(500, 400)
        dialog.setMinimumSize(450, 350)
        dialog.setMaximumSize(600, 500)
        dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)

        dialog.setStyleSheet(DIALOG_STYLE)

        main_layout = QVBoxLayout(dialog)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSizeConstraint(QVBoxLayout.SetMinAndMaxSize)

        main_layout.addLayout(self._create_title_section())
        main_layout.addLayout(self._create_content_section())
        main_layout.addLayout(self._create_button_section(dialog))

        dialog.exec()

    def _create_title_section(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        title_label = QLabel("关于工具箱")
        title_label.setStyleSheet(DIALOG_LABEL_TITLE_STYLE)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        version_label = QLabel("Version 3.0")
        version_label.setStyleSheet(DIALOG_LABEL_VERSION_STYLE)
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)

        return layout

    def _create_content_section(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        author_label = QLabel("作者：Rml@dr0n1")
        author_label.setStyleSheet(DIALOG_LABEL_INFO_STYLE)
        layout.addWidget(author_label)

        website_label = QLabel("blog：https://www.dr0n.top/")
        website_label.setStyleSheet(DIALOG_LABEL_INFO_STYLE)
        layout.addWidget(website_label)

        desc_label = QLabel("简介")
        desc_label.setStyleSheet(DIALOG_LABEL_DESC_TITLE_STYLE)
        layout.addWidget(desc_label)

        desc_text = QLabel("面向 Windows 的本地渗透/安全研究工具启动器。应用使用 PySide6 构建单窗口界面，内置 SQLite 数据库保存工具清单，支持一键启动脚本、二进制或打开目录/网页，并提供可视化的环境与数据库管理能力。")
        desc_text.setStyleSheet(DIALOG_LABEL_DESC_TEXT_STYLE)
        desc_text.setWordWrap(True)
        desc_text.setAlignment(Qt.AlignTop)
        desc_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(desc_text)

        return layout

    def _create_button_section(self, dialog):
        layout = QHBoxLayout()
        layout.setSpacing(12)
        layout.setSizeConstraint(QHBoxLayout.SetMinAndMaxSize)

        website_btn = QPushButton("完整版下载")
        website_btn.setStyleSheet(DIALOG_BUTTON_PRIMARY_STYLE)
        website_btn.clicked.connect(lambda: webbrowser.open("https://pan.quark.cn/s/b134d9a371d5"))
        website_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        close_btn = QPushButton("关闭")
        close_btn.setStyleSheet(DIALOG_BUTTON_SECONDARY_STYLE)
        close_btn.clicked.connect(dialog.accept)
        close_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        layout.addStretch()
        layout.addWidget(website_btn)
        layout.addWidget(close_btn)

        return layout

    def database(self):
        show_database_dialog(self)
        self.load_modules()

    def refresh_database(self):
        current_item = self.ui.listWidget.currentItem()
        current_name = current_item.text() if current_item else None

        self.load_modules()

        target_item = None
        if current_name:
            matches = self.ui.listWidget.findItems(current_name, Qt.MatchExactly)
            if matches:
                target_item = matches[0]

        if target_item is None and self.ui.listWidget.count() > 0:
            target_item = self.ui.listWidget.item(0)

        if target_item:
            self.ui.listWidget.setCurrentItem(target_item)
            self.on_module_clicked(target_item)

        try:
            self.statusBar().showMessage("数据库已刷新", 2000)
        except Exception:
            pass

    def restore_database_defaults(self):
        db_restore_database_defaults(self, self.refresh_database)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.ToolTip:
            text = ""
            if isinstance(obj, QWidget):
                text = obj.toolTip()
            if hasattr(self, "_tooltip"):
                self._tooltip.show_text(text, event.globalPos())
            return True
        if event.type() in (QEvent.Leave, QEvent.MouseButtonPress, QEvent.FocusOut):
            if hasattr(self, "_tooltip"):
                self._tooltip.hide()
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_F5:
            if event.modifiers() & Qt.ShiftModifier:
                self.restore_database_defaults()
                return True
        return super().eventFilter(obj, event)

    def env(self):
        show_env_dialog(self, env)
        self.load_config_env()

    def load_modules(self):
        self.ui.listWidget.clear()
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT name FROM modules ORDER BY sort_order, id')
            modules = [row[0] for row in c.fetchall()]
        for module_name in modules:
            item = QListWidgetItem(module_name)
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.ui.listWidget.addItem(item)
        self._adjust_list_width()

    def _adjust_list_width(self):
        # Center items and size the list based on the widest text so left/right padding matches.
        count = self.ui.listWidget.count()
        if count == 0:
            return
        fm = self.ui.listWidget.fontMetrics()
        max_text_width = max(fm.horizontalAdvance(self.ui.listWidget.item(i).text()) for i in range(count))
        # Add generous padding so text never elides; keep consistent side space.
        list_width = max(max_text_width + 64, 180)
        self.ui.listWidget.setMinimumWidth(list_width)
        self.ui.listWidget.setMaximumWidth(list_width)

        if hasattr(self, "_list_container"):
            container_width = list_width + 28  # container padding 14*2
            self._list_container.setMinimumWidth(container_width)
            self._list_container.setMaximumWidth(container_width)

    def load_config_env(self):
        # 从 config 表读取运行环境配置并回填到 env 对象，优先使用自定义路径
        try:
            env.load_env()
            with sqlite3.connect(DB_PATH) as conn:
                c = conn.cursor()
                c.execute("SELECT config_key, config_value FROM config")
                cfg = {k: v for k, v in c.fetchall()}

            use_py_builtin = (cfg.get("use_builtin_python", "true") == "true")
            python_custom = (cfg.get("python_custom_path") or '').strip()
            if use_py_builtin:
                pass
            elif python_custom:
                env.python3_path = python_custom.replace('\\', '/')
            else:
                if shutil.which("python"):
                    env.python3_path = "python"
                elif shutil.which("python3"):
                    env.python3_path = "python3"
                else:
                    env.python3_path = ''

            use_java_builtin = (cfg.get("use_builtin_java", "true") == "true")
            java_custom = (cfg.get("java_custom_path") or '').strip()
            if use_java_builtin:
                pass
            elif java_custom:
                custom = java_custom.replace('\\', '/')
                env.java8_path = custom
                env.java11_path = custom
                env.java16_path = custom
            else:
                if shutil.which("java"):
                    env.java8_path = "java"
                    env.java11_path = "java"
                    env.java16_path = "java"
                else:
                    env.java8_path = ""
                    env.java11_path = ""
                    env.java16_path = ""
        except Exception:
            pass

    def on_module_clicked(self, item):
        # 点击模块列表时查询该模块下启用的工具并动态刷新按钮区
        module_name = item.text()
        self.clear_tool_buttons()

        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT id FROM modules WHERE name = ?', (module_name,))
            module_row = c.fetchone()
            if not module_row:
                return
            module_id = module_row[0]
            c.execute(
                '''
                SELECT name, description, entry_path, runtime_key, arguments
                FROM tools
                WHERE module_id = ? AND is_enabled = 1
                ORDER BY LOWER(name), id
                ''',
                (module_id,),
            )
            tools = c.fetchall()

        self._create_tool_buttons(tools, module_name)

    def _create_tool_buttons(self, tools, module_name):
        # 按可用宽度自动换行生成工具按钮，使界面在不同窗口尺寸下自适应
        v_layout = self.ui.groupBox.layout()
        if v_layout is None or not isinstance(v_layout, QVBoxLayout):
            v_layout = QVBoxLayout()
            v_layout.setAlignment(Qt.AlignTop)
            v_layout.setSpacing(15)
            v_layout.setContentsMargins(0, 0, 0, 0)
            self.ui.groupBox.setLayout(v_layout)

        def _new_row_layout():
            layout = QHBoxLayout()
            layout.setAlignment(Qt.AlignLeft)
            layout.setSpacing(12)
            layout.setContentsMargins(0, 0, 0, 0)
            return layout

        h_layout = _new_row_layout()
        current_width = 0
        available_width = self.ui.groupBox.contentsRect().width()
        if available_width <= 0:
            available_width = self.ui.groupBox.width()
        if available_width <= 0:
            available_width = 600

        for tool_name, description, entry_path, runtime_key, arguments in tools:
            if not description:
                description = "No description provided"

            button = self._create_tool_button(
                tool_name, description, module_name, entry_path, runtime_key, arguments
            )
            button.ensurePolished()
            base_width = max(button.sizeHint().width(), button.minimumSizeHint().width())
            button_width = base_width + 16
            button.setFixedWidth(button_width)

            effective_width = max(available_width, button_width)
            projected_width = (
                button_width if current_width == 0 else current_width + h_layout.spacing() + button_width
            )

            if projected_width <= effective_width or current_width == 0:
                h_layout.addWidget(button)
                current_width = projected_width
            else:
                if h_layout.count():
                    v_layout.addLayout(h_layout)
                h_layout = _new_row_layout()
                h_layout.addWidget(button)
                current_width = button_width

        if h_layout.count():
            v_layout.addLayout(h_layout)

    def _create_tool_button(self, tool_name, description, module_name, entry_path, runtime_key, arguments):
        button = QPushButton(tool_name)
        button.setStyleSheet(TOOL_BUTTON_STYLE)
        button.setToolTip(description)
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        button.clicked.connect(
            partial(self.on_tool_button_clicked, module_name, entry_path, runtime_key, arguments)
        )
        return button

    def clear_tool_buttons(self):
        layout = self.ui.groupBox.layout()
        if layout is None or not isinstance(layout, QVBoxLayout):
            layout = QVBoxLayout()
            layout.setAlignment(Qt.AlignTop)
            self.ui.groupBox.setLayout(layout)

        while layout.count():
            child = layout.takeAt(0)
            if child.layout():
                while child.layout().count():
                    sub_child = child.layout().takeAt(0)
                    if sub_child.widget():
                        sub_child.widget().deleteLater()
            if child.widget():
                child.widget().deleteLater()

    def on_tool_button_clicked(self, module_name, entry_path, runtime_key, arguments):
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT directory FROM modules WHERE name = ?', (module_name,))
            module_row = c.fetchone()
            if not module_row:
                return
            module_dir = module_row[0]

        abs_entry_path = os.path.join(BASE_DIR, module_dir, entry_path)
        entry_file = os.path.basename(entry_path)
        command = self._build_command(runtime_key, entry_file, arguments, abs_entry_path)
        self._execute_command(command, runtime_key, abs_entry_path, BASE_DIR, entry_path)

    def _build_command(self, runtime_key, entry_file, arguments, abs_entry_path):
        # 按运行时类型拼装启动命令，动态解析 Python/Java 路径并补充参数
        runtime = runtime_key or ""
        base_runtime = runtime.split("_", 1)[0] if runtime else ""
        extra = (arguments or "").strip()

        def split_args(arg_string):
            if not arg_string:
                return []
            try:
                return shlex.split(arg_string, posix=False)
            except ValueError:
                return arg_string.split()

        def resolve_python_exec():
            python_path = (env.python3_path or "").strip()

            def _is_command(candidate):
                if not candidate:
                    return False
                if os.path.isabs(candidate):
                    return False
                return all(sep not in candidate for sep in ("/", "\\"))

            if _is_command(python_path):
                located = shutil.which(python_path)
                if located:
                    return located.replace('\\', '/')
                return python_path

            if python_path:
                python_path_norm = os.path.normpath(python_path)
                if os.path.isdir(python_path_norm):
                    candidate = os.path.join(python_path_norm, "python.exe")
                    if os.path.exists(candidate):
                        python_path_norm = candidate
                if python_path_norm and os.name == "nt" and not python_path_norm.lower().endswith(".exe"):
                    candidate = f"{python_path_norm}.exe"
                    if os.path.isfile(candidate):
                        python_path_norm = candidate
                if os.path.isfile(python_path_norm):
                    python_path = python_path_norm
                else:
                    python_path = ""

            if not python_path:
                for candidate in ("python", "python3"):
                    located = shutil.which(candidate)
                    if located:
                        return located.replace("\\", "/")

            return python_path.replace("\\", "/") if python_path else ""

        def resolve_java_exec():
            java_path = (getattr(env, f"{base_runtime}_path", "") or "").strip()

            def _is_command(candidate):
                if not candidate:
                    return False
                if os.path.isabs(candidate):
                    return False
                return all(sep not in candidate for sep in ("/", "\\"))

            if _is_command(java_path):
                located = shutil.which(java_path)
                if located:
                    return located.replace('\\', '/')
                return java_path

            if java_path:
                java_norm = os.path.normpath(java_path)
                if os.path.isdir(java_norm):
                    candidate = os.path.join(java_norm, "java.exe")
                    if os.path.isfile(candidate):
                        java_norm = candidate
                if java_norm and os.name == "nt" and not java_norm.lower().endswith(".exe"):
                    exe_candidate = f"{java_norm}.exe"
                    if os.path.isfile(exe_candidate):
                        java_norm = exe_candidate
                if os.path.isfile(java_norm):
                    java_path = java_norm
                else:
                    java_path = ""

            if not java_path:
                located = shutil.which("java")
                if located:
                    return located.replace("\\", "/")

            return java_path.replace("\\", "/") if java_path else ""

        extra_args = split_args(extra)

        if base_runtime.startswith("java"):
            java_exec = resolve_java_exec()
            if not java_exec:
                return []
            return [java_exec, *extra_args, "-jar", entry_file]
        if runtime == "python3_cli":
            python_exec = resolve_python_exec()
            if not python_exec:
                return []
            if entry_file.startswith("module|"):
                module_name = entry_file.split("|", 1)[1]
                return [python_exec, "-m", module_name, *extra_args]
            return [python_exec, entry_file, *extra_args]
        if runtime == "python3_module":
            python_exec = resolve_python_exec()
            if not python_exec:
                return []
            return [python_exec, "-m", entry_file, *extra_args]
        if base_runtime == "exe":
            return [abs_entry_path, *extra_args]
        if runtime == "file_folder":
            return [abs_entry_path]
        return []

    def _execute_command(self, command, runtime_key, abs_entry_path, base_dir, entry_path):
        # 根据运行模式执行命令或打开目录/浏览器，失败时弹窗提示
        if not command:
            return

        if runtime_key == "file_folder":
            target = command[0] if isinstance(command, (list, tuple)) and command else abs_entry_path
            try:
                os.startfile(target)
            except OSError:
                pass
            return

        if runtime_key.endswith("_browser"):
            target = command[0] if isinstance(command, (list, tuple)) and command else ""
            if target:
                webbrowser.open(target)
            return

        working_dir = os.path.dirname(abs_entry_path)

        def _resolve_exec_path(cmd):
            if not isinstance(cmd, (list, tuple)) or not cmd:
                return ""
            candidate = cmd[0]
            if not candidate:
                return ""
            if os.path.isabs(candidate):
                return candidate
            separators = (os.path.sep, os.path.altsep) if os.path.altsep else (os.path.sep,)
            if all(sep not in candidate for sep in separators):
                return ""
            return os.path.join(working_dir, candidate)

        if runtime_key.endswith("_gui"):
            exec_path = _resolve_exec_path(command)
            if exec_path and not os.path.exists(exec_path):
                self._show_execution_failure(f"未找到可执行文件\n{exec_path}")
                return
            subprocess.Popen(command, cwd=working_dir)
            return

        if runtime_key.endswith("_service"):
            exec_path = _resolve_exec_path(command)
            if exec_path and not os.path.exists(exec_path):
                self._show_execution_failure(f"未找到可执行文件\n{exec_path}")
                return
            subprocess.Popen(command, cwd=working_dir, creationflags=subprocess.CREATE_NO_WINDOW)
            return

        if isinstance(command, str):
            cmd_line = command
        else:
            cmd_line = subprocess.list2cmdline(command)

        if runtime_key.endswith("_module") or entry_path.startswith("module|"):
            working_dir = base_dir

        display_cmd = cmd_line.strip()
        if not display_cmd:
            return

        dir_for_cmd = working_dir.replace('"', '""')
        command_for_echo = self._escape_for_cmd_echo(display_cmd)
        launch = f'start cmd /K \"cd /d \"\"{dir_for_cmd}\"\" && echo {command_for_echo}\"'
        subprocess.Popen(launch, cwd=working_dir, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    @staticmethod
    def _escape_for_cmd_echo(command_text):
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

    def _show_execution_failure(self, message):
        QMessageBox.warning(self, "执行失败", message)

    def show_search_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Search Tools")
        dialog.setFixedSize(450, 350)
        dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)

        dialog.setStyleSheet(SEARCH_DIALOG_STYLE)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        search_input = self._create_search_input()
        layout.addWidget(search_input)
        result_list = self._create_result_list()
        layout.addWidget(result_list)

        search_input.setFocus()
        search_input.textChanged.connect(lambda text: self.perform_search(text, result_list))

        dialog.exec()

    def _create_search_input(self):
        search_input = QLineEdit()
        search_input.setPlaceholderText("请输入关键字...")
        search_input.setStyleSheet(SEARCH_INPUT_STYLE)
        return search_input

    def _create_result_list(self):
        result_list = QListWidget()
        result_list.setStyleSheet(SEARCH_RESULT_LIST_STYLE)
        return result_list

    def perform_search(self, text, result_list):
        result_list.clear()
        try:
            result_list.itemClicked.disconnect(self.on_search_result_clicked)
        except Exception:
            pass

        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(
                '''
                SELECT name, description
                FROM tools
                WHERE is_enabled = 1 AND (name LIKE ? OR description LIKE ?)
                ''',
                ('%' + text + '%', '%' + text + '%'),
            )
            tools = c.fetchall()

        for tool_name, description in tools:
            display_desc = description or ""
            item = QListWidgetItem(f"{tool_name} - {display_desc}")
            result_list.addItem(item)

        result_list.itemClicked.connect(self.on_search_result_clicked)

    def on_search_result_clicked(self, item):
        tool_name = item.text().split(" - ")[0]

        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(
                '''
                SELECT modules.name, tools.entry_path, tools.runtime_key, tools.arguments
                FROM tools
                JOIN modules ON tools.module_id = modules.id
                WHERE tools.name = ? AND tools.is_enabled = 1
                ''',
                (tool_name,),
            )
            tool_data = c.fetchone()

        if tool_data:
            module_name, entry_path, runtime_key, arguments = tool_data
            self.on_tool_button_clicked(module_name, entry_path, runtime_key, arguments)

        sender = self.sender()
        if sender is not None and sender.parent():
            sender.parent().close()


def main():
    # 仅在 Windows 上启动应用，启动前确保数据库与目录准备完毕
    if sys.platform != "win32":
        print("This application only runs on Windows.")
        sys.exit(1)

    check_and_init_db()
    create_module_directories()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


__all__ = ["MainWindow", "check_and_init_db", "create_module_directories"]
