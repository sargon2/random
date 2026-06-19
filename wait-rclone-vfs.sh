#!/usr/bin/env bash
set -euo pipefail

INTERVAL="${INTERVAL:-5}"

while true; do
  stats="$(rclone rc vfs/stats)"

  queued="$(jq -r '.diskCache.uploadsQueued // 0' <<< "$stats")"
  active="$(jq -r '.diskCache.uploadsInProgress // 0' <<< "$stats")"
  errors="$(jq -r '.diskCache.erroredFiles // 0' <<< "$stats")"

  printf 'queued=%s uploading=%s errors=%s\n' "$queued" "$active" "$errors"

  if [[ "$errors" != "0" ]]; then
    echo "rclone VFS has errored files; check with: rclone rc vfs/queue"
    exit 2
  fi

  if [[ "$queued" == "0" && "$active" == "0" ]]; then
    echo "rclone VFS sync complete."
    exit 0
  fi

  sleep "$INTERVAL"
done
