import os

DEFAULT_THEME = "dark"

THEMES = {
    "mocha": {
        "bar_background": "#3b4252",
        "segment_bg": "#242831",
        "segment_fg": "#d8dee9",
        "border_focus": "#038C8C",
        "border_normal": "#4c566a",
        "group_active": "#5e81ac",
        "group_inactive": "#4c566a",
        "group_highlight": "#3b4252",
        "group_block_text": "#81a1c1",
        "group_this_screen_border": "#a3be8c",
        "group_other_screen_border": "#242831",
    },
    "noche": {
        "bar_background": "#2F343F",
        "segment_bg": "#040414",
        "segment_fg": "#f1ffff",
        "border_focus": "#6272a4",
        "border_normal": "#4c566a",
        "group_active": "#36c6ff",
        "group_inactive": "#6B747A",
        "group_highlight": "#2F343F",
        "group_block_text": "#36c6ff",
        "group_this_screen_border": "#36c6ff",
        "group_other_screen_border": "#040414",
    },
    "dark": {
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
        "color1": "#1a1b26",
        "color1fg": "#cc6666",
        "color3": "#1a1b26",
        "color3fg": "#bb9af7",
        "color5": "#1a1b26",
        "color5fg": "#9ece6a",
    },
}


def get_theme(name: str = DEFAULT_THEME) -> dict[str, str]:
    selected_theme = (name or DEFAULT_THEME).lower()
    return THEMES.get(selected_theme, THEMES[DEFAULT_THEME]).copy()


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
