#!/usr/bin/env bash
set -Eeuo pipefail

SRC_REMOTE="Dropbox"
DST_REMOTE="Google Drive"

SRC_PATH="/Apps/WorkFlowy"
DST_BASE_PATH="/backups/Workflowy"

TIMESTAMP="$(date '+%Y-%m-%d_%H-%M-%S')"
BACKUP_NAME="WorkFlowy_${TIMESTAMP}"

SRC="${SRC_REMOTE}:${SRC_PATH}"
DST="${DST_REMOTE}:${DST_BASE_PATH}/${BACKUP_NAME}"

DRY_RUN=false

usage() {
  cat <<EOF
Usage:
  $0 [--dry-run]

Copies the full WorkFlowy Dropbox backup folder:

  ${SRC}

to:

  ${DST}

Then verifies the copy, and only if verification succeeds, deletes the Dropbox source contents.

The Data/ and History/ folders are preserved inside the timestamped backup folder.
EOF
}

if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
elif [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
elif [[ $# -gt 0 ]]; then
  echo "Unknown argument: $1" >&2
  usage >&2
  exit 2
fi

command -v rclone >/dev/null 2>&1 || {
  echo "Error: rclone not found in PATH." >&2
  exit 1
}

require_remote() {
  local remote="$1"

  if ! rclone listremotes | grep -Fxq "${remote}:"; then
    echo "Error: rclone remote not found: ${remote}" >&2
    exit 1
  fi
}

require_remote "$SRC_REMOTE"
require_remote "$DST_REMOTE"

echo "Source:      $SRC"
echo "Destination: $DST"
echo

echo "Checking source folder exists..."
rclone lsd "$SRC" >/dev/null

echo "Checking expected WorkFlowy subfolders exist..."
rclone lsd "${SRC}/Data" >/dev/null
rclone lsd "${SRC}/History" >/dev/null

if [[ "$DRY_RUN" == true ]]; then
  echo
  echo "DRY RUN: would copy backup folder to Google Drive:"
  rclone copy "$SRC" "$DST" \
    --progress \
    --transfers 4 \
    --checkers 8 \
    --create-empty-src-dirs \
    --dry-run

  echo
  echo "DRY RUN: would delete Dropbox source contents after successful verification:"
  rclone delete "$SRC" --rmdirs --dry-run

  echo
  echo "Dry run complete. No files were copied or deleted."
  exit 0
fi

echo
echo "Creating destination folder..."
rclone mkdir "$DST"

echo
echo "Copying WorkFlowy backup folder..."
rclone copy "$SRC" "$DST" \
  --progress \
  --transfers 4 \
  --checkers 8 \
  --create-empty-src-dirs

echo
echo "Verifying copied backup..."
rclone check "$SRC" "$DST" \
  --one-way \
  --download

echo
echo "Verification succeeded."
echo "Deleting Dropbox source contents..."
rclone delete "$SRC" --rmdirs

echo
echo "Done."
echo "Backup archived to:"
echo "  $DST"
echo
echo "Dropbox source contents deleted from:"
echo "  $SRC"
