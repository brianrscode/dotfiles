#!/bin/bash

# Verifica si se ejecuta como root
if [[ "$EUID" -ne 0 ]]; then
  echo "Por favor, ejecuta este script como root (usa sudo)"
  exit 1
fi

# Variables
USER_HOME=$(eval echo ~${SUDO_USER})
CONFIG_DIR="$USER_HOME/.config"
DOTFILES_REPO="https://github.com/brianrscode/dotfiles.git"
DOTFILES_DIR="$USER_HOME/dotfiles"
XINITRC="$USER_HOME/.xinitrc"

echo "Actualizando el sistema..."
pacman -Syu --noconfirm

echo "Instalando paquetes base..."
pacman -S --noconfirm \
  xorg-server \
  xorg-xinit \
  xorg-apps \
  qtile \
  alacritty \
  sxhkd \
  arandr \
  git

echo "Verificando archivo .xinitrc..."
if [ ! -f "$XINITRC" ]; then
  echo "Creando .xinitrc..."
  touch "$XINITRC"
  chown $SUDO_USER:$SUDO_USER "$XINITRC"
fi

if ! grep -Fxq "exec qtile start" "$XINITRC"; then
  echo "Agregando 'exec qtile start' a .xinitrc..."
  echo "exec qtile start" >> "$XINITRC"
else
  echo "La línea 'exec qtile start' ya existe en .xinitrc."
fi

echo "Clonando el repositorio de dotfiles..."
cd "$USER_HOME"
sudo -u $SUDO_USER git clone "$DOTFILES_REPO"

if [ -d "$DOTFILES_DIR/qtile" ]; then
  echo "Copiando configuración de qtile a ~/.config/..."
  mkdir -p "$CONFIG_DIR"
  rm -rf "$CONFIG_DIR/qtile"
  cp -r "$DOTFILES_DIR/qtile" "$CONFIG_DIR/"
  chown -R $SUDO_USER:$SUDO_USER "$CONFIG_DIR/qtile"
else
  echo "No se encontró la carpeta 'qtile' en el repositorio clonado."
fi

echo "Instalando paquetes adicionales..."
pacman -S --noconfirm \
  pavucontrol \
  brightnessctl \
  network-manager-applet \
  flameshot \
  udiskie \
  xfce4-power-manager \
  numlockx \
  blueberry \
  picom \
  volumeicon \
  cbatticon \
  nitrogen \
  dmenu \
  rofi \
  pamixer \
  lxappearance


echo "✅ Todo listo. Ahora puedes iniciar Qtile con 'startx'."
