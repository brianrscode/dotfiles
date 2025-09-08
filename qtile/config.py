import subprocess
from typing import List
from libqtile import layout, bar, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from os import path
from libqtile.utils import guess_terminal

from themes.colors import colores

from libqtile import qtile
from libqtile.widget import Spacer
import os
import socket
import subprocess


terminal = guess_terminal()

mod = "mod4"
mod1 = "alt"
mod2 = "control"
qtile_path = path.join(path.expanduser('~'), ".config", "qtile")
powerMenu = "bash .config/qtile/powermenu.sh"


def openCalendar():
    qtile.cmd_spawn("gsimplecal")

def openHtop():
    qtile.cmd_spawn("alacritty -e htop")

def openMenu():
    qtile.cmd_spawn(powerMenu)

def init_colors():
    return [
        ["#2e3440", "#2e3440"],  # 0 background
        ["#d8dee9", "#d8dee9"],  # 1 foreground
        ["#3b4252", "#3b4252"],  # 2 background lighter
        ["#bf616a", "#bf616a"],  # 3 red
        ["#a3be8c", "#a3be8c"],  # 4 green
        ["#ebcb8b", "#ebcb8b"],  # 5 yellow
        ["#81a1c1", "#81a1c1"],  # 6 blue
        ["#b48ead", "#b48ead"],  # 7 magenta
        ["#88c0d0", "#88c0d0"],  # 8 cyan
        ["#e5e9f0", "#e5e9f0"],  # 9 white
        ["#4c566a", "#4c566a"],  # 10 grey
        ["#d08770", "#d08770"],  # 11 orange
        ["#8fbcbb", "#8fbcbb"],  # 12 super cyan
        ["#5e81ac", "#5e81ac"],  # 13 super blue
        ["#242831", "#242831"],  # 14 super dark background
        ["#00000000", "#00000000"],  # 15 transparent (2)
    ]

colors = init_colors()
left = ""
right = ""


############################################################
##################   Atajos de teclado    ##################
############################################################

keys = [Key(key[0], key[1], *key[2:]) for key in [
    ([mod], "Return", lazy.spawn(terminal)),
    ([mod], "q", lazy.spawn(powerMenu)),

    ([mod], "b", lazy.hide_show_bar()),

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

base = lambda fg=colors[14], bg=colors[2], fs=26: {
    "foreground": fg,
    "background": bg,
    "fontsize": fs,
}
pwl_i = lambda: widget.TextBox(text=left, **base(), padding=-1)
pwl_d = lambda: widget.TextBox(text=right, **base())

def init_widgets_defaults():
    return dict(
        font="Noto Sans Bold", 
        padding=0,
        **base(fs=12),
        margin=2,
    )

widget_defaults = init_widgets_defaults()

def init_widgets_list():
    widgets = [
        widget.Spacer(length=10),

        widget.Image(
            filename="~/.config/qtile/icons/python.png",
            mouse_callbacks={"Button1": openMenu},
        ),

        widget.Spacer(length=10),

        pwl_i(),
        widget.GroupBox(
            font="FontAwesome",
            margin_y=0,
            margin_x=0,
            padding_y=0,
            padding_x=4,
            disable_drag=True,
            use_mouse_wheel=True,
            active=colors[13],
            inactive=colors[10],
            rounded=True,
            highlight_color=colors[2],
            highlight_method="text",
            block_highlight_text_color=colors[6],
            this_current_screen_border=colors[4],
            this_screen_border=colors[4],
            other_current_screen_border=colors[14],
            other_screen_border=colors[14],
            **base(fg=colors[1], bg=colors[14], fs=12),
        ),
        pwl_d(),

        widget.Spacer(length=20),

        pwl_i(),
        widget.WindowName(
            font="Noto Sans Bold",
            **base(fg=colors[1], bg=colors[14], fs=10),
            width=bar.CALCULATED,
            empty_group_string="Desktop",
            max_chars=80,
        ),
        pwl_d(),

        widget.Spacer(),

        # pwl_i(),
        # widget.TextBox(text="  ", foreground=colors[13], background=colors[14], fontsize=16, mouse_callbacks={"Button1": openHtop}),
        # widget.TextBox(text=" CPU ", foreground=colors[1], background=colors[14], fontsize=12),
        # widget.ThermalSensor(
        #     foreground=colors[1],
        #     background=colors[14],
        #     metric=True,
        #     padding=3,
        #     tag_sensor="Package id 0",
        #     threshold=80,
        #     mouse_callbacks={"Button1": openHtop},
        # ),
        # widget.TextBox(text=" GPU ", foreground=colors[1], background=colors[14], fontsize=12),
        # widget.ThermalSensor(
        #     foreground=colors[1],
        #     background=colors[14],
        #     metric=True,
        #     padding=3,
        #     tag_sensor="GPU",
        #     threshold=80,
        #     mouse_callbacks={"Button1": openHtop},
        # ),
        # widget.Sep(foreground=colors[1], background=colors[14], linewidth=2, padding=2, size_percent=50),
        # widget.TextBox(text="  ", foreground=colors[13], background=colors[14], fontsize=16),
        # widget.Memory(
        #     measure_mem="G",
        #     format="{MemUsed: .1f}G/{MemTotal: .1f}G ",
        #     update_interval=5,
        #     foreground=colors[1],
        #     background=colors[14],
        # ),
        # pwl_d(),

        pwl_i(),
        widget.TextBox(text=" ", **base(fg=colors[13], bg=colors[14], fs=18), mouse_callbacks={"Button1": openCalendar}),
        widget.Clock(
            format=" %a-%d | %H:%M ",
            **base(fg=colors[1], bg=colors[14], fs=12),
            mouse_callbacks={"Button1": openCalendar},
        ),
        pwl_d(),

        widget.Spacer(length=3),

        pwl_i(),
        widget.TextBox(text=" ", **base(fg=colors[1], bg=colors[14], fs=18)),
        widget.Backlight(backlight_name="intel_backlight", background=colors[14], foreground=colors[1]),
        pwl_d(),

        widget.Spacer(length=3),

        pwl_i(),
        widget.TextBox(text="  ", **base(fg=colors[1], bg=colors[14], fs=18), mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("pavucontrol")}),
        widget.Volume(background=colors[14], foreground=colors[1], padding=0),
        pwl_d(),

        widget.Spacer(length=3),

        # pwl_i(),
        # widget.Battery(
        #     format="{char} {percent:2.0%}",
        #     #format="{char} {percent:2.0%} {hour:d}:{min:02d}",
        #     charge_char=" 󰢝 ",
        #     discharge_char=" 󰁾 ",
        #     full_char=" 󰁹 ",
        #     show_short_text=False,
        #     foreground=colors[1],
        #     background=colors[14],
        #     update_interval=5,
        # ),
        # pwl_d(),

        pwl_i(),
        widget.Systray(background=colors[14], icon_size=15, padding=5),
        pwl_d(),

        widget.Spacer(length=5),
    ]
    return widgets

widgets_list = init_widgets_list()

def init_screens():
    return [
        Screen(top=bar.Bar(widgets=widgets_list, size=26, margin=[8, 8, 4, 8], background=colors[2], opacity=0.9))
    ]

screens = init_screens()


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