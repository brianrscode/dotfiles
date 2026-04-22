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
	base-devel \
	xorg-server \
	xorg-xinit \
	xorg-apps \
	alacritty \
	sxhkd \
	arandr \
	git \
	neovim \
	lazygit \
	ripgrep \
	fd \
	fzf \
	tree-sitter-cli

echo "Verificando archivo .xinitrc..."
if [ ! -f "$XINITRC" ]; then
	echo "Creando .xinitrc..."
	touch "$XINITRC"
	chown $SUDO_USER:$SUDO_USER "$XINITRC"
fi

if ! grep -Fxq "exec qtile start" "$XINITRC"; then
	echo "Agregando 'exec qtile start' a .xinitrc..."
	echo "exec qtile start" >>"$XINITRC"
else
	echo "La línea 'exec qtile start' ya existe en .xinitrc."
fi

if [ -d "$DOTFILES_DIR" ]; then
	echo "Actualizando el repositorio de dotfiles..."
	cd "$DOTFILES_DIR"
	sudo -u $SUDO_USER git pull
else
	echo "Clonando el repositorio de dotfiles..."
	cd "$USER_HOME"
	sudo -u $SUDO_USER git clone "$DOTFILES_REPO"
fi

if [ -d "$DOTFILES_DIR/qtile" ]; then
	echo "Copiando configuración de qtile a ~/.config/..."
	mkdir -p "$CONFIG_DIR"
	rm -rf "$CONFIG_DIR/qtile"
	cp -r "$DOTFILES_DIR/qtile" "$CONFIG_DIR/"
	chown -R $SUDO_USER:$SUDO_USER "$CONFIG_DIR/qtile"
else
	echo "No se encontró la carpeta 'qtile' en el repositorio clonado."
fi

if [ -d "$DOTFILES_DIR/fonts" ]; then
	echo "Instalando fuentes para todos los usuarios..."
	mkdir -p /usr/local/share/fonts
	cp -r "$DOTFILES_DIR/fonts/." /usr/local/share/fonts/
	fc-cache -f
else
	echo "No se encontró la carpeta 'fonts' en el repositorio clonado."
fi

echo "Instalando paquetes adicionales..."
pacman -S --noconfirm \
	networkmanager \
	pavucontrol \
	alsa-utils \
	playerctl \
	htop \
	thunar \
	xfce4-settings \
	xfce4-appfinder \
	xfce4-taskmanager \
	brightnessctl \
	network-manager-applet \
	flameshot \
	udiskie \
	xfce4-power-manager \
	numlockx \
	blueberry \
	picom \
	volumeicon \
	dmenu \
	rofi \
	pamixer \
	lxappearance \
	gsimplecal \
	noto-fonts \
	ttf-font-awesome

echo "Verificando/Instalando yay (AUR helper)..."
if ! command -v yay &> /dev/null; then
	pacman -S --needed --noconfirm base-devel git
	cd /tmp
	rm -rf yay
	sudo -u $SUDO_USER git clone https://aur.archlinux.org/yay.git
	cd yay
	sudo -u $SUDO_USER makepkg -si --noconfirm
fi

echo "Instalando dependencias desde AUR..."
sudo -u $SUDO_USER yay -S --noconfirm \
	nitrogen \
	cbatticon

echo "✅ Todo listo. Ahora puedes iniciar Qtile con 'startx'."
