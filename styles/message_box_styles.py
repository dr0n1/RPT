MESSAGE_BOX_LIGHT_STYLE = """
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

MESSAGE_BOX_DARK_STYLE = """
    QMessageBox {
        background-color: #1f1f2f;
        color: #cdd6f4;
    }
    QMessageBox QLabel {
        color: #cdd6f4;
        font-size: 13px;
    }
    QMessageBox QPushButton {
        padding: 8px 18px;
        font-size: 12px;
        font-weight: 600;
        border-radius: 8px;
        border: 1px solid #585b70;
        background-color: #313244;
        color: #cdd6f4;
        min-width: 70px;
    }
    QMessageBox QPushButton:hover {
        background-color: #45475a;
        border: 1px solid #89b4fa;
        color: #89b4fa;
    }
    QMessageBox QPushButton:pressed {
        background-color: #74c7ec;
        border: 1px solid #89dceb;
        color: #11111b;
    }
"""


def style_message_box(box, is_dark):
    box.setStyleSheet(MESSAGE_BOX_DARK_STYLE if is_dark else MESSAGE_BOX_LIGHT_STYLE)
