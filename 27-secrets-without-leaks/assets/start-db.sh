#!/bin/bash
set -Eeuo pipefail
ROOT=/root/lab/secrets-without-leaks
for attempt in $(seq 1 60); do
  docker info >/dev/null 2>&1 && break
  sleep 2
done
docker info >/dev/null
if docker container inspect hydra-lab27-postgres >/dev/null 2>&1; then
  echo 'The lab 27 database container already exists; refusing to overwrite it.' >&2
  exit 1
fi
export POSTGRES_PASSWORD=$(sed -n 's/^db.password=//p' "$ROOT/.hydra/secrets")
[ -n "$POSTGRES_PASSWORD" ]
docker run -d --name hydra-lab27-postgres \
  -p 127.0.0.1:5447:5432 \
  -e POSTGRES_USER=lab27 \
  -e POSTGRES_PASSWORD \
  -e POSTGRES_DB=lab27db \
  postgres:16
unset POSTGRES_PASSWORD
for attempt in $(seq 1 120); do
  if docker exec hydra-lab27-postgres pg_isready -U lab27 -d lab27db >/dev/null 2>&1; then
    docker exec -i hydra-lab27-postgres psql -v ON_ERROR_STOP=1 -U lab27 -d lab27db <<'SQL'
CREATE TABLE products (id integer PRIMARY KEY, name text NOT NULL);
INSERT INTO products (id, name) VALUES (1, 'Mug'), (2, 'Lamp');
SQL
    exit 0
  fi
  sleep 2
done
echo 'PostgreSQL did not become ready' >&2
exit 1
