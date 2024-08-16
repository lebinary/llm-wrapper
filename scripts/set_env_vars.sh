#!/bin/bash
set -euxo pipefail

# Load environment variables from a .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo ".env file not found"
    exit 1
fi
