#!/bin/bash -ex

wget https://api.steampowered.com/ISteamApps/GetAppList/v2/ -O apps.json
./parse_steam_apps_json.py
