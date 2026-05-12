"""Reusable button styles for dialogs, tables, and tool launchers."""

from .style_builders import (
    BLUE_BORDER,
    BLUE_TEXT,
    DEFAULT_TEXT,
    PRIMARY_BLUE,
    button_style,
    vertical_gradient,
)


BUTTON_STYLE = button_style(
    padding="12px 20px",
    font_size=13,
    font_weight=600,
    border=f"1px solid {BLUE_BORDER}",
    border_radius=10,
    background=vertical_gradient("#f8fbff", "#e0f2ff"),
    color=DEFAULT_TEXT,
    hover_background=vertical_gradient("#eff6ff", "#dbeafe"),
    hover_border=f"1px solid {PRIMARY_BLUE}",
    hover_color=BLUE_TEXT,
    pressed_background=PRIMARY_BLUE,
    pressed_border=f"1px solid {BLUE_TEXT}",
    pressed_color="#f8fafc",
    disabled=True,
    min_height="20px",
)

TOOL_BUTTON_STYLE = button_style(
    padding="12px 20px",
    font_size=13,
    font_weight=600,
    border=f"1px solid {BLUE_BORDER}",
    border_radius=12,
    background=vertical_gradient("#f8fbff", "#e0f2ff"),
    color=DEFAULT_TEXT,
    hover_background=vertical_gradient("#eff6ff", "#dbeafe"),
    hover_border=f"1px solid {PRIMARY_BLUE}",
    hover_color=BLUE_TEXT,
    pressed_background=PRIMARY_BLUE,
    pressed_border=f"1px solid {BLUE_TEXT}",
    pressed_color="#f8fafc",
    disabled=True,
    margin="4px",
)

RESTORE_BUTTON_STYLE = button_style(
    padding="12px 20px",
    font_size=13,
    font_weight=600,
    border="1px solid #f97316",
    border_radius=10,
    background=vertical_gradient("#fdba74", "#f97316"),
    color="white",
    hover_background=vertical_gradient("#f97316", "#ea580c"),
    hover_border="1px solid #ea580c",
    pressed_background="#c2410c",
    pressed_border="1px solid #c2410c",
    min_height="20px",
)

DIALOG_BUTTON_PRIMARY_STYLE = button_style(
    padding="12px 20px",
    font_size=13,
    font_weight=500,
    border="1px solid #3b82f6",
    border_radius=8,
    background=vertical_gradient("#3b82f6", PRIMARY_BLUE),
    color="white",
    hover_background=vertical_gradient(PRIMARY_BLUE, BLUE_TEXT),
    hover_border=f"1px solid {BLUE_TEXT}",
    pressed_background=vertical_gradient(BLUE_TEXT, "#1e40af"),
    min_width="100px",
)

DIALOG_BUTTON_SECONDARY_STYLE = button_style(
    padding="12px 20px",
    font_size=13,
    font_weight=500,
    border="1px solid #d1d5db",
    border_radius=8,
    background=vertical_gradient("#ffffff", "#f8fafc"),
    color="#374151",
    hover_background=vertical_gradient("#f0f9ff", "#e0f2fe"),
    hover_border="1px solid #3b82f6",
    hover_color="#1e40af",
    pressed_background=vertical_gradient("#e0f2fe", "#bae6fd"),
    min_width="100px",
)

ENV_BUTTON_STYLE = button_style(
    padding="10px 16px",
    font_size=12,
    font_weight=500,
    border=f"1px solid {BLUE_BORDER}",
    border_radius=10,
    background=vertical_gradient("#f8fbff", "#e0f2ff"),
    color=DEFAULT_TEXT,
    hover_background=vertical_gradient("#eff6ff", "#dbeafe"),
    hover_border=f"1px solid {PRIMARY_BLUE}",
    hover_color=BLUE_TEXT,
    pressed_background=PRIMARY_BLUE,
    pressed_border=f"1px solid {BLUE_TEXT}",
    pressed_color="#f8fafc",
)

ENV_SAVE_BUTTON_STYLE = button_style(
    padding="12px 24px",
    font_size=13,
    font_weight=600,
    border="none",
    border_radius=10,
    background=vertical_gradient("#10b981", "#059669"),
    color="white",
    hover_background=vertical_gradient("#059669", "#047857"),
    pressed_background=vertical_gradient("#047857", "#065f46"),
    min_width="80px",
)

ENV_CANCEL_BUTTON_STYLE = button_style(
    padding="12px 24px",
    font_size=13,
    font_weight=600,
    border=f"1px solid {BLUE_BORDER}",
    border_radius=10,
    background=vertical_gradient("#f8fbff", "#e0f2ff"),
    color=DEFAULT_TEXT,
    hover_background=vertical_gradient("#eff6ff", "#dbeafe"),
    hover_border=f"1px solid {PRIMARY_BLUE}",
    hover_color=BLUE_TEXT,
    pressed_background=PRIMARY_BLUE,
    pressed_border=f"1px solid {BLUE_TEXT}",
    pressed_color="#f8fafc",
    min_width="80px",
)

__all__ = [
    "BUTTON_STYLE",
    "DIALOG_BUTTON_PRIMARY_STYLE",
    "DIALOG_BUTTON_SECONDARY_STYLE",
    "ENV_BUTTON_STYLE",
    "ENV_CANCEL_BUTTON_STYLE",
    "ENV_SAVE_BUTTON_STYLE",
    "RESTORE_BUTTON_STYLE",
    "TOOL_BUTTON_STYLE",
]
