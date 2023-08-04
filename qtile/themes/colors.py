colores_comunes = {
    "black": ["#000", "#000"],
    "white": ["#FFF", "#FFF"],
    "activo": ["#f1ffff", "#f1ffff"],
    "inactivo": ["#4c566a", "#4c566a"],
    "gInactivo": ["#6B747A", "#6B747A"],
}

widgets = lambda w1="", w2="", w3="", w4="", w5="":{
    "wid1": w1,
    "wid2": w2,
    "wid3": w3,
    "wid4": w4,
    "wid5": w5,
}

#################################################
#################     Noche     #################
#################################################

noche = {
    **colores_comunes,
    "barra": ["#2F343F", "#2F343F"],
    "gSelec": ["#36c6ff", "#36c6ff"],
    "vFocus": ["#6272a4", "#6272a4"],
    **widgets("#102C50", "#041C3C", "#051E31", "#040414", "#0f101a"),
}


##################################################
#################     Waifu1     #################
##################################################

# Waifu de pelo rosa en campo
waifu1Completo = {
    "color1": "#ECD5A6",
    "color2": "#AB3742",
    "color3": "#2E2420",
    "color4": "#E29559",
    "color5": "#F16056",
    "color6": "#6D4749",
    "color7": "#04878C",
    "color8": "#4BCCB7",
    "color9": "#C086B5",
    "color10": "#434934",
    "color11": "#7FD4B5",
    "color12": "#AB6B41",
    "color13": "#CF5E81",
    "color14": "#37594E",
    "color15": "#25A4BC",
    "color16": "#FCBE54",
    "color17": "#446750",
    "color18": "#398980",
    "color19": "#46B8A4",
    "color20": "#348CAC"
    # "primero": "#BF4158",
    # "segundo": "#038C8C",-
    # "tercero": "#4AD9B0",-
    # "cuarto": "#F29D35",
    # "quinto": "#F27166",-
    # "primero": "#734854",
    # "segundo": "#A63F65",
    # "cuarto": "#364035",
    # "quinto": "#59551D",
    # "primero": "#F24B59",
    # "segundo": "#F2295F",
    # "cuarto": "#F2D9BB",
}

waifu1 = {
    **colores_comunes,
    "barra": ["#0f101a", "#0f101a"],  # #0f101a
    "gSelec": ["#4AD9B0", "#4AD9B0"],
    "vFocus": ["#038C8C", "#038C8C"],
    **widgets("#4AD9B0", "#25A4BC", "#038C8C", "#04878C", "#0f101a"),
}

waifu1c = {
    **colores_comunes,
    "barra": ["#0f101a", "#0f101a"],  # #0f101a
    "gSelec": ["#4AD9B0", "#4AD9B0"],
    "vFocus": ["#038C8C", "#038C8C"],
    **widgets("#F2916D", "#038C8C", "#D96055", "#04878C", "#0f101a"),
}

##################################################
#################     Waifu2     #################
##################################################

# Waifu viendo el cielo
waifu2Completo = {
    "color1": "#BE7F7C",
    "color2": "#30638F",
    "color3": "#63455E",
    "color4": "#0B0A15",
    "color5": "#164070",
    "color6": "#0C2547",
    "color7": "#1B4F78",
    "color8": "#3878B2",
    "color9": "#F9DC97",
    "color10": "#BA5325",
    "color11": "#363351",
    "color12": "#786579",
    "color13": "#0D325D",
    "color14": "#091731",
    "color15": "#5DA1B8",
    "color16": "#113D61",
    "color17": "#A03133",
    "color18": "#1E2A4B",
    "color19": "#AEB4BE",
    "color20": "#0A0B2C",
    # "segundo": "#0A2140",
    # "primero": "#00010D",
    # "tercero": "#0D4C73",
    # "cuarto": "#03738C",
    # "segundo": "#03658C",
    # "tercero": "#F2AB6D",
    # "cuarto": "#F2490C",
    # "quinto": "#D96459",
    # "tercero": "#F2921D",
}

waifu2 = {
    **colores_comunes,
    "barra": ["#0f101a", "#0f101a"],  # #0f101a
    "gSelec": ["#3878B2", "#3878B2"],
    "vFocus": ["#03738C", "#03738C"],
    **widgets("#3878B2", "#F2AB6D", "#0A2140", "#00010D", "#0f101a"),
}

##################################################
#################     Waifu3     #################
##################################################

# Waifu con guitarra
waifu3Completo = {
    "color1": "#ECE2D6",
    "color2": "#847878",
    "color3": "#D13649",
    "color4": "#9DA9A7",
    "color5": "#373C4A",
    "color6": "#CA9677",
    "color7": "#BE8960",
    "color8": "#131827",
    "color9": "#635960",
    "color10": "#6B747A",
    "color11": "#211C20",
    "color12": "#DBAB85",
    "color13": "#66697C",
    "color14": "#7E1C39",
    "color15": "#1E2031",
    "color16": "#4F4A52",
    "color17": "#4D5E6B",
    "color18": "#959CAC",
    "color19": "#261322",
    "color20": "#485364",
    # "primero": "#BF213E",
    # "segundo": "#73123F",
    # "tercero": "#141A26",
    # "cuarto": "#D9A577",
    # "quinto": "#F2D4C2",
}

waifu3 = {
    **colores_comunes,
    "barra": ["#131827", "#131827"],  # #0f101a
    "gSelec": ["#D13649", "#D13649"],
    "vFocus": ["#D9A577", "#D9A577"],
    **widgets("#F2D4C2", "#D13649", "#D9A577", "#BF213E", "#141A26"),
}

##################################################
#################     Waifu4     #################
##################################################

# Waifu samurai
waifu4Completo = {
    "color1": "#C37C66",
    "color2": "#7B4A44",
    "color3": "#4D322F",
    "color4": "#BA2927",
    "color5": "#E7DED6",
    "color6": "#839D94",
    "color7": "#EED295",
    "color8": "#131113",
    "color9": "#7C789E",
    "color10": "#4E5C5E",
    "color11": "#271819",
    "color12": "#313B40",
    "color13": "#372324",
    "color14": "#CF621F",
    "color15": "#343531",
    "color16": "#3F4465",
    "color17": "#23272D",
    "color18": "#182422",
    "color19": "#171B24",
    "color20": "#04090A",
    # "primero": "#261014",
    # "segundo": "#D9A566",
    # "tercero": "#F2916D",
    # "cuarto": "#D96055",
    # "quinto": "#D92929",
    # "tercero": "#F21B1B",
}

waifu4 = {  # Waifu 1 rosa
    **colores_comunes,
    "barra": ["#0f101a", "#0f101a"],  # #0f101a
    "gSelec": ["#D96055", "#D96055"],
    "vFocus": ["#D96055", "#D96055"],
    **widgets("#F2916D", "#C37C66", "#D96055", "#D92929", "#0f101a"),
}
