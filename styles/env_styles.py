"""Environment configuration dialog styles."""

from .style_builders import dialog_background_style


ENV_DIALOG_STYLE = dialog_background_style(include_font=True)

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

__all__ = [
    "ENV_DIALOG_STYLE",
    "ENV_GROUPBOX_STYLE",
    "ENV_LINE_EDIT_STYLE",
    "ENV_RADIO_BUTTON_STYLE",
    "ENV_STATUS_LABEL_STYLE",
]
