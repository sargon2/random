#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

MINECRAFT_USER="minecraft"
MINECRAFT_DATA_ROOT="/srv/minecraft"
MINECRAFT_DATA_LOCATION="/srv/minecraft/server1"

if ! id "$MINECRAFT_USER" >/dev/null 2>&1; then
  sudo useradd --system --create-home --shell /usr/sbin/nologin "$MINECRAFT_USER"
fi

sudo install -d \
  -o "$MINECRAFT_USER" \
  -g "$MINECRAFT_USER" \
  -m 750 \
  "$MINECRAFT_DATA_ROOT"

sudo install -d \
  -o "$MINECRAFT_USER" \
  -g "$MINECRAFT_USER" \
  -m 750 \
  "$MINECRAFT_DATA_LOCATION"

export MINECRAFT_UID="$(id -u "$MINECRAFT_USER")"
export MINECRAFT_GID="$(id -g "$MINECRAFT_USER")"
export MINECRAFT_DATA_LOCATION

docker compose up -d
