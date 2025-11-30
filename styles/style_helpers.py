def apply_stylesheet(widget, light_style, dark_style, is_dark):
    widget.setStyleSheet(dark_style if is_dark else light_style)


def apply_stylesheets(
    widgets,
    light_style,
    dark_style,
    is_dark,
):
    for widget in widgets:
        if widget is None:
            continue
        apply_stylesheet(widget, light_style, dark_style, is_dark)


def clear_stylesheet(widget):
    if widget is not None:
        widget.setStyleSheet("")
