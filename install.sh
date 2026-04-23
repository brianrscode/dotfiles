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
NVIM_REPO="https://github.com/brianrscode/nvim.git"
NVIM_CONFIG_DIR="$CONFIG_DIR/nvim"

echo "Actualizando el sistema..."
pacman -Syu --noconfirm

install_pkg() {
	if ! pacman -S --needed --noconfirm "$1"; then
		echo "⚠️ No se pudo instalar: $1. Continuando con el siguiente paquete..."
	fi
}

echo "=============================================="
echo "1) Instalando base critica del sistema"
echo "=============================================="
install_pkg xorg-server
install_pkg git
install_pkg networkmanager

echo "=============================================="
echo "2) Instalando base esencial para Qtile"
echo "=============================================="
install_pkg sxhkd
install_pkg network-manager-applet
install_pkg rofi
install_pkg dmenu
install_pkg picom
install_pkg thunar
install_pkg pavucontrol
install_pkg alsa-utils
install_pkg pamixer
install_pkg playerctl
install_pkg brightnessctl
install_pkg flameshot
install_pkg udiskie
install_pkg xfce4-power-manager
install_pkg numlockx
install_pkg volumeicon
install_pkg gsimplecal

echo "=============================================="
echo "3) Instalando y aplicando dotfiles"
echo "=============================================="

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
	echo "Copiando configuracion de qtile a ~/.config/..."
	mkdir -p "$CONFIG_DIR"
	rm -rf "$CONFIG_DIR/qtile"
	cp -r "$DOTFILES_DIR/qtile" "$CONFIG_DIR/"
	chown -R $SUDO_USER:$SUDO_USER "$CONFIG_DIR/qtile"
else
	echo "No se encontro la carpeta 'qtile' en el repositorio clonado."
fi

if [ -d "$DOTFILES_DIR/fonts" ]; then
	echo "Instalando fuentes para todos los usuarios..."
	mkdir -p /usr/local/share/fonts
	cp -r "$DOTFILES_DIR/fonts/." /usr/local/share/fonts/
	fc-cache -f
else
	echo "No se encontro la carpeta 'fonts' en el repositorio clonado."
fi

install_pkg noto-fonts
install_pkg ttf-font-awesome

echo "=============================================="
echo "4) Instalando configuracion de Neovim"
echo "=============================================="
install_pkg neovim

mkdir -p "$CONFIG_DIR"

if [ -d "$NVIM_CONFIG_DIR" ]; then
	BACKUP_DIR="$CONFIG_DIR/nvim.bak-$(date +%Y%m%d-%H%M%S)"
	echo "Respaldando configuracion existente de Neovim en: $BACKUP_DIR"
	mv "$NVIM_CONFIG_DIR" "$BACKUP_DIR"
	chown -R $SUDO_USER:$SUDO_USER "$BACKUP_DIR"
fi

echo "Clonando configuracion de Neovim..."
sudo -u $SUDO_USER git clone "$NVIM_REPO" "$NVIM_CONFIG_DIR"
chown -R $SUDO_USER:$SUDO_USER "$NVIM_CONFIG_DIR"

echo "=============================================="
echo "5) Instalando herramientas de desarrollo"
echo "=============================================="
install_pkg base-devel
install_pkg lazygit
install_pkg ripgrep
install_pkg fd
install_pkg fzf
install_pkg xorg-apps
install_pkg tree-sitter-cli
install_pkg nodejs
install_pkg npm

echo "=============================================="
echo "6) Instalando extras opcionales (AUR)"
echo "=============================================="
INSTALL_AUR="n"
if [ -r /dev/tty ]; then
	read -r -p "¿Deseas instalar paquetes opcionales desde AUR con yay? [s/N]: " INSTALL_AUR < /dev/tty
else
	echo "No hay terminal interactiva. Se omitira la instalacion de paquetes AUR."
fi

if [[ "$INSTALL_AUR" =~ ^[sSyY]$ ]]; then
	echo "Verificando/Instalando yay (AUR helper)..."
	if ! command -v yay &> /dev/null; then
		install_pkg base-devel
		install_pkg git
		cd /tmp
		rm -rf yay
		sudo -u $SUDO_USER git clone https://aur.archlinux.org/yay.git
		cd yay
		sudo -u $SUDO_USER makepkg -si --noconfirm || echo "⚠️ No se pudo instalar yay. Se omiten paquetes AUR."
	fi

	if command -v yay &> /dev/null; then
		echo "Instalando dependencias desde AUR..."
		sudo -u $SUDO_USER yay -S --needed --noconfirm nitrogen || echo "⚠️ No se pudo instalar: nitrogen"
		sudo -u $SUDO_USER yay -S --needed --noconfirm cbatticon || echo "⚠️ No se pudo instalar: cbatticon"
	fi
else
	echo "Se omitio la instalacion de paquetes AUR."
fi

echo "✅ Todo listo. Ahora puedes iniciar sesión en Qtile desde tu display manager."
