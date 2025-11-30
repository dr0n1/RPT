MAIN_WINDOW_DARK_STYLE = """
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #1e1e2e, stop:1 #181825);
        font-family: 'Microsoft YaHei UI', 'Segoe UI', sans-serif;
        color: #cdd6f4;
    }
    
    QToolTip {
        color: #cdd6f4;
        background-color: #1f1f2f;
        border: 1px solid #585b70;
        border-radius: 8px;
        padding: 10px 12px;
        font-size: 12px;
    }
    
    QMenuBar {
        background: #1f1f2f;
        border-bottom: 1px solid #585b70;
        padding: 6px 12px;
        color: #cdd6f4;
    }
    
    QMenuBar::item {
        padding: 6px 14px;
        border-radius: 6px;
        margin: 0 4px;
        color: #cdd6f4;
    }
    
    QMenuBar::item:selected {
        background: #74c7ec;
        color: #1e1e2e;
    }
    
    QMenu {
        background-color: #1f1f2f;
        border: 1px solid #585b70;
        border-radius: 10px;
        padding: 6px;
        margin: 0px;
        color: #cdd6f4;
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
        color: #cdd6f4;
    }
    
    QMenu::item:selected {
        background: rgba(116, 199, 236, 0.2);
        color: #89b4fa;
    }
    
    QStatusBar {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #1f1f2f, stop:1 #181825);
        border-top: 1px solid #585b70;
        padding: 6px 12px;
        color: #cdd6f4;
    }
    
    QStatusBar::item {
        border: none;
        padding: 4px 10px;
        color: #bac2de;
    }
    
    QPushButton:focus, QListWidget:focus, QListWidget::item:focus {
        outline: none;
    }
"""

GROUPBOX_DARK_STYLE = """
    QGroupBox {
        background: rgba(30, 32, 48, 0.85);
        border: 1px solid #585b70;
        border-radius: 16px;
        margin: 8px;
        padding: 18px;
        font-weight: 600;
        color: #cdd6f4;
    }
"""

LISTWIDGET_DARK_STYLE = """
    QListWidget {
        background: rgba(30, 32, 48, 0.9);
        border: 1px solid #585b70;
        border-radius: 14px;
        padding: 8px;
        margin: 8px;
        font-size: 13px;
        font-weight: 500;
        color: #cdd6f4;
    }
    
    QListWidget::item {
        padding: 12px 16px;
        margin: 2px;
        border-radius: 10px;
        background: transparent;
        color: #cdd6f4;
    }
    
    QListWidget::item:hover {
        background: rgba(137, 180, 250, 0.12);
        border: 1px solid #89b4fa;
    }
    
    QListWidget::item:selected {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #74c7ec, stop:1 #89b4fa);
        color: #1e1e2e;
        border: 1px solid #74c7ec;
    }
"""

TOOL_BUTTON_DARK_STYLE = """
    QPushButton {
        padding: 12px 20px;
        margin: 4px;
        border: 1px solid #585b70;
        border-radius: 12px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #313244, stop:1 #1f1f2f);
        color: #cdd6f4;
        font-weight: 600;
        font-size: 13px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #45475a, stop:1 #313244);
        border: 1px solid #89b4fa;
        color: #89b4fa;
    }
    QPushButton:pressed {
        background: #89b4fa;
        color: #11111b;
        border: 1px solid #74c7ec;
    }
    QPushButton:disabled {
        background: #27283a;
        color: #6c7086;
        border: 1px solid #3b3d4f;
    }
"""

DIALOG_DARK_STYLE = """
    QDialog {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #1e1e2e, stop:1 #11111b);
        border-radius: 16px;
    }
"""

DIALOG_LABEL_TITLE_DARK_STYLE = """
    QLabel {
        font-size: 24px;
        font-weight: bold;
        color: #cdd6f4;
        background: transparent;
        border: none;
        padding: 10px;
    }
"""

DIALOG_LABEL_VERSION_DARK_STYLE = """
    QLabel {
        font-size: 16px;
        font-weight: 500;
        color: #a6adc8;
        background: transparent;
        border: none;
        padding: 5px;
    }
"""

DIALOG_LABEL_INFO_DARK_STYLE = """
    QLabel {
        font-size: 14px;
        font-weight: 500;
        color: #cdd6f4;
        background: rgba(49, 50, 68, 0.8);
        border: 1px solid #45475a;
        border-radius: 10px;
        padding: 12px 16px;
    }
"""

DIALOG_LABEL_DESC_TITLE_DARK_STYLE = """
    QLabel {
        font-size: 14px;
        font-weight: 600;
        color: #cdd6f4;
        background: transparent;
        border: none;
        padding: 8px 0px;
    }
"""

DIALOG_LABEL_DESC_TEXT_DARK_STYLE = """
    QLabel {
        font-size: 13px;
        color: #a6adc8;
        background: rgba(49, 50, 68, 0.9);
        border: 1px solid #45475a;
        border-radius: 10px;
        padding: 16px;
        line-height: 1.5;
    }
"""

DIALOG_BUTTON_PRIMARY_DARK_STYLE = """
    QPushButton {
        padding: 12px 20px;
        font-size: 13px;
        font-weight: 500;
        border: 1px solid #89b4fa;
        border-radius: 10px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #89b4fa, stop:1 #74c7ec);
        color: #1e1e2e;
        min-width: 100px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #74c7ec, stop:1 #89b4fa);
        border: 1px solid #74c7ec;
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #89b4fa, stop:1 #74c7ec);
    }
    QPushButton:focus {
        outline: none;
    }
"""

DIALOG_BUTTON_SECONDARY_DARK_STYLE = """
    QPushButton {
        padding: 12px 20px;
        font-size: 13px;
        font-weight: 500;
        border: 1px solid #45475a;
        border-radius: 10px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #313244, stop:1 #1e1e2e);
        color: #cdd6f4;
        min-width: 100px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #45475a, stop:1 #313244);
        border: 1px solid #89b4fa;
        color: #89b4fa;
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #1e1e2e, stop:1 #11111b);
    }
    QPushButton:focus {
        outline: none;
    }
"""

SEARCH_DIALOG_DARK_STYLE = """
    QDialog {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #1e1e2e, stop:1 #11111b);
        border-radius: 12px;
    }
"""

SEARCH_INPUT_DARK_STYLE = """
    QLineEdit {
        padding: 12px 16px;
        font-size: 14px;
        border: 2px solid #45475a;
        border-radius: 12px;
        background: #313244;
        color: #cdd6f4;
    }
    QLineEdit:focus {
        border: 2px solid #89b4fa;
        background: #1e1e2e;
    }
"""

SEARCH_RESULT_LIST_DARK_STYLE = """
    QListWidget {
        font-size: 13px;
        background: rgba(49, 50, 68, 0.9);
        border: 1px solid #45475a;
        border-radius: 12px;
        padding: 8px;
        color: #cdd6f4;
    }
    QListWidget::item {
        padding: 10px 12px;
        margin: 2px;
        border-radius: 8px;
        background: transparent;
        color: #cdd6f4;
    }
    QListWidget::item:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #313244, stop:1 #1e1e2e);
        border: 1px solid #89b4fa;
    }
    QListWidget::item:selected {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #89b4fa, stop:1 #74c7ec);
        color: #1e1e2e;
    }
"""

DB_DIALOG_DARK_STYLE = """
    QDialog {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #1e1e2e, stop:1 #181825);
        font-family: 'Microsoft YaHei UI', 'Segoe UI', sans-serif;
    }
"""

TAB_WIDGET_DARK_STYLE = """
    QTabWidget::pane {
        border: 1px solid #585b70;
        border-radius: 10px;
        background: rgba(30, 32, 48, 0.9);
    }
    QTabBar::tab {
        background: #1f1f2f;
        border: 1px solid #585b70;
        padding: 10px 20px;
        margin: 0 2px;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        font-weight: 600;
        color: #cdd6f4;
    }
    QTabBar::tab:selected {
        background: #74c7ec;
        color: #11111b;
        border: 1px solid #89dceb;
    }
    QTabBar::tab:hover:!selected {
        background: rgba(137, 180, 250, 0.18);
        color: #89b4fa;
    }
"""

TABLE_WIDGET_DARK_STYLE = """
    QTableWidget {
        font-size: 14px;
        background: rgba(30, 32, 48, 0.94);
        border: 1px solid #585b70;
        border-radius: 10px;
        gridline-color: #2b2d40;
        selection-background-color: transparent;
        selection-color: #cdd6f4;
        outline: none;
        color: #cdd6f4;
    }
    QTableWidget::item {
        padding: 0px;
        border-bottom: 1px solid #2b2d40;
        border: none;
        min-height: 30px;
        color: #cdd6f4;
        background: transparent;
    }
    QTableWidget::item:selected {
        background: #74c7ec;
        color: #11111b;
        border: 1px solid #89dceb;
        outline: none;
    }
    QTableWidget::item:focus {
        outline: none;
        border: none;
        background: transparent;
        color: #cdd6f4;
    }
    QTableWidget:focus {
        outline: none;
    }
    QTableWidget::item:focus:selected {
        outline: none;
        border: 1px solid #89dceb;
        background: #74c7ec;
        color: #11111b;
    }
    QTableWidget::item:!focus:selected {
        outline: none;
        border: 1px solid #89dceb;
        background: #74c7ec;
        color: #11111b;
    }
    QTableWidget QHeaderView {
        background: #1f1f2f;
        border: none;
    }
    QLineEdit {
        background: rgba(31, 31, 47, 0.9);
        border: 2px solid #74c7ec;
        border-radius: 6px;
        padding: 4px 8px;
        color: #cdd6f4;
        selection-background-color: #89b4fa;
        selection-color: #11111b;
    }
    QHeaderView::section {
        background: #1f1f2f;
        border: 1px solid #585b70;
        padding: 15px;
        font-weight: 600;
        color: #cdd6f4;
        font-size: 15px;
        min-height: 40px;
    }
    QHeaderView::section:horizontal {
        border-top: 1px solid #45475a;
    }
    QHeaderView::section:vertical {
        border-left: 1px solid #45475a;
    }
    QTableCornerButton::section {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #313244, stop:1 #1e1e2e);
        border: 1px solid #45475a;
        border-top-left-radius: 10px;
    }
"""

BUTTON_DARK_STYLE = """
    QPushButton {
        padding: 12px 20px;
        font-size: 13px;
        font-weight: 600;
        border: 1px solid #585b70;
        border-radius: 10px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #313244, stop:1 #1f1f2f);
        color: #cdd6f4;
        min-height: 20px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #45475a, stop:1 #313244);
        border: 1px solid #89b4fa;
        color: #89b4fa;
    }
    QPushButton:pressed {
        background: #74c7ec;
        color: #11111b;
        border: 1px solid #89dceb;
    }
    QPushButton:focus {
        outline: none;
    }
"""

RESTORE_BUTTON_DARK_STYLE = """
    QPushButton {
        padding: 12px 20px;
        font-size: 13px;
        font-weight: 600;
        border: 1px solid #f97316;
        border-radius: 10px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #fba94c, stop:1 #f97316);
        color: #11111b;
        min-height: 20px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #f97316, stop:1 #ea580c);
        border: 1px solid #ea580c;
        color: #11111b;
    }
    QPushButton:pressed {
        background: #c2410c;
        border: 1px solid #c2410c;
        color: #fde68a;
    }
    QPushButton:focus {
        outline: none;
    }
"""

ENV_DIALOG_DARK_STYLE = """
    QDialog {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #1e1e2e, stop:1 #11111b);
        font-family: 'Microsoft YaHei UI', 'Segoe UI', sans-serif;
    }
"""

ENV_GROUPBOX_DARK_STYLE = """
    QGroupBox {
        background: rgba(49, 50, 68, 0.9);
        border: 2px solid #45475a;
        border-radius: 14px;
        margin: 8px;
        padding: 16px;
        font-weight: 600;
        font-size: 14px;
        color: #cdd6f4;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 8px 0 8px;
        background: #313244;
    }
"""

ENV_RADIO_BUTTON_DARK_STYLE = """
    QRadioButton {
        font-size: 13px;
        font-weight: 500;
        color: #cdd6f4;
        spacing: 8px;
    }
    QRadioButton::indicator {
        width: 18px;
        height: 18px;
        border-radius: 9px;
        border: 2px solid #585b70;
        background: #1f1f2f;
    }
    QRadioButton::indicator:checked {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #74c7ec, stop:1 #89b4fa);
        border: 2px solid #89dceb;
    }
"""

ENV_LINE_EDIT_DARK_STYLE = """
    QLineEdit {
        padding: 10px 12px;
        font-size: 12px;
        border: 1px solid #585b70;
        border-radius: 10px;
        background: #1f1f2f;
        color: #cdd6f4;
    }
"""

ENV_BUTTON_DARK_STYLE = """
    QPushButton {
        padding: 10px 16px;
        font-size: 12px;
        font-weight: 500;
        border: 1px solid #585b70;
        border-radius: 10px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #313244, stop:1 #1f1f2f);
        color: #cdd6f4;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #45475a, stop:1 #313244);
        border: 1px solid #89b4fa;
        color: #89b4fa;
    }
    QPushButton:pressed {
        background: #74c7ec;
        color: #11111b;
        border: 1px solid #89dceb;
    }
    QPushButton:focus {
        outline: none;
    }
"""

ENV_STATUS_LABEL_DARK_STYLE = """
    QLabel {
        padding: 12px 16px;
        color: #cdd6f4;
        background: rgba(49, 50, 68, 0.8);
        border: 1px solid #45475a;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 500;
    }
"""

ENV_SAVE_BUTTON_DARK_STYLE = """
    QPushButton {
        padding: 12px 24px;
        font-size: 13px;
        font-weight: 600;
        border: 1px solid #89b4fa;
        border-radius: 10px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #89b4fa, stop:1 #74c7ec);
        color: #1e1e2e;
        min-width: 80px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #74c7ec, stop:1 #89b4fa);
        border: 1px solid #74c7ec;
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #89b4fa, stop:1 #74c7ec);
    }
    QPushButton:focus {
        outline: none;
    }
"""

ENV_CANCEL_BUTTON_DARK_STYLE = """
    QPushButton {
        padding: 12px 24px;
        font-size: 13px;
        font-weight: 600;
        border: 1px solid #585b70;
        border-radius: 10px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #313244, stop:1 #1f1f2f);
        color: #cdd6f4;
        min-width: 80px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #45475a, stop:1 #313244);
        border: 1px solid #89b4fa;
    }
    QPushButton:pressed {
        background: #1f1f2f;
        border: 1px solid #585b70;
    }
    QPushButton:focus {
        outline: none;
    }
"""
