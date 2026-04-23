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

echo "Actualizando el sistema..."
pacman -Syu --noconfirm

install_pkg() {
	if ! pacman -S --needed --noconfirm "$1"; then
		echo "⚠️ No se pudo instalar: $1. Continuando con el siguiente paquete..."
	fi
}

echo "Instalando paquetes base y de desarrollo..."
install_pkg base-devel
install_pkg xorg-server
install_pkg xorg-apps
install_pkg sxhkd
install_pkg git
install_pkg neovim
install_pkg lazygit
install_pkg ripgrep
install_pkg fd
install_pkg fzf
install_pkg tree-sitter-cli

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

echo "Instalando paquetes adicionales para Qtile..."
install_pkg networkmanager
install_pkg network-manager-applet
install_pkg pavucontrol
install_pkg alsa-utils
install_pkg playerctl
install_pkg brightnessctl
install_pkg flameshot
install_pkg udiskie
install_pkg xfce4-power-manager
install_pkg numlockx
install_pkg picom
install_pkg volumeicon
install_pkg dmenu
install_pkg rofi
install_pkg pamixer
install_pkg gsimplecal
install_pkg thunar
install_pkg noto-fonts
install_pkg ttf-font-awesome

echo "Verificando/Instalando yay (AUR helper)..."
if ! command -v yay &> /dev/null; then
	install_pkg base-devel
	install_pkg git
	cd /tmp
	rm -rf yay
	sudo -u $SUDO_USER git clone https://aur.archlinux.org/yay.git
	cd yay
	sudo -u $SUDO_USER makepkg -si --noconfirm
fi

echo "Instalando dependencias desde AUR..."
sudo -u $SUDO_USER yay -S --noconfirm nitrogen || echo "⚠️ No se pudo instalar: nitrogen"
sudo -u $SUDO_USER yay -S --noconfirm cbatticon || echo "⚠️ No se pudo instalar: cbatticon"

echo "✅ Todo listo. Ahora puedes iniciar sesión en Qtile desde tu display manager."
