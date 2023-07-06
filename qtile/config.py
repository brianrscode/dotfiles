import os
import subprocess
from typing import List  # noqa: F401
from libqtile import layout, bar, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule
from libqtile.command import lazy
from themes.colors import coloress
from libqtile.log_utils import logger

#mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')

############################################################
##################   Atajos de teclado    ##################
############################################################

keys = [Key(key[0], key[1], *key[2:]) for key in [
        # La mayoría de las combinaciones están en sxhkd, excepto estas...
        # SUPER + FUNCTION KEYS
        ([mod], "f", lazy.window.toggle_fullscreen()),
        ([mod], "q", lazy.window.kill()),

        # SUPER + SHIFT KEYS
        ([mod, "shift"], "q", lazy.window.kill()),
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

        # REDIMENSIONAR ARRIBA, ABAJO, IZQUIERDA, DERECHA
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

        # DISEÑO FLIP PARA MONADTALL/MONADWIDE
        ([mod, "shift"], "f", lazy.layout.flip()),

        # FLIP LAYOUT FOR BSP
        ([mod, "mod1"], "k", lazy.layout.flip_up()),
        ([mod, "mod1"], "j", lazy.layout.flip_down()),
        ([mod, "mod1"], "l", lazy.layout.flip_right()),
        ([mod, "mod1"], "h", lazy.layout.flip_left()),

        # MOVE WINDOWS UP OR DOWN BSP LAYOUT
        ([mod, "shift"], "k", lazy.layout.shuffle_up()),
        ([mod, "shift"], "j", lazy.layout.shuffle_down()),
        ([mod, "shift"], "h", lazy.layout.shuffle_left()),
        ([mod, "shift"], "l", lazy.layout.shuffle_right()),

        # MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
        ([mod, "shift"], "Up", lazy.layout.shuffle_up()),
        ([mod, "shift"], "Down", lazy.layout.shuffle_down()),
        ([mod, "shift"], "Left", lazy.layout.swap_left()),
        ([mod, "shift"], "Right", lazy.layout.swap_right()),

        # TOGGLE FLOATING LAYOUT
        ([mod, "shift"], "space", lazy.window.toggle_floating()),

    ]]

@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)

def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)

keys.extend([
    # MOVE WINDOW TO NEXT SCREEN
    Key([mod,"shift"], "Right", lazy.function(window_to_next_screen, switch_screen=True)),
    Key([mod,"shift"], "Left", lazy.function(window_to_previous_screen, switch_screen=True)),
])

##################################################
##################   Grupos     ##################
##################################################

group_labels = [" ", " ", "", "", " ", "󰍳 ",]
group_names = [str(i + 1) for i in range(len(group_labels))]
group_layouts = ["monadtall"] * len(group_labels)

groups = [Group(name=n, layout=l.lower(), label=la) for n, l, la in zip(group_names, group_layouts, group_labels)]

for i in groups:
    keys.extend([

        #CAMBIAR ESPACIOS DE TRABAJO
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

        # MUEVE LA VENTANA AL ESPACIO DE TRABAJO SELECCIONADO 1-10 Y PERMANECES EN EL ESPACIO DE TRABAJO
        #Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
        # MUEVE LA VENTANA AL ESPACIO DE TRABAJO SELECCIONADO 1-10 Y SIGUES LA VENTANA MOVIDA AL ESPACIO DE TRABAJO
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])

##################################################
##################   Lyout     ###################
##################################################

layout_config = { # Configuraciones de la ventana seleccionada
    "margin":5,
    "border_width":2,
    "border_focus": coloress["blue2"][0],
    "border_normal": coloress["inactive"][0]
}

# Forma como se colocan las ventanas
layouts = [layout.MonadTall(**layout_config)]

floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='Arcolinux-welcome-app.py'),
    Match(wm_class='Arcolinux-calamares-tool.py'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='Arandr'),  # para configurar las resoluciones de las pantallas
    Match(wm_class='nitrogen'),
    Match(wm_class='Galculator'),
    Match(wm_class='archlinux-logout'),
], fullscreen_border_width = 0, border_width = 0)

#################################################################
##################   WIDGETS PARA LA BARRA    ###################
#################################################################

base = lambda fg="color2", bg="color1":{
    "foreground": coloress[fg],
    "background": coloress[bg]
}

fuente = lambda ft="Mononoki Nerd Font", tam=16:{
    "font": ft,
    "fontsize": tam
}

def separator():
    return widget.Sep(linewidth = 1, padding = 10, **base())

def work_spaces():
    return [
        widget.GroupBox(
            **base(),
            **fuente(ft="FontAwesome"),
            margin_x = 0,
            padding_y = 6,
            padding_x = 5,
            borderwidth = 0,
            disable_drag = True,
            active = coloress["color9"],
            inactive = coloress["color5"],
            rounded = False,
            highlight_method = "text",
            this_current_screen_border=coloress["grupo"][0],
        ),
    ]

widgets_list = [
    *work_spaces(),
    separator(),
    widget.CurrentLayout(font="Mononoki Nerd Font",**base("color5"),), # **base("pink"),
    separator(),
    widget.WindowName(**fuente(tam=12), **base("color5"),),
    widget.OpenWeather(
        **base(),
        **fuente(),
        app_key = "7834197c2338888258f8cb94ae14ef49",
        location='Atlixco', format='{location_city}: {main_temp} °{units_temperature} {icon} - {weather_details}',
        language="es",
    ),
    separator(),
    widget.Battery(**base(), **fuente(), format='{char} {percent:2.0%}', notify_below=30,),
    separator(),
    widget.TextBox(**fuente(), **base("color5"), text="  ", padding=0,),
    widget.Clock(**base("color5"), **fuente(), format="%d/%m/%Y - %H:%M"),
    widget.Systray(background=coloress["color1"], icon_size=20, adding=4),
]

other_widgets_list = [
    *work_spaces(),
    separator(),
    widget.CurrentLayout(font="Mononoki Nerd Font",**base("pink"),),
    separator(),
    widget.WindowName(**fuente(tam=12), **base("color5"),),
]

screens = [Screen(top=bar.Bar(widgets=widgets_list, size=26, opacity=0.8)),]

xrandr = "xrandr | grep -w 'connected' | cut -d ' ' -f 2 | wc -l"
command = subprocess.run(
    xrandr,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
if command.returncode != 0:
    error = command.stderr.decode("UTF-8")
    logger.error(f"Failed counting monitors using {xrandr}:\n{error}")
    connected_monitors = 1
else:
    connected_monitors = int(command.stdout.decode("UTF-8"))

if connected_monitors > 1:
    for _ in range(1, connected_monitors):
        screens.append(Screen(top=bar.Bar(widgets=other_widgets_list, size=26, opacity=0.8)))

#############################################################
##################   MOUSE CONFIGURATION   ##################
#############################################################

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size())
]

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]

main = None
dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "focus" # or smart focus
wmname = "LG3D"
