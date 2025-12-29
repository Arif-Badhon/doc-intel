#!/bin/bash
set -e

echo "Creating docintel_user with superuser privileges..."
psql -v ON_ERROR_STOP=0 -U postgres <<-EOSQL
    CREATE ROLE docintel_user WITH SUPERUSER LOGIN PASSWORD 'docintel_pass';
EOSQL

echo "Creating database..."
psql -v ON_ERROR_STOP=0 -U postgres <<-EOSQL
    CREATE DATABASE docintel_db OWNER docintel_user;
EOSQL

echo "Creating vector extension..."
psql -v ON_ERROR_STOP=1 -U docintel_user -d docintel_db <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS vector;
EOSQL

echo "Creating tables..."
psql -v ON_ERROR_STOP=1 -U docintel_user -d docintel_db <<-EOSQL
    CREATE TABLE IF NOT EXISTS documents (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS embeddings (
        id SERIAL PRIMARY KEY,
        document_id INTEGER REFERENCES documents(id),
        embedding vector(1536),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE INDEX IF NOT EXISTS embeddings_vector_idx ON embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
EOSQL

echo "Initialization complete!"
