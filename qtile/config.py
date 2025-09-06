import subprocess
from typing import List
from libqtile import layout, bar, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from os import path
from libqtile.utils import guess_terminal

from themes.colors import colores

terminal = guess_terminal()

mod = "mod4"
mod1 = "alt"
mod2 = "control"
qtile_path = path.join(path.expanduser('~'), ".config", "qtile")
powerMenu = "bash .config/qtile/powermenu.sh"

############################################################
##################   Atajos de teclado    ##################
############################################################

keys = [Key(key[0], key[1], *key[2:]) for key in [
    ([mod], "Return", lazy.spawn(terminal)),
    ([mod], "q", lazy.spawn(powerMenu)),

    ([mod], "f", lazy.window.toggle_fullscreen()),
    ([mod], "w", lazy.window.kill()),
    ([mod, "shift"], "r", lazy.restart()),

    # QTILE LAYOUT KEYS
    ([mod], "n", lazy.layout.normalize()),
    ([mod], "space", lazy.next_layout()),

    # TOGGLE FLOATING
    ([mod, "shift"], "space", lazy.window.toggle_floating()),
    
     # REDIMENSIONAR
    ([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    ([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    ([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    ([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    ([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),
    ([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),
    ([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),
    ([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),
]]

# Movimiento entre ventanas
directions = [("h", "left"), ("l", "right"), ("j", "down"), ("k", "up")]
for key, dir in directions:
    keys.append(Key([mod], key, lazy.layout.__getattr__(dir)()))
    keys.append(Key([mod], dir.capitalize(), lazy.layout.__getattr__(dir)()))

# Redimensionar
# resize = [("h", "grow_left"), ("l", "grow_right"), ("j", "grow_down"), ("k", "grow_up")]
# for key, action in resize:
#     keys.append(Key([mod, "control"], key, lazy.layout.__getattr__(action)()))
#     keys.append(Key([mod, "control"], action.split("_")[-1].capitalize(), lazy.layout.__getattr__(action)()))

# Shuffle ventanas
for key, dir in directions:
    keys.append(Key([mod, "shift"], key, lazy.layout.__getattr__(f"shuffle_{dir}")()))

@lazy.function
def window_to_prev_group(qtile):
    if qtile.current_window is not None:
        i = qtile.groups.index(qtile.current_group)
        qtile.current_window.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.current_window is not None:
        i = qtile.groups.index(qtile.current_group)
        qtile.current_window.togroup(qtile.groups[i + 1].name)

@lazy.function
def window_to_previous_screen(qtile, switch_group=True, switch_screen=True):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen:
            qtile.cmd_to_screen(i - 1)

@lazy.function
def window_to_next_screen(qtile, switch_group=True, switch_screen=True):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen:
            qtile.cmd_to_screen(i + 1)


keys.extend([  # Cambiar entre pantallas
    Key([mod, "shift"], "Left", window_to_previous_screen),
    Key([mod, "shift"], "Right", window_to_next_screen),
])

##################################################
##################   Grupos     ##################
##################################################

# group_labels = [" ", " ", "", "", " ", "󰍳 "]
group_labels = ["", "", "", "", "", ""]
group_names = [str(i + 1) for i in range(len(group_labels))]
group_layouts = ["monadtall"] * len(group_labels)

groups = [Group(name=n, layout=l.lower(), label=la) for n, l, la in zip(group_names, group_layouts, group_labels)]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen()), # Ir al grupo i
        Key([mod], "Tab", lazy.screen.next_group()),  # Siguiente grupo
        Key([mod, "shift"], "Tab", lazy.screen.prev_group()),  # Anteriror grupo
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name), lazy.group[i.name].toscreen()),  # Mover la ventana al grupo i
    ])

##################################################
##################   Layout     ##################
##################################################

layout_config = {
    "margin": 2,
    "border_width": 2,
    "border_focus": colores["vFocus"][0],
    "border_normal": colores["inactivo"][0]
}

layouts = [layout.MonadTall(**layout_config)]

floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class='Arandr'),
    Match(wm_class='nitrogen'),
    Match(wm_class='Galculator'),
    Match(wm_class='archlinux-logout'),
], fullscreen_border_width=0, border_width=0)

#################################################################
##################   WIDGETS PARA LA BARRA    ###################
#################################################################

base = lambda fg="white", bg="barra": {
    "foreground": colores[fg],
    "background": colores[bg]
}

fuente = lambda ft="Mononoki Nerd Font", tam=16: {
    "font": ft,
    "fontsize": tam
}

separator = lambda: widget.Sep(linewidth=1, padding=10, **base())
icono = lambda ico="?", f="white", g="barra": widget.TextBox(**fuente(), **base(fg=f, bg=g), text=ico, padding=0)
powerline = lambda f="white", g="barra": widget.TextBox(**fuente(tam=42), **base(fg=f, bg=g), text="", padding=-2)

work_spaces = lambda color=colores["gSelec"][0]: [
    widget.GroupBox(
        **base(),
        **fuente(ft="FontAwesome"),
        margin_x=0,
        padding_y=6,
        padding_x=5,
        borderwidth=0,
        disable_drag=True,
        active=colores["activo"],
        inactive=colores["gInactivo"],
        rounded=False,
        highlight_method="text",
        this_current_screen_border=color,
    ),
]


bar_1 = [
    *work_spaces(),
    separator(),
    widget.CurrentLayout(font="Mononoki Nerd Font", **base()),
    separator(),
    widget.WindowName(**fuente(tam=12), **base()),

    powerline(f="wid3"),
    icono(ico=" ", g="wid3"),
    widget.Battery(**base(fg="white", bg="wid3"), **fuente(), format='{char} {percent:2.0%}', notify_below=30),

    powerline(f="wid4", g="wid3"),
    icono(ico=" ", g="wid4"),
    widget.Clock(**base(fg="white", bg="wid4"), **fuente(), format="%d/%m/%Y - %I:%M%p"),

    powerline(f="wid5", g="wid4"),
    widget.Systray(background=colores["wid5"], icon_size=20, padding=5),

    powerline(f="black", g="wid5"),
    widget.WidgetBox(
        widgets=[
            widget.QuickExit(
                default_text=' 󰍃',
                countdown_format=' {}  ',
                background=colores["black"],
                **fuente()
            ),
            widget.TextBox(
                " 󰐥 ",
                background=colores["black"],
                **fuente(),
                mouse_callbacks={'Button1': lazy.spawn(powerMenu)}
            ),
        ],
        text_closed=' ',
        text_open=' ',
        **base(bg="black"),
        **fuente(),
    ),

]

bar_2 = [
    *work_spaces(color="#ffb347"),
    separator(),
    widget.CurrentLayout(font="Mononoki Nerd Font", **base()),
    separator(),
    widget.WindowName(**fuente(tam=12), **base("white")),
]

#################################################
##################   SCREENS   ##################
#################################################

screens = [
    Screen(bottom=bar.Bar(widgets=bar_1, size=26, opacity=0.9)),
    Screen(bottom=bar.Bar(widgets=bar_2, size=26, opacity=0.9))
]

#############################################################
##################   MOUSE CONFIGURATION   ##################
#############################################################

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size())
]

@hook.subscribe.startup_once
def start_once():
    subprocess.call([path.join(qtile_path, 'autostart.sh')])

@hook.subscribe.startup
def start_always():
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for() or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]

main = None
auto_fullscreen = True
bring_front_click = True
cursor_warp = False
dgroups_key_binder = None
dgroups_app_rules = []
focus_on_window_activation = "smart"
follow_mouse_focus = True
wmname = "LG3D"