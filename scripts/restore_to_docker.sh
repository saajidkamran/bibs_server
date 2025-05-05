#!/bin/bash

set -e  # Stop on any error

echo "🧹 Shutting down and cleaning up existing containers..."
docker-compose down

echo "🔨 Rebuilding Docker images from scratch..."
docker-compose build --no-cache

echo "🚀 Starting containers in detached mode..."
docker-compose up -d

echo "⏳ Waiting for MySQL container to initialize..."
sleep 10  # wait for MySQL to start up

echo "💾 Dumping local MySQL DB to backups/backup.sql..."
mysqldump -u root bibs_server_db > backups/backup.sql

echo "📦 Copying SQL backup into Docker MySQL container..."
docker cp backups/backup.sql bibs-db:/backup.sql

echo "🔄 Restoring DB inside container..."
docker exec -i bibs-db sh -c 'mysql -uroot -proot bibs_server_db < /backup.sql'

echo "✅ All done! Project is up and DB restored."
