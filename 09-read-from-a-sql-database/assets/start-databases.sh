#!/bin/bash
set -Eeuo pipefail
ASSETS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Refuse to replace containers, including those from an earlier setup attempt.
for name in hydra-lab09-mysql hydra-lab09-postgres; do
  if docker container inspect "$name" >/dev/null 2>&1; then
    echo "Container $name already exists. Inspect it before retrying setup." >&2
    exit 1
  fi
done
docker run -d --name hydra-lab09-mysql \
  -p 127.0.0.1:3309:3306 \
  -e MYSQL_ROOT_PASSWORD=lab09-root-only \
  -e MYSQL_DATABASE=shop -e MYSQL_USER=lab09_reader \
  -e MYSQL_PASSWORD=lab09-mysql-only \
  --mount "type=bind,source=$ASSETS/mysql-init.sql,target=/docker-entrypoint-initdb.d/01-products.sql,readonly" \
  mysql:8.0 &
mysql_pid=$!
docker run -d --name hydra-lab09-postgres \
  -p 127.0.0.1:5439:5432 \
  -e POSTGRES_USER=lab09_writer -e POSTGRES_PASSWORD=lab09-postgres-only \
  -e POSTGRES_DB=warehouse \
  --mount "type=bind,source=$ASSETS/postgres-init.sql,target=/docker-entrypoint-initdb.d/01-totals.sql,readonly" \
  postgres:16 &
postgres_pid=$!
status=0
wait "$mysql_pid" || status=1
wait "$postgres_pid" || status=1
exit "$status"
