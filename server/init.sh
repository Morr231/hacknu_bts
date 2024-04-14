#!/bin/bash

set -a
source .env
set +a

echo "Run migrations"
alembic upgrade head
