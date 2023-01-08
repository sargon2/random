# Self-elevate to administrator
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-noexit -NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }

Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

choco upgrade -y 7zip
choco upgrade -y putty
choco upgrade -y googlechrome
choco upgrade -y dropbox
choco upgrade -y notepadplusplus
choco upgrade -y steam
# choco upgrade -y launchy
# choco upgrade -y anki
choco upgrade -y paint.net
choco upgrade -y audacity
# choco upgrade -y vlc
choco upgrade -y minecraft-launcher
# choco upgrade -y spacesniffer
# choco upgrade -y veracrypt
choco upgrade -y discord
choco upgrade -y microsoft-windows-terminal

wsl.exe --install
wsl --install -d Ubuntu
