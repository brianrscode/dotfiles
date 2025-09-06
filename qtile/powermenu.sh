#!/bin/bash

# Definir las opciones con íconos
options="󰒲  Suspender\n󰜉  Reiniciar\n󰐥  Apagar"

# Mostrar el menú y capturar la opción seleccionada
selected=$(echo -e "$options" | rofi -dmenu -p "" -l 3 -theme "$HOME/.config/qtile/rofi/configpowermenu.rasi")

# Extraer solo la palabra clave (segunda palabra) ignorando íconos
action=$(echo "$selected" | awk '{print $2}')

# Ejecutar la acción según la selección
case "$action" in
    Suspender)
        systemctl suspend
        ;;
    Reiniciar)
        reboot
        ;;
    Apagar)
        shutdown now
        ;;
    *)
        echo "Opción no válida o cancelada"
        ;;
esac