#!/bin/bash
set -Eeuo pipefail
# This disposable service belongs only to lab 11. Never replace an existing one.
for attempt in $(seq 1 60); do
  docker info >/dev/null 2>&1 && break
  sleep 2
done
docker info >/dev/null
if docker container inspect hydra-lab11-postgres >/dev/null 2>&1; then
  echo 'The lab 11 database container already exists. Setup will not overwrite it.' >&2
  exit 1
fi
docker run -d --name hydra-lab11-postgres \
  -p 127.0.0.1:5441:5432 \
  -e POSTGRES_USER=lab11 \
  -e POSTGRES_PASSWORD=lab11-postgres-only \
  -e POSTGRES_DB=hydra_lab11 \
  postgres:16
