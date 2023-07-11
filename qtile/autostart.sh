#!/bin/bash

# Verifica si un proceso con el mismo nombre del comando pasado como argumento está en ejecución
# Si no se encuentra coincidencia con otro comando, se ejecuta en segundo plano
# Esto puede usarse para evitar ejecución duplicada de un comando o proceso específico
function run {
  if ! pgrep -x $(basename $1 | head -c 15) 1>/dev/null;
  then
    $@&
  fi
}

# ESTE AUTOSTART ES SOLO PARA INICIAR COSAS DENTRO DE QTILE

# Establezca su resolución nativa SI no existe en xrandr

# Averigüe el nombre de su monitor con xrandr o arandr (guarde y obtendrá esta línea)
#xrandr --output Virtual1 --primary --mode 1360x768 --pos 0x0 --rotate normal
#xrandr --output DP2 --primary --mode 1920x1080 --rate 60.00 --output LVDS1 --off &
#xrandr --output LVDS1 --mode 1366x768 --output DP3 --mode 1920x1080 --right-of LVDS1
#xrandr --output HDMI2 --mode 1920x1080 --pos 1920x0 --rotate normal --output HDMI1 --primary --mode 1920x1080 --pos 0x0 --rotate normal --output VIRTUAL1 --off
#autorandr horizontal

# cambia tu teclado si lo necesitas
# setxkbmap es -----------------------------------------------------------------------

#autostart ArcoLinux Welcome App
run dex $HOME/.config/autostart/arcolinux-welcome-app.desktop &

# inicie sxhkd para reemplazar las combinaciones de teclas nativas de Qtile
run sxhkd -c ~/.config/qtile/sxhkd/sxhkdrc &

# Poder ver las conexiones a internet
run nm-applet &
run pamac-tray &
run xfce4-power-manager &
numlockx on &
blueberry-tray &
picom --config $HOME/.config/qtile/scripts/picom.conf &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &

# Muestra el icono de volumen en la barra
run volumeicon &
# recupera el fondo de pantalla seteado
nitrogen --restore &
#run caffeine -a &
#run vivaldi-stable &
# run firefox &
# run thunar &
#run dropbox &
#run insync start &
#run spotify &
#run atom &
#run telegram-desktop &
