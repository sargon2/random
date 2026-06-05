#!/usr/bin/env bash
set -euo pipefail

HOST="sargon-openclaw.exe.xyz"
REMOTE_ROOT="~/.openclaw"
LOCAL_BACKUP_DIR="$HOME/Dropbox/openclaw/backups"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
REMOTE_TAR="/tmp/openclaw-backup-$STAMP.tar.gz"
LOCAL_TAR="$LOCAL_BACKUP_DIR/openclaw-backup-$STAMP.tar.gz"

mkdir -p "$LOCAL_BACKUP_DIR"

ssh "$HOST" "
  set -euo pipefail
  tar -czf '$REMOTE_TAR' \
    --exclude='*/node_modules' \
    --exclude='*/.git' \
    --exclude='*/.cache' \
    --exclude='*/cache' \
    --exclude='*/tmp' \
    --exclude='*/temp' \
    --exclude='*/logs' \
    --exclude='*/dist' \
    --exclude='*/build' \
    --exclude='*/__pycache__' \
    --exclude='*/.venv' \
    --exclude='*/venv' \
    -C "\$HOME" \
    .openclaw/workspace \
    .openclaw/skills \
    .openclaw/plugin-skills 2>/tmp/openclaw-backup-warnings-$STAMP.log || true

  if [ ! -s '$REMOTE_TAR' ]; then
    echo 'Backup tarball was not created or is empty' >&2
    exit 1
  fi
"

scp "$HOST:$REMOTE_TAR" "$LOCAL_TAR"
ssh "$HOST" "rm -f '$REMOTE_TAR' /tmp/openclaw-backup-warnings-$STAMP.log"

sha256sum "$LOCAL_TAR" > "$LOCAL_TAR.sha256"
ls -lh "$LOCAL_TAR" "$LOCAL_TAR.sha256"

echo "$LOCAL_TAR"
