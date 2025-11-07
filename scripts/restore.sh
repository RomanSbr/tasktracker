#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Usage: ./scripts/restore.sh <backup-file>"
  echo "Available backups:"
  ls -1 backups/
  exit 1
fi

BACKUP_FILE=$1

if [ ! -f "$BACKUP_FILE" ]; then
  echo "❌ Backup file not found: $BACKUP_FILE"
  exit 1
fi

read -p "⚠️  This will overwrite the current database. Continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Cancelled."
  exit 1
fi

echo "📥 Restoring from $BACKUP_FILE..."
docker-compose exec -T postgres psql -U tasktracker tasktracker < $BACKUP_FILE

echo "✅ Database restored successfully!"
