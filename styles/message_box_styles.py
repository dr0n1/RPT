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


def style_message_box(box):
    box.setStyleSheet(MESSAGE_BOX_STYLE)
