"""
# -*- coding: utf-8 -*-
# @Author: dr0n1
# @Version: v3.111.0
# @Link: https://www.dr0n.top/
# @Last Update: 2026/5/12
"""

import os
import shutil
import sqlite3
import subprocess
import sys
import webbrowser
from collections.abc import Sequence
from functools import partial

from PySide6.QtCore import QDateTime, QEvent, QPoint, Qt, QTimer
from PySide6.QtGui import QColor, QIcon, QPainter, QPainterPath, QPen, QShortcut
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

from db import (
    DB_PATH,
    create_db,
    restore_database_defaults as db_restore_database_defaults,
    show_database_dialog,
    upgrade_db,
)
from env import env, show_env_dialog
from runtime_utils import (
    escape_cmd_echo,
    resolve_configured_executable,
    resolve_relative_executable,
    split_command_arguments,
)
from styles import (
    CUSTOM_TOOLTIP_STYLE,
    DIALOG_BUTTON_PRIMARY_STYLE,
    DIALOG_BUTTON_SECONDARY_STYLE,
    DIALOG_LABEL_DESC_TEXT_STYLE,
    DIALOG_LABEL_DESC_TITLE_STYLE,
    DIALOG_LABEL_INFO_STYLE,
    DIALOG_LABEL_TITLE_STYLE,
    DIALOG_LABEL_VERSION_STYLE,
    DIALOG_STYLE,
    GROUPBOX_STYLE,
    LISTWIDGET_STYLE,
    LIST_CONTAINER_STYLE,
    MAIN_WINDOW_STYLE,
    SEARCH_DIALOG_STYLE,
    SEARCH_INPUT_STYLE,
    SEARCH_RESULT_LIST_STYLE,
    STATUS_BAR_STYLE,
    TOOL_BUTTON_STYLE,
)
from styles.ui_main import Ui_MainWindow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Command = list[str]
ToolRow = tuple[str, str | None, str, str | None, str | None]


class RoundedToolTip(QFrame):
    """Custom tooltip frame with rounded corners and no transparent halo."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent, Qt.ToolTip | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setObjectName("RoundedToolTip")
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAutoFillBackground(False)

        self._bg_color = QColor("#ffffff")
        self._border_color = QColor("#dbeafe")
        self._radius = 10
        self._content_margin = 0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            self._content_margin,
            self._content_margin,
            self._content_margin,
            self._content_margin,
        )
        self._label = QLabel(self)
        self._label.setWordWrap(True)
        self._label.setMaximumWidth(360)
        layout.addWidget(self._label)

    def paintEvent(self, event: object) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        inner = self.rect().adjusted(0, 0, -1, -1)

        path = QPainterPath()
        path.addRoundedRect(inner, self._radius, self._radius)
        painter.fillPath(path, self._bg_color)
        pen = QPen(self._border_color)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawPath(path)

    def show_text(self, text: str, global_pos: QPoint) -> None:
        """Render tooltip text near the global cursor position."""
        if not text:
            self.hide()
            return
        self._label.setText(text)
        self.adjustSize()
        offset = QPoint(12, 16)
        self.move(global_pos + offset)
        self.show()
        self.raise_()


def check_and_init_db() -> None:
    """Ensure the database file exists, is structurally valid, and is upgraded."""
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


def create_module_directories() -> None:
    """Create local module directories listed in the database."""
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
    """Main application window for browsing and launching configured tools."""

    def __init__(self) -> None:
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

    def _setup_main_styles(self) -> None:
        app = QApplication.instance()
        if app is not None:
            app.setStyleSheet(MAIN_WINDOW_STYLE)
        else:
            self.setStyleSheet(MAIN_WINDOW_STYLE)

    def _setup_widget_styles(self) -> None:
        self.ui.groupBox.setStyleSheet(GROUPBOX_STYLE)
        self.ui.listWidget.setStyleSheet(LISTWIDGET_STYLE)
        self.ui.listWidget.setAttribute(Qt.WA_StyledBackground, True)
        self.ui.listWidget.setAutoFillBackground(False)
        if self.ui.listWidget.viewport() is not None:
            self.ui.listWidget.viewport().setAutoFillBackground(False)
        self.ui.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.listWidget.setSpacing(4)
        self.ui.listWidget.setContentsMargins(8, 8, 8, 8)
        self.ui.listWidget.setTextElideMode(Qt.ElideNone)
        self.ui.listWidget.setWordWrap(False)

    def _setup_tooltip(self) -> None:
        self._tooltip = RoundedToolTip(self)
        self._tooltip.setStyleSheet(CUSTOM_TOOLTIP_STYLE)

    def _setup_fonts(self) -> None:
        font = self.ui.listWidget.font()
        font.setPointSize(11)
        font.setBold(True)
        self.ui.listWidget.setFont(font)

    def _setup_window_icon(self) -> None:
        icon_path = os.path.abspath(os.path.join(BASE_DIR, 'styles', 'logo.png'))
        self.setWindowIcon(QIcon(icon_path))

    def _bind_events(self) -> None:
        if self.ui.action_about not in self.ui.menu_4.actions():
            self.ui.menu_4.addAction(self.ui.action_about)
        self.ui.listWidget.itemClicked.connect(self.on_module_clicked)
        self.ui.action_about.triggered.connect(self.show_about_toolbox)
        self.ui.action_env.triggered.connect(self.env)
        self.ui.action_database.triggered.connect(self.database)

    def _initialize_data(self) -> None:
        self.load_modules()
        self.load_config_env()
        if self.ui.listWidget.count() > 0:
            first_item = self.ui.listWidget.item(0)
            self.ui.listWidget.setCurrentItem(first_item)
            self.on_module_clicked(first_item)

    def _setup_status_bar(self) -> None:
        self.statusBar().showMessage("⌛...")
        self.statusBar().setStyleSheet("QStatusBar::item {border: none;}")
        self.copyright_label = QLabel("⌛...")
        self.statusBar().addWidget(self.copyright_label, 1)
        self.time_label = QLabel()
        self.statusBar().addPermanentWidget(self.time_label)

    def _update_status_bar_style(self) -> None:
        self.statusBar().setStyleSheet(STATUS_BAR_STYLE)

    def _setup_timer(self) -> None:
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.update_time()

    def _setup_layout(self) -> None:
        self.ui.groupBox.setContentsMargins(10, 10, 10, 10)
        self.ui.groupBox.setMaximumHeight(16777215)
        self.ui.listWidget.setMaximumHeight(16777215)
        if self.ui.centralwidget.layout() is None:
            layout = QHBoxLayout(self.ui.centralwidget)
            layout.setContentsMargins(12, 18, 12, 18)
            layout.setSpacing(16)
            self._list_container = QWidget(self.ui.centralwidget)
            self._list_container.setObjectName("listContainer")
            self._list_container.setAttribute(Qt.WA_StyledBackground, True)
            inner_layout = QVBoxLayout(self._list_container)
            inner_layout.setContentsMargins(0, 0, 0, 0)
            inner_layout.setSpacing(0)
            self.ui.listWidget.setParent(self._list_container)
            self.ui.listWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            inner_layout.addWidget(self.ui.listWidget, 1, Qt.AlignHCenter)
            self._list_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            self._list_container.setMaximumWidth(16777215)
            self._list_container.setMinimumWidth(self.ui.listWidget.sizeHint().width() + 16)
            self._list_container.setStyleSheet(LIST_CONTAINER_STYLE)
            self.ui.groupBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            layout.addWidget(self._list_container)
            layout.addWidget(self.ui.groupBox, 1)
        else:
            self.ui.centralwidget.layout().setContentsMargins(12, 18, 12, 18)
            self.ui.centralwidget.layout().setSpacing(16)
            if hasattr(self, "_list_container"):
                self._list_container.setStyleSheet(LIST_CONTAINER_STYLE)
        self._resize_panels()
        self._adjust_list_width()

    def _setup_shortcuts(self) -> None:
        self._search_shortcut = QShortcut("Ctrl+F", self)
        self._search_shortcut.activated.connect(self.show_search_dialog)

        app = QApplication.instance()
        if app is not None:
            app.installEventFilter(self)

    def update_time(self) -> None:
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.time_label.setText(current_time)

    def resizeEvent(self, event: object) -> None:
        super().resizeEvent(event)
        self._resize_panels()

    def _resize_panels(self) -> None:
        layout = self.ui.centralwidget.layout()
        if layout is not None:
            layout.setContentsMargins(10, 20, 10, 20)
            return

    def _configure_menus(self) -> None:
        for menu in self.menuBar().findChildren(QMenu):
            self._prepare_menu(menu)

    def _prepare_menu(self, menu: QMenu) -> None:
        if menu.property("_polished_menu"):
            return
        menu.setProperty("_polished_menu", True)
        self._apply_menu_flags(menu)
        menu.aboutToShow.connect(lambda m=menu: self._on_menu_about_to_show(m))

    def _apply_menu_flags(self, menu: QMenu) -> None:
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

    def _on_menu_about_to_show(self, menu: QMenu) -> None:
        self._apply_menu_flags(menu)
        for sub_menu in menu.findChildren(QMenu):
            self._prepare_menu(sub_menu)

    def show_about_toolbox(self) -> None:
        self._show_about_dialog()

    def _show_about_dialog(self) -> None:
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

    def _create_title_section(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(10)

        title_label = QLabel("关于工具箱")
        title_label.setStyleSheet(DIALOG_LABEL_TITLE_STYLE)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        version_label = QLabel("Version 3")
        version_label.setStyleSheet(DIALOG_LABEL_VERSION_STYLE)
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)

        return layout

    def _create_content_section(self) -> QVBoxLayout:
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

    def _create_button_section(self, dialog: QDialog) -> QHBoxLayout:
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

    def database(self) -> None:
        show_database_dialog(self)
        self.load_modules()

    def refresh_database(self) -> None:
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

    def restore_database_defaults(self) -> None:
        db_restore_database_defaults(
            self,
            self.refresh_database,
            getattr(self, "_db_dialog_refresh", None),
        )

    def eventFilter(self, obj: object, event: object) -> bool:
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

    def env(self) -> None:
        show_env_dialog(self, env)
        self.load_config_env()

    def load_modules(self) -> None:
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

    def _adjust_list_width(self) -> None:
        count = self.ui.listWidget.count()
        if count == 0:
            return
        fm = self.ui.listWidget.fontMetrics()
        max_text_width = max(fm.horizontalAdvance(self.ui.listWidget.item(i).text()) for i in range(count))
        list_width = max(max_text_width + 64, 180)
        self.ui.listWidget.setMinimumWidth(list_width)
        self.ui.listWidget.setMaximumWidth(list_width)

        if hasattr(self, "_list_container"):
            container_width = list_width + 28  # container padding 14*2
            self._list_container.setMinimumWidth(container_width)
            self._list_container.setMaximumWidth(container_width)

    def load_config_env(self) -> None:
        """Load runtime configuration from the database into the shared env object."""
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
            else:
                if shutil.which("java"):
                    env.java8_path = "java"
                    env.java11_path = "java"
                else:
                    env.java8_path = ""
                    env.java11_path = ""
        except Exception:
            pass

    def on_module_clicked(self, item: QListWidgetItem) -> None:
        """Refresh tool buttons for the selected module."""
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

    def _create_tool_buttons(
        self,
        tools: Sequence[ToolRow],
        module_name: str,
    ) -> None:
        """Create responsive rows of tool buttons for a module."""
        v_layout = self.ui.groupBox.layout()
        if v_layout is None or not isinstance(v_layout, QVBoxLayout):
            v_layout = QVBoxLayout()
            v_layout.setAlignment(Qt.AlignTop)
            v_layout.setSpacing(15)
            v_layout.setContentsMargins(0, 0, 0, 0)
            self.ui.groupBox.setLayout(v_layout)

        def _new_row_layout() -> QHBoxLayout:
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

    def _create_tool_button(
        self,
        tool_name: str,
        description: str,
        module_name: str,
        entry_path: str,
        runtime_key: str | None,
        arguments: str | None,
    ) -> QPushButton:
        button = QPushButton(tool_name)
        button.setStyleSheet(TOOL_BUTTON_STYLE)
        button.setToolTip(description)
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        button.clicked.connect(
            partial(self.on_tool_button_clicked, module_name, entry_path, runtime_key, arguments)
        )
        return button

    def clear_tool_buttons(self) -> None:
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

    def on_tool_button_clicked(
        self,
        module_name: str,
        entry_path: str,
        runtime_key: str | None,
        arguments: str | None,
    ) -> None:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT directory FROM modules WHERE name = ?', (module_name,))
            module_row = c.fetchone()
            if not module_row:
                self._show_execution_failure(f"未找到工具所属模块\n{module_name}")
                return
            module_dir = module_row[0]

        abs_entry_path = os.path.join(BASE_DIR, module_dir, entry_path)
        if not self._validate_tool_target(runtime_key, entry_path, abs_entry_path):
            return

        entry_file = os.path.basename(entry_path)
        command = self._build_command(runtime_key, entry_file, arguments, abs_entry_path)
        self._execute_command(command, runtime_key, abs_entry_path, BASE_DIR, entry_path)

    def _validate_tool_target(
        self,
        runtime_key: str | None,
        entry_path: str,
        abs_entry_path: str,
    ) -> bool:
        """Validate the local tool path before launching."""
        runtime = runtime_key or ""
        if runtime.endswith("_browser") or entry_path.startswith("module|"):
            return True
        if runtime.endswith("_module"):
            return True

        if runtime == "file_folder":
            if os.path.exists(abs_entry_path):
                return True
            self._show_execution_failure(f"工具路径不存在\n{abs_entry_path}")
            return False

        working_dir = os.path.dirname(abs_entry_path)
        if os.path.isdir(working_dir):
            return True

        self._show_execution_failure(f"工具目录不存在\n{working_dir}")
        return False

    def _build_command(
        self,
        runtime_key: str | None,
        entry_file: str,
        arguments: str | None,
        abs_entry_path: str,
    ) -> Command:
        """Build the launch command for a configured runtime."""
        runtime = runtime_key or ""
        base_runtime = runtime.split("_", 1)[0] if runtime else ""
        extra = (arguments or "").strip()
        extra_args = split_command_arguments(extra)

        if base_runtime.startswith("java"):
            java_exec = resolve_configured_executable(
                getattr(env, f"{base_runtime}_path", ""),
                "java.exe",
                ("java",),
            )
            if not java_exec:
                return []
            return [java_exec, *extra_args, "-jar", entry_file]
        if runtime == "python3_cli":
            python_exec = resolve_configured_executable(
                env.python3_path,
                "python.exe",
                ("python", "python3"),
            )
            if not python_exec:
                return []
            if entry_file.startswith("module|"):
                module_name = entry_file.split("|", 1)[1]
                return [python_exec, "-m", module_name, *extra_args]
            return [python_exec, entry_file, *extra_args]
        if runtime == "python3_module":
            python_exec = resolve_configured_executable(
                env.python3_path,
                "python.exe",
                ("python", "python3"),
            )
            if not python_exec:
                return []
            return [python_exec, "-m", entry_file, *extra_args]
        if base_runtime == "exe":
            return [abs_entry_path, *extra_args]
        if runtime == "file_folder":
            return [abs_entry_path]
        return []

    def _execute_command(
        self,
        command: Command,
        runtime_key: str | None,
        abs_entry_path: str,
        base_dir: str,
        entry_path: str,
    ) -> None:
        """Execute or display the command according to its runtime mode."""
        if not command:
            return

        runtime = runtime_key or ""

        if runtime == "file_folder":
            target = command[0] if command else abs_entry_path
            try:
                os.startfile(target)
            except OSError as exc:
                self._show_execution_failure(f"工具路径打开失败\n{target}\n{exc}")
            return

        if runtime.endswith("_browser"):
            target = command[0] if command else ""
            if target:
                webbrowser.open(target)
            return

        working_dir = os.path.dirname(abs_entry_path)

        if runtime.endswith("_gui"):
            exec_path = resolve_relative_executable(command, working_dir)
            if exec_path and not os.path.exists(exec_path):
                self._show_execution_failure(f"未找到可执行文件\n{exec_path}")
                return
            subprocess.Popen(command, cwd=working_dir)
            return

        if runtime.endswith("_service"):
            exec_path = resolve_relative_executable(command, working_dir)
            if exec_path and not os.path.exists(exec_path):
                self._show_execution_failure(f"未找到可执行文件\n{exec_path}")
                return
            subprocess.Popen(command, cwd=working_dir, creationflags=subprocess.CREATE_NO_WINDOW)
            return

        if isinstance(command, str):
            cmd_line = command
        else:
            cmd_line = subprocess.list2cmdline(command)

        if runtime.endswith("_module") or entry_path.startswith("module|"):
            working_dir = base_dir

        display_cmd = cmd_line.strip()
        if not display_cmd:
            return

        dir_for_cmd = working_dir.replace('"', '""')
        command_for_echo = escape_cmd_echo(display_cmd)
        launch = f'start cmd /K \"cd /d \"\"{dir_for_cmd}\"\" && echo {command_for_echo}\"'
        subprocess.Popen(launch, cwd=working_dir, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def _show_execution_failure(self, message: str) -> None:
        QMessageBox.warning(self, "执行失败", message)

    def show_search_dialog(self) -> None:
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

    def _create_search_input(self) -> QLineEdit:
        search_input = QLineEdit()
        search_input.setPlaceholderText("请输入关键字...")
        search_input.setStyleSheet(SEARCH_INPUT_STYLE)
        return search_input

    def _create_result_list(self) -> QListWidget:
        result_list = QListWidget()
        result_list.setStyleSheet(SEARCH_RESULT_LIST_STYLE)
        return result_list

    def perform_search(self, text: str, result_list: QListWidget) -> None:
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

    def on_search_result_clicked(self, item: QListWidgetItem) -> None:
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


def main() -> None:
    """Start the Windows desktop application."""
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
