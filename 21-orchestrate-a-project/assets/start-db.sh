#!/bin/bash
set -Eeuo pipefail
for attempt in $(seq 1 60); do docker info >/dev/null 2>&1 && break; sleep 2; done
docker info >/dev/null
if docker container inspect hydra-lab21-postgres >/dev/null 2>&1; then
 echo 'Lab 21 database already exists; refusing to overwrite it.' >&2
 exit 1
fi
docker run -d --name hydra-lab21-postgres -p 127.0.0.1:5445:5432  -e POSTGRES_USER=lab21 -e POSTGRES_PASSWORD=lab21-only -e POSTGRES_DB=hydra_lab21 postgres:16
for attempt in $(seq 1 120); do
 docker exec hydra-lab21-postgres pg_isready -U lab21 -d hydra_lab21 >/dev/null 2>&1 && exit 0
 sleep 2
done
echo 'PostgreSQL not ready' >&2;exit 1
