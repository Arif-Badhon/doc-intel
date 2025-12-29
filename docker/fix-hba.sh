#!/bin/bash
set -e

echo "Fixing pg_hba.conf..."

# Create new pg_hba.conf with trust auth
cat > /var/lib/postgresql/data/pg_hba.conf << 'EOHBA'
local   all             all                                     trust
host    all             all             127.0.0.1/32            trust
host    all             all             ::1/128                 trust
local   replication     all                                     trust
host    replication     all             127.0.0.1/32            trust
host    replication     all             ::1/128                 trust
EOHBA

chmod 600 /var/lib/postgresql/data/pg_hba.conf

echo "pg_hba.conf fixed!"
