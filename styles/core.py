"""Centralized PySide6 stylesheet exports."""

from collections.abc import Iterable
from pathlib import Path


STYLE_DIR = Path(__file__).resolve().parent
BLUE_BORDER = "#bfdbfe"
BLUE_TEXT = "#1d4ed8"
DEFAULT_TEXT = "#1f2937"
PRIMARY_BLUE = "#2563eb"


def _load_qss(name: str) -> str:
    """Load a QSS file next to this module."""
    return (STYLE_DIR / name).read_text(encoding="utf-8").strip()


def _compose(*parts: str) -> str:
    """Join stylesheet fragments while preserving selector order."""
    return "\n\n".join(part.strip() for part in parts if part and part.strip())


def vertical_gradient(start: str, end: str) -> str:
    """Return a vertical Qt gradient string."""
    return f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {start}, stop:1 {end})"


def dialog_background_style(
    *,
    selector: str = "QDialog",
    start: str = "#f8fafc",
    end: str = "#e2e8f0",
    border_radius: int | None = None,
) -> str:
    """Build a dialog background override appended after base.qss."""
    lines = [
        f"{selector} {{",
        f"    background: {vertical_gradient(start, end)};",
    ]
    if border_radius is not None:
        lines.append(f"    border-radius: {border_radius}px;")
    lines.append("}")
    return "\n".join(lines)


def button_style(
    *,
    padding: str,
    font_size: int,
    font_weight: int,
    border: str,
    border_radius: int,
    background: str,
    color: str,
    hover_background: str,
    hover_border: str | None = None,
    hover_color: str | None = None,
    pressed_background: str | None = None,
    pressed_border: str | None = None,
    pressed_color: str | None = None,
    disabled: bool = False,
    margin: str | None = None,
    min_width: str | None = None,
    min_height: str | None = None,
) -> str:
    """Build a QPushButton stylesheet with shared interaction states."""
    lines = [
        "QPushButton {",
        f"    padding: {padding};",
        f"    font-size: {font_size}px;",
        f"    font-weight: {font_weight};",
        f"    border: {border};",
        f"    border-radius: {border_radius}px;",
        f"    background: {background};",
        f"    color: {color};",
    ]
    if margin is not None:
        lines.insert(2, f"    margin: {margin};")
    if min_width is not None:
        lines.append(f"    min-width: {min_width};")
    if min_height is not None:
        lines.append(f"    min-height: {min_height};")
    lines.extend(
        [
            "}",
            "QPushButton:hover {",
            f"    background: {hover_background};",
        ]
    )
    if hover_border is not None:
        lines.append(f"    border: {hover_border};")
    if hover_color is not None:
        lines.append(f"    color: {hover_color};")
    lines.append("}")

    if pressed_background is not None:
        lines.extend(
            [
                "QPushButton:pressed {",
                f"    background: {pressed_background};",
            ]
        )
        if pressed_border is not None:
            lines.append(f"    border: {pressed_border};")
        if pressed_color is not None:
            lines.append(f"    color: {pressed_color};")
        lines.append("}")

    if disabled:
        lines.extend(
            [
                "QPushButton:disabled {",
                "    background: #e2e8f0;",
                "    color: #94a3b8;",
                "    border: 1px solid #cbd5e1;",
                "}",
            ]
        )

    lines.extend(
        [
            "QPushButton:focus {",
            "    outline: none;",
            "}",
        ]
    )
    return "\n".join(lines)


BASE_QSS = _load_qss("base.qss")

BUTTON_STYLE = button_style(
    padding="12px 20px",
    font_size=13,
    font_weight=600,
    border=f"1px solid {BLUE_BORDER}",
    border_radius=10,
    background=vertical_gradient("#f8fbff", "#e0f2ff"),
    color=DEFAULT_TEXT,
    hover_background=vertical_gradient("#eff6ff", "#dbeafe"),
    hover_border=f"1px solid {PRIMARY_BLUE}",
    hover_color=BLUE_TEXT,
    pressed_background=PRIMARY_BLUE,
    pressed_border=f"1px solid {BLUE_TEXT}",
    pressed_color="#f8fafc",
    disabled=True,
    min_height="20px",
)

TOOL_BUTTON_STYLE = button_style(
    padding="12px 20px",
    font_size=13,
    font_weight=600,
    border=f"1px solid {BLUE_BORDER}",
    border_radius=12,
    background=vertical_gradient("#f8fbff", "#e0f2ff"),
    color=DEFAULT_TEXT,
    hover_background=vertical_gradient("#eff6ff", "#dbeafe"),
    hover_border=f"1px solid {PRIMARY_BLUE}",
    hover_color=BLUE_TEXT,
    pressed_background=PRIMARY_BLUE,
    pressed_border=f"1px solid {BLUE_TEXT}",
    pressed_color="#f8fafc",
    disabled=True,
    margin="4px",
)

RESTORE_BUTTON_STYLE = button_style(
    padding="12px 20px",
    font_size=13,
    font_weight=600,
    border="1px solid #f97316",
    border_radius=10,
    background=vertical_gradient("#fdba74", "#f97316"),
    color="white",
    hover_background=vertical_gradient("#f97316", "#ea580c"),
    hover_border="1px solid #ea580c",
    pressed_background="#c2410c",
    pressed_border="1px solid #c2410c",
    min_height="20px",
)

DIALOG_BUTTON_PRIMARY_STYLE = button_style(
    padding="12px 20px",
    font_size=13,
    font_weight=500,
    border="1px solid #3b82f6",
    border_radius=8,
    background=vertical_gradient("#3b82f6", PRIMARY_BLUE),
    color="white",
    hover_background=vertical_gradient(PRIMARY_BLUE, BLUE_TEXT),
    hover_border=f"1px solid {BLUE_TEXT}",
    pressed_background=vertical_gradient(BLUE_TEXT, "#1e40af"),
    min_width="100px",
)

DIALOG_BUTTON_SECONDARY_STYLE = button_style(
    padding="12px 20px",
    font_size=13,
    font_weight=500,
    border="1px solid #d1d5db",
    border_radius=8,
    background=vertical_gradient("#ffffff", "#f8fafc"),
    color="#374151",
    hover_background=vertical_gradient("#f0f9ff", "#e0f2fe"),
    hover_border="1px solid #3b82f6",
    hover_color="#1e40af",
    pressed_background=vertical_gradient("#e0f2fe", "#bae6fd"),
    min_width="100px",
)

ENV_BUTTON_STYLE = button_style(
    padding="10px 16px",
    font_size=12,
    font_weight=500,
    border=f"1px solid {BLUE_BORDER}",
    border_radius=10,
    background=vertical_gradient("#f8fbff", "#e0f2ff"),
    color=DEFAULT_TEXT,
    hover_background=vertical_gradient("#eff6ff", "#dbeafe"),
    hover_border=f"1px solid {PRIMARY_BLUE}",
    hover_color=BLUE_TEXT,
    pressed_background=PRIMARY_BLUE,
    pressed_border=f"1px solid {BLUE_TEXT}",
    pressed_color="#f8fafc",
)

ENV_SAVE_BUTTON_STYLE = button_style(
    padding="12px 24px",
    font_size=13,
    font_weight=600,
    border="none",
    border_radius=10,
    background=vertical_gradient("#10b981", "#059669"),
    color="white",
    hover_background=vertical_gradient("#059669", "#047857"),
    pressed_background=vertical_gradient("#047857", "#065f46"),
    min_width="80px",
)

ENV_CANCEL_BUTTON_STYLE = button_style(
    padding="12px 24px",
    font_size=13,
    font_weight=600,
    border=f"1px solid {BLUE_BORDER}",
    border_radius=10,
    background=vertical_gradient("#f8fbff", "#e0f2ff"),
    color=DEFAULT_TEXT,
    hover_background=vertical_gradient("#eff6ff", "#dbeafe"),
    hover_border=f"1px solid {PRIMARY_BLUE}",
    hover_color=BLUE_TEXT,
    pressed_background=PRIMARY_BLUE,
    pressed_border=f"1px solid {BLUE_TEXT}",
    pressed_color="#f8fafc",
    min_width="80px",
)

MAIN_WINDOW_STYLE = _compose(
    BASE_QSS,
    """
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #f5f7ff, stop:1 #eef2ff);
    }
    QMenuBar {
        background: #f8fafc;
        border-bottom: 1px solid #dbeafe;
        padding: 6px 12px;
        color: #1f2937;
    }
    QMenuBar::item {
        padding: 6px 14px;
        border-radius: 6px;
        margin: 0 4px;
    }
    QMenuBar::item:selected {
        background: #2563eb;
        color: #f8fafc;
    }
    QMenu {
        background-color: #ffffff;
        border: 1px solid #dbeafe;
        border-radius: 10px;
        padding: 6px;
        margin: 0px;
        color: #1f2937;
    }
    QWidget#qt_menu_shadow {
        border-radius: 12px;
        background-color: transparent;
        border: none;
        border-image: none;
    }
    QMenu::item {
        padding: 8px 16px;
        border-radius: 6px;
        margin: 2px 0;
    }
    QMenu::item:selected {
        background: #e0f2fe;
        color: #1d4ed8;
    }
    """,
)

GROUPBOX_STYLE = """
QGroupBox {
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid #dbeafe;
    border-radius: 14px;
    margin: 8px;
    padding: 18px;
    font-weight: 600;
}
"""

LISTWIDGET_STYLE = """
QListWidget {
    background: transparent;
    border: none;
    border-radius: 14px;
    padding: 12px;
    margin: 0px;
    font-size: 13px;
    font-weight: 600;
    color: #0f172a;
    outline: none;
}
QListWidget::viewport {
    background: transparent;
    border: none;
    border-radius: 14px;
}
QListWidget::item {
    padding: 12px 14px;
    margin: 6px 0;
    border-radius: 10px;
    background: transparent;
}
QListWidget::item:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #f0f7ff, stop:1 #e5efff);
    border: 1px solid #bfdbfe;
    color: #1d4ed8;
}
QListWidget::item:selected {
    background: #2563eb;
    color: #f8fafc;
    border: 1px solid #1d4ed8;
}
QScrollBar:vertical {
    width: 0px;
    background: transparent;
    margin: 0;
}
QScrollBar::handle:vertical {
    min-height: 0;
    background: transparent;
}
"""

LIST_CONTAINER_STYLE = """
#listContainer {
    background: rgba(255, 255, 255, 0.94);
    border: 1px solid #dbeafe;
    border-radius: 14px;
    padding: 14px;
    margin: 8px;
}
"""

CUSTOM_TOOLTIP_STYLE = """
QFrame#RoundedToolTip {
    background: transparent;
    border: none;
}
QFrame#RoundedToolTip QLabel {
    color: #1e293b;
    padding: 6px 10px;
    font-size: 12px;
    background: transparent;
}
"""

STATUS_BAR_STYLE = """
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

DIALOG_STYLE = dialog_background_style(border_radius=16)

DIALOG_LABEL_TITLE_STYLE = """
QLabel {
    font-size: 24px;
    font-weight: bold;
    color: #1e293b;
    background: transparent;
    border: none;
    padding: 10px;
}
"""

DIALOG_LABEL_VERSION_STYLE = """
QLabel {
    font-size: 16px;
    font-weight: 500;
    color: #64748b;
    background: transparent;
    border: none;
    padding: 5px;
}
"""

DIALOG_LABEL_INFO_STYLE = """
QLabel {
    font-size: 14px;
    font-weight: 500;
    color: #374151;
    background: rgba(255, 255, 255, 0.8);
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 12px 16px;
}
"""

DIALOG_LABEL_DESC_TITLE_STYLE = """
QLabel {
    font-size: 14px;
    font-weight: 600;
    color: #1e293b;
    background: transparent;
    border: none;
    padding: 8px 0px;
}
"""

DIALOG_LABEL_DESC_TEXT_STYLE = """
QLabel {
    font-size: 13px;
    color: #64748b;
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 16px;
    line-height: 1.5;
}
"""

SEARCH_DIALOG_STYLE = dialog_background_style(border_radius=12)

SEARCH_INPUT_STYLE = """
QLineEdit {
    padding: 12px 16px;
    font-size: 14px;
    border: 2px solid #e2e8f0;
    border-radius: 10px;
    background: white;
    color: #374151;
}
QLineEdit:focus {
    border: 2px solid #3b82f6;
    background: #f8fafc;
}
"""

SEARCH_RESULT_LIST_STYLE = """
QListWidget {
    font-size: 13px;
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 8px;
}
QListWidget::item {
    padding: 10px 12px;
    margin: 2px;
    border-radius: 6px;
    background: transparent;
}
QListWidget::item:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #f0f9ff, stop:1 #e0f2fe);
    border: 1px solid #bae6fd;
}
QListWidget::item:selected {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3b82f6, stop:1 #2563eb);
    color: white;
}
"""

DB_DIALOG_STYLE = dialog_background_style(start="#f5f7ff", end="#eef2ff")

TAB_WIDGET_STYLE = """
QTabWidget::pane {
    border: 1px solid #dbeafe;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.96);
}
QTabBar::tab {
    background: #f1f5f9;
    border: 1px solid #cbd5f5;
    padding: 10px 20px;
    margin: 0 2px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    font-weight: 600;
    color: #1f2937;
}
QTabBar::tab:selected {
    background: #2563eb;
    color: #f8fafc;
    border: 1px solid #1d4ed8;
}
QTabBar::tab:hover:!selected {
    background: #e0f2ff;
    color: #1d4ed8;
}
"""

TABLE_WIDGET_STYLE = """
QTableWidget {
    font-size: 14px;
    background: rgba(255, 255, 255, 0.96);
    border: 1px solid #dbeafe;
    border-radius: 10px;
    gridline-color: #e2e8f0;
    selection-background-color: transparent;
    selection-color: #1f2937;
    outline: none;
}
QTableWidget::item {
    padding: 0px;
    border: none;
    border-bottom: 1px solid #e2e8f0;
    min-height: 30px;
    color: #1f2937;
    background: transparent;
}
QTableWidget::item:selected {
    background: #2563eb;
    color: #f8fafc;
    border: 1px solid #1d4ed8;
    outline: none;
}
QTableWidget::item:focus {
    border: none;
    background: transparent;
    color: #1f2937;
}
QTableWidget::item:focus:selected,
QTableWidget::item:!focus:selected {
    border: 1px solid #1d4ed8;
    background: #2563eb;
    color: #f8fafc;
}
QTableWidget QLineEdit {
    background: #ffffff;
    border: 2px solid #2563eb;
    border-radius: 6px;
    padding: 4px 8px;
}
QHeaderView::section {
    background: #f5f7ff;
    border: 1px solid #dbeafe;
    padding: 14px;
    font-weight: 600;
    color: #1f2937;
    font-size: 14px;
    min-height: 40px;
}
"""

ENV_DIALOG_STYLE = dialog_background_style()

ENV_GROUPBOX_STYLE = """
QGroupBox {
    background: rgba(255, 255, 255, 0.9);
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    margin: 8px;
    padding: 16px;
    font-weight: 600;
    font-size: 14px;
    color: #374151;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    background: white;
}
"""

ENV_RADIO_BUTTON_STYLE = """
QRadioButton {
    font-size: 13px;
    font-weight: 500;
    color: #1f2937;
    spacing: 8px;
}
QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border-radius: 9px;
    border: 2px solid #cbd5f5;
    background: white;
}
QRadioButton::indicator:checked {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #2563eb, stop:1 #1d4ed8);
    border: 2px solid #1d4ed8;
}
"""

ENV_LINE_EDIT_STYLE = """
QLineEdit {
    padding: 10px 12px;
    font-size: 12px;
    border: 1px solid #cbd5f5;
    border-radius: 10px;
    background: #f8fafc;
    color: #1f2937;
}
"""

ENV_STATUS_LABEL_STYLE = """
QLabel {
    padding: 12px 16px;
    color: #1f2937;
    background: rgba(248, 250, 252, 0.85);
    border: 1px solid #dbeafe;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 500;
}
"""

MESSAGE_BOX_STYLE = """
    QMessageBox {
        background-color: #ffffff;
        color: #1f2937;
    }
    QMessageBox QLabel {
        color: #1f2937;
        font-size: 13px;
    }
    QMessageBox QPushButton {
        padding: 8px 18px;
        font-size: 12px;
        font-weight: 600;
        border-radius: 8px;
        border: 1px solid #bfdbfe;
        background-color: #f8fbff;
        color: #1f2937;
        min-width: 70px;
    }
    QMessageBox QPushButton:hover {
        background-color: #e0f2ff;
        border: 1px solid #2563eb;
        color: #1d4ed8;
    }
    QMessageBox QPushButton:pressed {
        background-color: #2563eb;
        border: 1px solid #1d4ed8;
        color: #f8fafc;
    }
"""


def apply_stylesheet(widget: object | None, style: str) -> None:
    """Apply a single stylesheet to a widget if it exists."""
    if widget is not None:
        widget.setStyleSheet(style)


def apply_stylesheets(widgets: Iterable[object | None], style: str) -> None:
    """Apply the same stylesheet to a collection of widgets."""
    for widget in widgets:
        if widget is None:
            continue
        apply_stylesheet(widget, style)


def clear_stylesheet(widget: object | None) -> None:
    """Clear a widget stylesheet if the widget exists."""
    if widget is not None:
        widget.setStyleSheet("")


def style_message_box(box: object) -> None:
    """Apply the shared QMessageBox stylesheet."""
    box.setStyleSheet(MESSAGE_BOX_STYLE)


__all__ = [
    "BASE_QSS",
    "BUTTON_STYLE",
    "CUSTOM_TOOLTIP_STYLE",
    "DB_DIALOG_STYLE",
    "DIALOG_BUTTON_PRIMARY_STYLE",
    "DIALOG_BUTTON_SECONDARY_STYLE",
    "DIALOG_LABEL_DESC_TEXT_STYLE",
    "DIALOG_LABEL_DESC_TITLE_STYLE",
    "DIALOG_LABEL_INFO_STYLE",
    "DIALOG_LABEL_TITLE_STYLE",
    "DIALOG_LABEL_VERSION_STYLE",
    "DIALOG_STYLE",
    "ENV_BUTTON_STYLE",
    "ENV_CANCEL_BUTTON_STYLE",
    "ENV_DIALOG_STYLE",
    "ENV_GROUPBOX_STYLE",
    "ENV_LINE_EDIT_STYLE",
    "ENV_RADIO_BUTTON_STYLE",
    "ENV_SAVE_BUTTON_STYLE",
    "ENV_STATUS_LABEL_STYLE",
    "GROUPBOX_STYLE",
    "LISTWIDGET_STYLE",
    "LIST_CONTAINER_STYLE",
    "MAIN_WINDOW_STYLE",
    "MESSAGE_BOX_STYLE",
    "RESTORE_BUTTON_STYLE",
    "SEARCH_DIALOG_STYLE",
    "SEARCH_INPUT_STYLE",
    "SEARCH_RESULT_LIST_STYLE",
    "STATUS_BAR_STYLE",
    "TABLE_WIDGET_STYLE",
    "TAB_WIDGET_STYLE",
    "TOOL_BUTTON_STYLE",
    "apply_stylesheet",
    "apply_stylesheets",
    "clear_stylesheet",
    "style_message_box",
]
