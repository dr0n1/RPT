"""Small QSS builders for repeated Qt stylesheet fragments."""


APP_FONT_FAMILY = "'Microsoft YaHei UI', 'Segoe UI', sans-serif"
BLUE_BORDER = "#bfdbfe"
BLUE_TEXT = "#1d4ed8"
DEFAULT_TEXT = "#1f2937"
PRIMARY_BLUE = "#2563eb"


def vertical_gradient(start: str, end: str) -> str:
    """Return a vertical Qt gradient string."""
    return f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {start}, stop:1 {end})"


def dialog_background_style(
    selector: str = "QDialog",
    *,
    start: str = "#f8fafc",
    end: str = "#e2e8f0",
    border_radius: int | None = None,
    include_font: bool = False,
) -> str:
    """Build a standard dialog background style."""
    lines = [
        f"    {selector} {{",
        f"        background: {vertical_gradient(start, end)};",
    ]
    if border_radius is not None:
        lines.append(f"        border-radius: {border_radius}px;")
    if include_font:
        lines.append(f"        font-family: {APP_FONT_FAMILY};")
    lines.append("    }")
    return "\n".join(lines)


def button_style(
    *,
    padding: str,
    font_size: int,
    font_weight: int,
    border: str,
    border_radius: int,
    background: str,
    color: str,
    hover_background: str,
    hover_border: str | None = None,
    hover_color: str | None = None,
    pressed_background: str | None = None,
    pressed_border: str | None = None,
    pressed_color: str | None = None,
    disabled: bool = False,
    margin: str | None = None,
    min_width: str | None = None,
    min_height: str | None = None,
) -> str:
    """Build a QPushButton stylesheet with common interaction states."""
    lines = [
        "    QPushButton {",
        f"        padding: {padding};",
        f"        font-size: {font_size}px;",
        f"        font-weight: {font_weight};",
        f"        border: {border};",
        f"        border-radius: {border_radius}px;",
        f"        background: {background};",
        f"        color: {color};",
    ]
    if margin is not None:
        lines.insert(2, f"        margin: {margin};")
    if min_width is not None:
        lines.append(f"        min-width: {min_width};")
    if min_height is not None:
        lines.append(f"        min-height: {min_height};")
    lines.extend(
        [
            "    }",
            "    QPushButton:hover {",
            f"        background: {hover_background};",
        ]
    )
    if hover_border is not None:
        lines.append(f"        border: {hover_border};")
    if hover_color is not None:
        lines.append(f"        color: {hover_color};")
    lines.append("    }")

    if pressed_background is not None:
        lines.extend(
            [
                "    QPushButton:pressed {",
                f"        background: {pressed_background};",
            ]
        )
        if pressed_border is not None:
            lines.append(f"        border: {pressed_border};")
        if pressed_color is not None:
            lines.append(f"        color: {pressed_color};")
        lines.append("    }")

    if disabled:
        lines.extend(
            [
                "    QPushButton:disabled {",
                "        background: #e2e8f0;",
                "        color: #94a3b8;",
                "        border: 1px solid #cbd5e1;",
                "    }",
            ]
        )

    lines.extend(
        [
            "    QPushButton:focus {",
            "        outline: none;",
            "    }",
        ]
    )
    return "\n".join(lines)
