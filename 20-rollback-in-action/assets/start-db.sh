#!/bin/bash
set -Eeuo pipefail
for attempt in $(seq 1 60); do
  docker info >/dev/null 2>&1 && break
  sleep 2
done
docker info >/dev/null
if docker container inspect hydra-lab20-postgres >/dev/null 2>&1; then
  echo 'The lab 20 database container already exists; refusing to overwrite it.' >&2
  exit 1
fi
docker run -d --name hydra-lab20-postgres \
  -p 127.0.0.1:5443:5432 \
  -e POSTGRES_USER=lab20 \
  -e POSTGRES_PASSWORD=lab20-postgres-only \
  -e POSTGRES_DB=hydra_lab20 \
  postgres:16
for attempt in $(seq 1 120); do
  docker exec hydra-lab20-postgres pg_isready -U lab20 -d hydra_lab20 >/dev/null 2>&1 && exit 0
  sleep 2
done
echo 'PostgreSQL did not become ready' >&2
exit 1
