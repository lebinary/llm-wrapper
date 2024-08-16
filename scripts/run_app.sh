#!/bin/bash
set -euxo pipefail

# Check required env variables
if [ -z "${OPENAI_API_KEY:-}" ]; then
    echo "OPENAI_API_KEY is not set. Please check your .env file."
    exit 1
fi
if [ -z "${DATABASE_URL:-}" ]; then
    echo "DATABASE_URL is not set. Please check your .env file."
    exit 1
fi

# Start app
poetry run alembic upgrade head
poetry run python main.py
