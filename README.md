# script.service.hdmipowersave
Kodi Add-on Script - HDMI On/Off Powersave Mode

## Installation
1. Download latest release: https://github.com/devshans/script.service.hdmipowersave/releases/download/0.1.1/script.service.hdmipowersave.zip
2. Upload to raspberry pi using FTP.
3. Navigate to: Settings -> Addons -> Install from Zip File
4. Select "script.service.hdmipowersave.zip"

## Overview
Kodi/XBMC python add-on - Automates turning off HDMI output after user-defined extended idle time. Triggers after the default Kodi screensaver so that no other settings need to be changed and original screensaver functionality remains intact.

Designed for Raspberry Pi running OSMC and tested on Raspberry Pi 1 Model B+ with OSMC 2015.11-1.

## Future Work
Supports Linux by toggling DPMS settings but not fully tested.

Windows support - Have placeholder code stubs using pywin32.
