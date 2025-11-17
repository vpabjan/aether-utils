#!/bin/bash
sudo pacman -S --needed git base-devel dbus rust dmenu
git clone https://aur.archlinux.org/iwmenu.git
cd iwmenu
makepkg -si
