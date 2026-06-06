#!/bin/bash -e

cd "$(dirname "$0")"

export MINECRAFT_UID=`id -u`
export MINECRAFT_GID=`id -g`

docker compose up
