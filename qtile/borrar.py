from themes.colors import waifu1Colorful

coloress = waifu1Colorful

# print(type(coloress))
# print(coloress)


basicos = {
    "black": ["#000", "#000"],
    "white": ["#FFF", "#FFF"],
    "activo": ["#f1ffff", "#f1ffff"],
    "inactivo": ["#4c566a", "#4c566a"],
}
waifu1Bright = {
    "primero": "#F24B59",
    "segundo": "#F2295F",
    "tercero": "#038C8C",
    "cuarto": "#F29D35",
    "quinto": "#F27166",
}
waifu1Mued = {
    "primero": "#BF4158",
    "segundo": "#038C8C",
    "tercero": "#4AD9B0",
    "cuarto": "#F2D9BB",
    "quinto": "#F27166",
}

for n, v in basicos.items():
    waifu1Bright[n] = v
    waifu1Mued[n] = v

print(waifu1Bright)
print("Espacio")
print(waifu1Mued)
    
