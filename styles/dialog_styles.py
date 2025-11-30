DIALOG_STYLE = """
    QDialog {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #f8fafc, stop:1 #e2e8f0);
        border-radius: 16px;
    }
"""

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

DIALOG_BUTTON_PRIMARY_STYLE = """
    QPushButton {
        padding: 12px 20px;
        font-size: 13px;
        font-weight: 500;
        border: 1px solid #3b82f6;
        border-radius: 8px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #3b82f6, stop:1 #2563eb);
        color: white;
        min-width: 100px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #2563eb, stop:1 #1d4ed8);
        border: 1px solid #1d4ed8;
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #1d4ed8, stop:1 #1e40af);
    }
    QPushButton:focus {
        outline: none;
    }
"""

DIALOG_BUTTON_SECONDARY_STYLE = """
    QPushButton {
        padding: 12px 20px;
        font-size: 13px;
        font-weight: 500;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #ffffff, stop:1 #f8fafc);
        color: #374151;
        min-width: 100px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #f0f9ff, stop:1 #e0f2fe);
        border: 1px solid #3b82f6;
        color: #1e40af;
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #e0f2fe, stop:1 #bae6fd);
    }
    QPushButton:focus {
        outline: none;
    }
"""

SEARCH_DIALOG_STYLE = """
    QDialog {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #f8fafc, stop:1 #e2e8f0);
        border-radius: 12px;
    }
"""

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

