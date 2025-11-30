DB_DIALOG_STYLE = """
    QDialog {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #f5f7ff, stop:1 #eef2ff);
        font-family: 'Microsoft YaHei UI', 'Segoe UI', sans-serif;
    }
"""

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
        outline: none;
        border: none;
        background: transparent;
        color: #1f2937;
    }
    QTableWidget:focus {
        outline: none;
    }
    QTableWidget::item:focus:selected,
    QTableWidget::item:!focus:selected {
        outline: none;
        border: 1px solid #1d4ed8;
        background: #2563eb;
        color: #f8fafc;
    }
    QLineEdit {
        background: #ffffff;
        border: 2px solid #2563eb;
        border-radius: 6px;
        padding: 4px 8px;
        color: #1e293b;
        selection-background-color: #2563eb;
        selection-color: #f8fafc;
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

BUTTON_STYLE = """
    QPushButton {
        padding: 12px 20px;
        font-size: 13px;
        font-weight: 600;
        border: 1px solid #bfdbfe;
        border-radius: 10px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #f8fbff, stop:1 #e0f2ff);
        color: #1f2937;
        min-height: 20px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #eff6ff, stop:1 #dbeafe);
        border: 1px solid #2563eb;
        color: #1d4ed8;
    }
    QPushButton:pressed {
        background: #2563eb;
        color: #f8fafc;
        border: 1px solid #1d4ed8;
    }
    QPushButton:disabled {
        background: #e2e8f0;
        color: #94a3b8;
        border: 1px solid #cbd5e1;
    }
    QPushButton:focus {
        outline: none;
    }
"""

RESTORE_BUTTON_STYLE = """
    QPushButton {
        padding: 12px 20px;
        font-size: 13px;
        font-weight: 600;
        border: 1px solid #f97316;
        border-radius: 10px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #fdba74, stop:1 #f97316);
        color: white;
        min-height: 20px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #f97316, stop:1 #ea580c);
        border: 1px solid #ea580c;
    }
    QPushButton:pressed {
        background: #c2410c;
        border: 1px solid #c2410c;
    }
    QPushButton:focus {
        outline: none;
    }
"""

ENV_DIALOG_STYLE = """
    QDialog {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #f8fafc, stop:1 #e2e8f0);
        font-family: 'Microsoft YaHei UI', 'Segoe UI', sans-serif;
    }
"""

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

ENV_BUTTON_STYLE = """
    QPushButton {
        padding: 10px 16px;
        font-size: 12px;
        font-weight: 500;
        border: 1px solid #bfdbfe;
        border-radius: 10px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #f8fbff, stop:1 #e0f2ff);
        color: #1f2937;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #eff6ff, stop:1 #dbeafe);
        border: 1px solid #2563eb;
        color: #1d4ed8;
    }
    QPushButton:pressed {
        background: #2563eb;
        color: #f8fafc;
        border: 1px solid #1d4ed8;
    }
    QPushButton:focus {
        outline: none;
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

ENV_SAVE_BUTTON_STYLE = """
    QPushButton {
        padding: 12px 24px;
        font-size: 13px;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #10b981, stop:1 #059669);
        color: white;
        min-width: 80px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #059669, stop:1 #047857);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #047857, stop:1 #065f46);
    }
    QPushButton:focus {
        outline: none;
    }
"""

ENV_CANCEL_BUTTON_STYLE = """
    QPushButton {
        padding: 12px 24px;
        font-size: 13px;
        font-weight: 600;
        border: 1px solid #bfdbfe;
        border-radius: 10px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #f8fbff, stop:1 #e0f2ff);
        color: #1f2937;
        min-width: 80px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #eff6ff, stop:1 #dbeafe);
        border: 1px solid #2563eb;
        color: #1d4ed8;
    }
    QPushButton:pressed {
        background: #2563eb;
        color: #f8fafc;
        border: 1px solid #1d4ed8;
    }
    QPushButton:focus {
        outline: none;
    }
"""

