import subprocess
from libqtile import layout, bar, widget, hook
from libqtile.config import Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from os import path
from libqtile.utils import guess_terminal

from themes.colors import get_active_theme

from libqtile import qtile


terminal = guess_terminal()

mod = "mod4"
mod1 = "alt"
mod2 = "control"
qtile_path = path.join(path.expanduser("~"), ".config", "qtile")
powerMenu = f'bash "{path.join(qtile_path, "powermenu.sh")}"'
theme = get_active_theme()


def openCalendar():
    qtile.cmd_spawn("gsimplecal")


def pavucontrol():
    qtile.cmd_spawn("pavucontrol")


def openHtop():
    qtile.cmd_spawn("alacritty -e htop")


def openMenu():
    qtile.cmd_spawn(powerMenu)


left = ""
right = ""


############################################################
##################   Atajos de teclado    ##################
############################################################

keys = [
    Key(key[0], key[1], *key[2:])
    for key in [
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
        (
            [mod, "control"],
            "l",
            lazy.layout.grow_right(),
            lazy.layout.grow(),
            lazy.layout.increase_ratio(),
            lazy.layout.delete(),
        ),
        (
            [mod, "control"],
            "Right",
            lazy.layout.grow_right(),
            lazy.layout.grow(),
            lazy.layout.increase_ratio(),
            lazy.layout.delete(),
        ),
        (
            [mod, "control"],
            "h",
            lazy.layout.grow_left(),
            lazy.layout.shrink(),
            lazy.layout.decrease_ratio(),
            lazy.layout.add(),
        ),
        (
            [mod, "control"],
            "Left",
            lazy.layout.grow_left(),
            lazy.layout.shrink(),
            lazy.layout.decrease_ratio(),
            lazy.layout.add(),
        ),
        (
            [mod, "control"],
            "k",
            lazy.layout.grow_up(),
            lazy.layout.grow(),
            lazy.layout.decrease_nmaster(),
        ),
        (
            [mod, "control"],
            "Up",
            lazy.layout.grow_up(),
            lazy.layout.grow(),
            lazy.layout.decrease_nmaster(),
        ),
        (
            [mod, "control"],
            "j",
            lazy.layout.grow_down(),
            lazy.layout.shrink(),
            lazy.layout.increase_nmaster(),
        ),
        (
            [mod, "control"],
            "Down",
            lazy.layout.grow_down(),
            lazy.layout.shrink(),
            lazy.layout.increase_nmaster(),
        ),
    ]
]

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
    if qtile.current_window is None:
        return
    i = qtile.groups.index(qtile.current_group)
    prev_group = qtile.groups[(i - 1) % len(qtile.groups)].name
    qtile.current_window.togroup(prev_group)


@lazy.function
def window_to_next_group(qtile):
    if qtile.current_window is None:
        return
    i = qtile.groups.index(qtile.current_group)
    next_group = qtile.groups[(i + 1) % len(qtile.groups)].name
    qtile.current_window.togroup(next_group)


@lazy.function
def window_to_previous_screen(qtile, switch_group=True, switch_screen=True):
    if qtile.current_window is None:
        return
    i = qtile.screens.index(qtile.current_screen)
    if i != 0 and qtile.screens[i - 1].group is not None:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen:
            qtile.cmd_to_screen(i - 1)


@lazy.function
def window_to_next_screen(qtile, switch_group=True, switch_screen=True):
    if qtile.current_window is None:
        return
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens) and qtile.screens[i + 1].group is not None:
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen:
            qtile.cmd_to_screen(i + 1)


keys.extend(
    [  # Cambiar entre pantallas
        Key([mod, "shift"], "Left", window_to_previous_screen),
        Key([mod, "shift"], "Right", window_to_next_screen),
    ]
)

##################################################
##################   Grupos     ##################
##################################################

# group_labels = [" ", " ", "", "", " ", "󰍳 "]
group_labels = ["", "", "", "", "", ""]
group_names = [str(i + 1) for i in range(len(group_labels))]
group_layouts = ["monadtall"] * len(group_labels)

groups = [
    Group(name=n, layout=l.lower(), label=la)
    for n, l, la in zip(group_names, group_layouts, group_labels)
]

for i in groups:
    keys.extend(
        [
            Key([mod], i.name, lazy.group[i.name].toscreen()),  # Ir al grupo i
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name),
                lazy.group[i.name].toscreen(),
            ),  # Mover la ventana al grupo i
        ]
    )

keys.extend(
    [
        Key([mod], "Tab", lazy.screen.next_group()),  # Siguiente grupo
        Key([mod, "shift"], "Tab", lazy.screen.prev_group()),  # Anteriror grupo
    ]
)

##################################################
##################   Layout     ##################
##################################################

layout_config = {
    "margin": 2,
    "border_width": 2,
    "border_focus": theme["border_focus"],
    "border_normal": theme["border_normal"],
}

layouts = [layout.MonadTall(**layout_config)]

floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="Arandr"),
        Match(wm_class="nitrogen"),
        Match(wm_class="thunar"),
    ],
    fullscreen_border_width=0,
        border_width=0,
)

#################################################################
##################   WIDGETS PARA LA BARRA    ###################
#################################################################

def init_widgets_defaults():
    return dict(
        font="Noto Sans Bold",
        padding=3,
        fontsize=12,
        foreground=theme["segment_fg"],
        background=theme["bar_background"],
    )


widget_defaults = init_widgets_defaults()


def init_widgets_list():
    widgets = [
        widget.Sep(linewidth=0, padding=6, background=theme["bar_background"]),
        widget.Image(
            filename="~/.config/qtile/icons/python.png",
            margin=3,
            background=theme["bar_background"],
            mouse_callbacks={"Button1": openMenu},
        ),
        widget.Sep(linewidth=0, padding=6, background=theme["bar_background"]),
        
        ### Grupos ###
        widget.GroupBox(
            font="FontAwesome",
            borderwidth=3,
            active=theme["group_active"],
            inactive=theme["group_inactive"],
            rounded=False,
            highlight_method="line",
            highlight_color=theme["bar_background"],
            this_current_screen_border=theme["group_this_screen_border"],
            this_screen_border=theme["border_focus"],
            other_screen_border=theme["bar_background"],
            foreground=theme["segment_fg"],
            background=theme["bar_background"],
            disable_drag=True,
            use_mouse_wheel=True,
            padding_x=4,
        ),
        widget.Sep(padding=6, linewidth=0, background=theme["bar_background"]),
        
        ### Window Name ###
        widget.WindowName(
            font="Noto Sans Bold",
            foreground=theme["segment_fg"],
            background=theme["bar_background"],
            fontsize=10,
            empty_group_string="Desktop",
            max_chars=80,
        ),
        widget.Spacer(),

        ### Systray ###
        widget.Systray(background=theme.get("color3", theme["bar_background"]), padding=10),
        widget.Sep(linewidth=0, padding=6, background=theme.get("color3", theme["bar_background"])),

        ### Volume ###
        widget.Sep(padding=9, linewidth=0, background=theme.get("color3", theme["bar_background"])),
        widget.TextBox(
            text=" ", 
            font="FontAwesome",
            foreground=theme.get("color3fg", theme["segment_fg"]),
            background=theme.get("color3", theme["bar_background"]),
            fontsize=14,
            padding=0,
            mouse_callbacks={"Button1": pavucontrol},
        ),
        widget.Volume(
            foreground=theme.get("color3fg", theme["segment_fg"]),
            background=theme.get("color3", theme["bar_background"]),
        ),
        widget.Sep(padding=6, linewidth=0, background=theme.get("color3", theme["bar_background"])),

        ### Clock (Date) ###
        widget.Sep(padding=6, linewidth=0, background=theme.get("color1", theme["bar_background"])),
        widget.TextBox(
            foreground=theme.get("color1fg", theme["segment_fg"]),
            background=theme.get("color1", theme["bar_background"]),
            text=" ",
            font="FontAwesome",
            mouse_callbacks={"Button1": openCalendar},
        ),
        widget.Clock(
            foreground=theme.get("color1fg", theme["segment_fg"]),
            background=theme.get("color1", theme["bar_background"]),
            format="%d/%m/%y",
            mouse_callbacks={"Button1": openCalendar},
        ),
        widget.Sep(padding=6, linewidth=0, background=theme.get("color1", theme["bar_background"])),
        
        ### Clock (Time) ###
        widget.TextBox(
            foreground=theme.get("color5fg", theme["segment_fg"]),
            background=theme.get("color5", theme["bar_background"]),
            text=" ", 
            font="FontAwesome",
            mouse_callbacks={"Button1": openCalendar},
        ),
        widget.Clock(
            foreground=theme.get("color5fg", theme["segment_fg"]),
            background=theme.get("color5", theme["bar_background"]),
            format="%A - %H:%M",
            mouse_callbacks={"Button1": openCalendar},
        ),
        widget.Sep(padding=6, linewidth=0, background=theme.get("color5", theme["bar_background"])),
    ]
    return widgets


widgets_list = init_widgets_list()


def init_screens():
    return [
        Screen(
            top=bar.Bar(
                widgets=widgets_list,
                size=26,
                margin=0,
                background=theme["bar_background"],
                opacity=0.9,
            )
        )
    ]
##################   MOUSE CONFIGURATION   ##################
#############################################################

mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
]


@hook.subscribe.startup_once
def start_once():
    subprocess.call([path.join(qtile_path, "autostart.sh")])


@hook.subscribe.startup
def start_always():
    subprocess.Popen(["xsetroot", "-cursor_name", "left_ptr"])


floating_types = ["notification", "toolbar", "splash", "dialog"]


@hook.subscribe.client_new
def set_floating(window):
    if (
        window.window.get_wm_transient_for()
        or window.window.get_wm_type() in floating_types
    ):
        window.floating = True


main = None
auto_fullscreen = True
bring_front_click = True
cursor_warp = False
dgroups_key_binder = None
dgroups_app_rules = []
focus_on_window_activation = "smart"
follow_mouse_focus = True
wmname = "LG3D"
