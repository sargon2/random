#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

MINECRAFT_USER="minecraft"
MINECRAFT_DATA_ROOT="/srv/minecraft"
MINECRAFT_DATA_LOCATION="/srv/minecraft/server1"

export MINECRAFT_UID="$(id -u "$MINECRAFT_USER")"
export MINECRAFT_GID="$(id -g "$MINECRAFT_USER")"
export MINECRAFT_DATA_LOCATION

docker compose logs

echo "(Detach with ^p follwed by ^q.)"

docker compose attach minecraft
