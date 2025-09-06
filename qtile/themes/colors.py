#######################################################
############### Ajustes predeterminados ###############
#######################################################

class TemaBase:
    colores_comunes = {
        "black": ["#000", "#000"],
        "white": ["#FFF", "#FFF"],
        "activo": ["#f1ffff", "#f1ffff"],
        "inactivo": ["#4c566a", "#4c566a"],
        "gInactivo": ["#6B747A", "#6B747A"],
    }

    def __init__(
            self,
            barra: list[str, str]=None,
            selec: list[str, str]=None,
            focus: list[str, str]=None,
            widget1: str="",
            widget2: str="",
            widget3: str="",
            widget4: str="",
            widget5: str="#0f101a"
            ):

        # Elementos comunes
        self.colores = dict(self.colores_comunes)  # Copia para no mutar la clase base
        
        # Barra de navegación y bordes de las ventanas
        self.colores.update({
            "barra": barra or ["#0f101a", "#0f101a"],
            "gSelec": selec or ["#4AD9B0", "#4AD9B0"],
            "vFocus": focus or ["#038C8C", "#038C8C"],
        })

        # Widgets
        self.colores.update({
            "wid1": widget1,
            "wid2": widget2,
            "wid3": widget3,
            "wid4": widget4,
            "wid5": widget5,
        })

    def obtener_colores(self):
        return self.colores


#######################################################
######################## TEMAS ########################
#######################################################

class Noche(TemaBase):
    def __init__(self):
        super().__init__(
            barra=["#2F343F", "#2F343F"],
            selec=["#36c6ff", "#36c6ff"],
            focus=["#6272a4", "#6272a4"],
            widget1="#102C50",
            widget2="#041C3C",
            widget3="#051E31",
            widget4="#040414"
        )


class Waifu(TemaBase):
    def __init__(self):
        super().__init__(
            widget1="#F2916D",
            widget2="#038C8C",
            widget3="#D96055",
            widget4="#04878C"
        )

class Waifu2(TemaBase):
    def __init__(self):
        super().__init__(
            barra=["#0f101a", "#0f101a"],
            selec=["#3878B2", "#3878B2"],
            focus=["#03738C", "#03738C"],
            widget1="#3878B2",
            widget2="#F2AB6D",
            widget3="#0A2140",
            widget4="#00010D"
        )

class Waifu3(TemaBase):
    def __init__(self):
        super().__init__(
            barra=["#131827", "#131827"],
            selec=["#D13649", "#D13649"],
            focus=["#D9A577", "#D9A577"],
            widget1="#F2D4C2",
            widget2="#D13649",
            widget3="#D9A577",
            widget4="#BF213E"
        )

class Waifu4(TemaBase):
    def __init__(self):
        super().__init__(
            barra=["#0f101a", "#0f101a"],
            selec=["#D96055", "#D96055"],
            focus=["#D96055", "#D96055"],
            widget1="#F2916D",
            widget2="#C37C66",
            widget3="#D96055",
            widget4="#D92929"
        )

class Mocha(TemaBase):
    def __init__(self):
        super().__init__(
            barra=["#0F0F1C", "#0F0F1C"], # #1a1b26 #0F0F1C  #1A1C31
            widget1="#BEBEBE",# 9399b2
            widget2="#949494", # 7f849c
            widget3="#7A7A7A", # 45475a
            widget4="#545454", # 313244
            widget5="#3C3C3C"
        )


#######################################################
################## Gestión de temas ###################
#######################################################

temas = {
    "noche": Noche,
    "waifu": Waifu,
    "waifu2": Waifu2,
    "waifu3": Waifu3,
    "waifu4": Waifu4,
    "mocha": Mocha,
}


def get_tema(nombre="mocha"):
    tema_clase = temas.get(nombre, Mocha)
    return tema_clase().obtener_colores()


# Ejemplo de uso
colores = get_tema("mocha")
