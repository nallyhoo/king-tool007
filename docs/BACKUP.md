
# Backup & Disaster Recovery Guide

This guide outlines the strategy and procedures for backing up your application's data and recovering from a potential disaster.

## 1. Database Backups (PostgreSQL)

Automated daily backups of your PostgreSQL database are essential.

### Backup Script (`scripts/backup_db.sh`)

This script will dump the contents of your database to a compressed file.

```bash
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
```

### Automation (Cron Job)

Run this script daily using a cron job.

```bash
# Edit the crontab
crontab -e

# Add this line to run the backup at 2 AM every day
0 2 * * * /path/to/your/scripts/backup_db.sh
```

## 2. Video File Backups (MinIO/S3)

Your video files should be backed up to a separate, off-site location.

-   **MinIO**: Use the `mc mirror` command to replicate your MinIO buckets to another MinIO instance or a compatible cloud storage service (like Backblaze B2 or Wasabi).

    ```bash
    mc alias set source http://localhost:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}
    mc alias set destination https://s3.us-west-001.backblazeb2.com <B2_KEY_ID> <B2_APP_KEY>
    mc mirror --overwrite source/videos destination/videos
    ```

-   **AWS S3**: If you are using S3, enable **Cross-Region Replication** to automatically copy your files to a bucket in another AWS region.

## 3. Configuration Backups

Your configuration files (`.env`, `docker-compose.prod.yml`, Nginx configs) should be stored in a private Git repository.

## 4. Recovery Procedures

In the event of a total server failure, here are the steps to recover:

1.  **Provision a New Server**: Follow the [Self-Hosted Deployment Guide](./SELF_HOSTED.md) to set up a new server.
2.  **Restore Git Repository**: Clone your Git repository with all the configuration files.
3.  **Restore Database**: 
    -   Start the database container (`docker-compose up -d db`).
    -   Copy the latest backup file to the server.
    -   Run the restore command:

        ```bash
        gunzip < backup.sql.gz | docker exec -i <db_container_name> psql -U $POSTGRES_USER -d $POSTGRES_DB
        ```

4.  **Restore Video Files**:
    -   If using MinIO with `mc mirror`, reverse the mirror direction to restore files to the new MinIO instance.
    -   If using S3, you can access the files from the replica bucket.
5.  **Start the Application**: Run `make up-prod` to start all services.
