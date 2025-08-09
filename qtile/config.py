import subprocess
from typing import List
from libqtile import layout, bar, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from os import path
from libqtile.utils import guess_terminal

from themes.colors import coloress

terminal = guess_terminal()

mod = "mod4"
mod1 = "alt"
mod2 = "control"
qtile_path = path.join(path.expanduser('~'), ".config", "qtile")

############################################################
##################   Atajos de teclado    ##################
############################################################

keys = [Key(key[0], key[1], *key[2:]) for key in [
    ([mod], "Return", lazy.spawn(terminal)),

    ([mod], "f", lazy.window.toggle_fullscreen()),
    ([mod], "w", lazy.window.kill()),
    ([mod, "shift"], "r", lazy.restart()),

    # QTILE LAYOUT KEYS
    ([mod], "n", lazy.layout.normalize()),
    ([mod], "space", lazy.next_layout()),

    # CAMBIAR ENFOQUE
    ([mod], "Up", lazy.layout.up()),
    ([mod], "Down", lazy.layout.down()),
    ([mod], "Left", lazy.layout.left()),
    ([mod], "Right", lazy.layout.right()),
    ([mod], "k", lazy.layout.up()),
    ([mod], "j", lazy.layout.down()),
    ([mod], "h", lazy.layout.left()),
    ([mod], "l", lazy.layout.right()),

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

    # FLIP LAYOUT
    ([mod, "shift"], "f", lazy.layout.flip()),

    # FLIP BSP
    ([mod, "mod1"], "k", lazy.layout.flip_up()),
    ([mod, "mod1"], "j", lazy.layout.flip_down()),
    ([mod, "mod1"], "l", lazy.layout.flip_right()),
    ([mod, "mod1"], "h", lazy.layout.flip_left()),

    # MOVER VENTANAS BSP
    ([mod, "shift"], "k", lazy.layout.shuffle_up()),
    ([mod, "shift"], "j", lazy.layout.shuffle_down()),
    ([mod, "shift"], "h", lazy.layout.shuffle_left()),
    ([mod, "shift"], "l", lazy.layout.shuffle_right()),

    # MOVER VENTANAS MONADTALL/MONADWIDE
    ([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    ([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    ([mod, "shift"], "Left", lazy.layout.swap_left()),
    ([mod, "shift"], "Right", lazy.layout.swap_right()),

    # TOGGLE FLOATING
    ([mod, "shift"], "space", lazy.window.toggle_floating()),
]]

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

def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen:
            qtile.cmd_to_screen(i - 1)

def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen:
            qtile.cmd_to_screen(i + 1)

keys.extend([
    Key([mod, "shift"], "Right", lazy.function(window_to_next_screen, switch_screen=True)),
    Key([mod, "shift"], "Left", lazy.function(window_to_previous_screen, switch_screen=True)),
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
        Key(["mod1"], i.name, lazy.group[i.name].toscreen()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name), lazy.group[i.name].toscreen()),
    ])

##################################################
##################   Layout     ##################
##################################################

layout_config = {
    "margin": 5,
    "border_width": 1,
    "border_focus": coloress["vFocus"][0],
    "border_normal": coloress["inactivo"][0]
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
    "foreground": coloress[fg],
    "background": coloress[bg]
}

fuente = lambda ft="Mononoki Nerd Font", tam=16: {
    "font": ft,
    "fontsize": tam
}

separator = lambda: widget.Sep(linewidth=1, padding=10, **base())
icono = lambda ico="?", f="white", g="barra": widget.TextBox(**fuente(), **base(fg=f, bg=g), text=ico, padding=0)
powerline = lambda f="white", g="barra": widget.TextBox(**fuente(tam=42), **base(fg=f, bg=g), text="", padding=-2)

work_spaces = lambda: [
    widget.GroupBox(
        **base(),
        **fuente(ft="FontAwesome"),
        margin_x=0,
        padding_y=6,
        padding_x=5,
        borderwidth=0,
        disable_drag=True,
        active=coloress["activo"],
        inactive=coloress["gInactivo"],
        rounded=False,
        highlight_method="text",
        this_current_screen_border=coloress["gSelec"][0],
    ),
]

widgets_list = [
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
    widget.Systray(background=coloress["wid5"], icon_size=20, padding=5),
]

other_widgets_list = [
    *work_spaces(),
    separator(),
    widget.CurrentLayout(font="Mononoki Nerd Font", **base()),
    separator(),
    widget.WindowName(**fuente(tam=12), **base("white")),
]

#################################################
##################   SCREENS   ##################
#################################################

screens = [
    Screen(bottom=bar.Bar(widgets=widgets_list, size=26, opacity=0.8)),
    Screen(bottom=bar.Bar(widgets=other_widgets_list, size=26, opacity=0.8))
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