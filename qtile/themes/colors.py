import os

DEFAULT_THEME = "dark"

THEME_BASE = {
    "bar_background": "#1a1b26",
    "segment_bg": "#1a1b26",
    "segment_fg": "#c0caf5",
    "border_focus": "#bb9af7",
    "border_normal": "#1a1b26",
    "group_active": "#bb9af7",
    "group_inactive": "#c0caf5",
    "group_highlight": "#1a1b26",
    "group_block_text": "#bb9af7",
    "group_this_screen_border": "#9ece6a",
    "group_other_screen_border": "#1a1b26",
    "groups_bg": "#1a1b26",
    "systray": "#1a1b26",
    "separator": "#1a1b26",
    "color1": "#1a1b26",
    "color1fg": "#cc6666",
    "color2": "#1a1b26",
    "color2fg": "#7dcfff",
    "color3": "#1a1b26",
    "color3fg": "#bb9af7",
    "color4": "#1a1b26",
    "color4fg": "#e0af68",
    "color5": "#1a1b26",
    "color5fg": "#9ece6a",
}

THEMES = {
    "dark": {},
    "mocha": {
        "bar_background": "#0F0F1C",
        "segment_bg": "#0F0F1C",
        "segment_fg": "#cdd6f4",
        "border_focus": "#89b4fa",
        "border_normal": "#313244",
        "group_active": "#89b4fa",
        "group_inactive": "#7f849c",
        "group_this_screen_border": "#a6e3a1",
        "group_other_screen_border": "#0F0F1C",
        "color1fg": "#f38ba8",
        "color2fg": "#89dceb",
        "color3fg": "#f5c2e7",
        "color4fg": "#f9e2af",
        "color5fg": "#a6e3a1",
    },
    "noche": {
        "bar_background": "#2F343F",
        "segment_bg": "#2F343F",
        "segment_fg": "#f1ffff",
        "border_focus": "#6272a4",
        "border_normal": "#4c566a",
        "group_active": "#36c6ff",
        "group_inactive": "#6B747A",
        "group_highlight": "#2F343F",
        "group_block_text": "#36c6ff",
        "group_this_screen_border": "#36c6ff",
        "group_other_screen_border": "#2F343F",
        "groups_bg": "#2F343F",
        "systray": "#2F343F",
        "separator": "#2F343F",
        "color1": "#2F343F",
        "color2": "#2F343F",
        "color3": "#2F343F",
        "color4": "#2F343F",
        "color5": "#2F343F",
        "color1fg": "#ff8f70",
        "color2fg": "#8be9fd",
        "color3fg": "#bd93f9",
        "color4fg": "#ffb86c",
        "color5fg": "#50fa7b",
    },
}


def get_theme(name: str = DEFAULT_THEME) -> dict[str, str]:
    selected_theme = (name or DEFAULT_THEME).lower()
    theme = dict(THEME_BASE)
    theme.update(THEMES.get(selected_theme, THEMES[DEFAULT_THEME]))
    return theme


def get_active_theme() -> dict[str, str]:
    return get_theme(os.getenv("QTILE_THEME", DEFAULT_THEME))


def get_tema(nombre: str = DEFAULT_THEME) -> dict[str, list[str]]:
    tema = get_theme(nombre)
    return {
        "barra": [tema["bar_background"], tema["bar_background"]],
        "vFocus": [tema["border_focus"], tema["border_focus"]],
        "inactivo": [tema["border_normal"], tema["border_normal"]],
        "activo": [tema["segment_fg"], tema["segment_fg"]],
        "gInactivo": [tema["group_inactive"], tema["group_inactive"]],
        "gSelec": [tema["group_active"], tema["group_active"]],
    }


theme = get_active_theme()
