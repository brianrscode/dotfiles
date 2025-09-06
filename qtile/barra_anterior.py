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