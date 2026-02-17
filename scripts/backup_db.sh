#!/bin/bash

# Environment variables
DB_USER=${POSTGRES_USER}
DB_NAME=${POSTGRES_DB}
DB_CONTAINER=<your_db_container_name>
BACKUP_DIR=/path/to/backups/db

# Create a timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create the backup
'docker exec $DB_CONTAINER pg_dump -U $DB_USER $DB_NAME | gzip > ${BACKUP_DIR}/backup_${TIMESTAMP}.sql.gz'

# Prune old backups (keep last 7 days)
find $BACKUP_DIR -type f -name '*.sql.gz' -mtime +7 -delete
