#!/bin/bash
set -e

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/tasktracker_$TIMESTAMP.sql"

mkdir -p $BACKUP_DIR

echo "📦 Creating backup..."
docker-compose exec -T postgres pg_dump -U tasktracker tasktracker > $BACKUP_FILE

echo "✅ Backup created: $BACKUP_FILE"
echo "📊 Backup size: $(du -h $BACKUP_FILE | cut -f1)"

# Keep only last 7 backups
ls -t $BACKUP_DIR/tasktracker_*.sql | tail -n +8 | xargs -r rm
echo "🧹 Old backups cleaned up"
