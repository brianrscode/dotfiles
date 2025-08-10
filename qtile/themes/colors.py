colores_comunes = {
    "black": ["#000", "#000"],
    "white": ["#FFF", "#FFF"],
    "activo": ["#f1ffff", "#f1ffff"],
    "inactivo": ["#4c566a", "#4c566a"],
    "gInactivo": ["#6B747A", "#6B747A"],
}

widgets = lambda w1="", w2="", w3="", w4="", w5="#0f101a":{
    "wid1": w1,
    "wid2": w2,
    "wid3": w3,
    "wid4": w4,
    "wid5": w5,
}

barra_y_borders = lambda barra=["#0f101a", "#0f101a"], selec=["#4AD9B0", "#4AD9B0"], focus=["#038C8C", "#038C8C"]: {
    "barra": barra,
    "gSelec": selec,
    "vFocus": focus,
}


noche = {
    **colores_comunes,
    **barra_y_borders(["#2F343F", "#2F343F"], ["#36c6ff", "#36c6ff"], ["#6272a4", "#6272a4"]),
    **widgets("#102C50", "#041C3C", "#051E31", "#040414"),
}

# Waifu de pelo rosa en campo
waifu1 = {
    **colores_comunes,
    **barra_y_borders(),
    **widgets("#4AD9B0", "#25A4BC", "#038C8C", "#04878C"),
}

waifu1c = {
    **colores_comunes,
    **barra_y_borders(),
    **widgets("#F2916D", "#038C8C", "#D96055", "#04878C"),
}


# Waifu viendo el cielo
waifu2 = {
    **colores_comunes,
    **barra_y_borders(["#0f101a", "#0f101a"], ["#3878B2", "#3878B2"], ["#03738C", "#03738C"]),
    **widgets("#3878B2", "#F2AB6D", "#0A2140", "#00010D"),
}



# Waifu con guitarra
waifu3 = {
    **colores_comunes,
    **barra_y_borders(["#131827", "#131827"], ["#D13649", "#D13649"], ["#D9A577", "#D9A577"]),
    **widgets("#F2D4C2", "#D13649", "#D9A577", "#BF213E"),
}



# Waifu samurai
waifu4 = {  # Waifu 1 rosa
    **colores_comunes,
    **barra_y_borders(["#0f101a", "#0f101a"], ["#D96055", "#D96055"], ["#D96055", "#D96055"]),
    **widgets("#F2916D", "#C37C66", "#D96055", "#D92929"),
}

mocha = {
    **colores_comunes,
    **barra_y_borders(barra=["#1e1e2e", "#1e1e2e"]),
    **widgets("#9399b2", "#7f849c", "#45475a", "#313244"),
}

temas = {
    "noche": noche,
    "waifu1": waifu1,
    "waifu1c": waifu1c,
    "waifu2": waifu2,
    "waifu3": waifu3,
    "waifu4": waifu4,
    "mocha": mocha,
}

def get_tema(nombre="mocha"):
    return temas.get(nombre, mocha)


coloress = get_tema("mocha")