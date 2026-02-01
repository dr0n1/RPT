def apply_stylesheet(widget, style):
    """Apply a single stylesheet to a widget if it exists."""
    if widget is not None:
        widget.setStyleSheet(style)


def apply_stylesheets(widgets, style):
    """Apply the same stylesheet to a collection of widgets."""
    for widget in widgets:
        if widget is None:
            continue
        apply_stylesheet(widget, style)


def clear_stylesheet(widget):
    if widget is not None:
        widget.setStyleSheet("")
