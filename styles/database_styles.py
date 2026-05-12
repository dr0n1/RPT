"""Database management dialog and table styles."""

from .style_builders import dialog_background_style


DB_DIALOG_STYLE = dialog_background_style(
    start="#f5f7ff",
    end="#eef2ff",
    include_font=True,
)

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

__all__ = [
    "DB_DIALOG_STYLE",
    "TAB_WIDGET_STYLE",
    "TABLE_WIDGET_STYLE",
]
