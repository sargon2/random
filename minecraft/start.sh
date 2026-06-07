#!/bin/bash -e

cd "$(dirname "$0")"

export MINECRAFT_UID=`id -u`
export MINECRAFT_GID=`id -g`

export MINECRAFT_DATA_LOCATION="/srv/minecraft/server1"

docker compose up
