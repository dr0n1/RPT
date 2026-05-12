from collections.abc import Iterable


def apply_stylesheet(widget: object | None, style: str) -> None:
    """Apply a single stylesheet to a widget if it exists."""
    if widget is not None:
        widget.setStyleSheet(style)


def apply_stylesheets(widgets: Iterable[object | None], style: str) -> None:
    """Apply the same stylesheet to a collection of widgets."""
    for widget in widgets:
        if widget is None:
            continue
        apply_stylesheet(widget, style)


def clear_stylesheet(widget: object | None) -> None:
    """Clear a widget stylesheet if the widget exists."""
    if widget is not None:
        widget.setStyleSheet("")
