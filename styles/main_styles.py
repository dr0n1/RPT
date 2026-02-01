MAIN_WINDOW_STYLE = """
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #f5f7ff, stop:1 #eef2ff);
        font-family: 'Microsoft YaHei UI', 'Segoe UI', sans-serif;
        color: #1f2937;
    }
    
    QToolTip {
        color: #1e293b;
        background-color: #ffffff;
        border: 1px solid #dbeafe;
        border-radius: 6px;
        padding: 8px 10px;
        font-size: 12px;
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
    
    QStatusBar {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #ffffff, stop:1 #f1f5f9);
        border-top: 1px solid #dbeafe;
        padding: 6px 12px;
        color: #1f2937;
    }
    
    QStatusBar::item {
        border: none;
        padding: 4px 10px;
        color: #475569;
    }
    
    QPushButton:focus, QListWidget:focus, QListWidget::item:focus {
        outline: none;
    }
"""

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

TOOL_BUTTON_STYLE = """
    QPushButton {
        padding: 12px 20px;
        margin: 4px;
        border: 1px solid #bfdbfe;
        border-radius: 12px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #f8fbff, stop:1 #e0f2ff);
        color: #1f2937;
        font-weight: 600;
        font-size: 13px;
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
