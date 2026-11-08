#!/bin/bash
set -Eeuo pipefail
for attempt in $(seq 1 60); do
  docker info >/dev/null 2>&1 && break
  sleep 2
done
docker info >/dev/null
if docker container inspect hydra-lab12-mysql >/dev/null 2>&1; then
  echo 'The lab 12 database already exists. Setup will not overwrite it.' >&2
  exit 1
fi
docker run -d --name hydra-lab12-mysql \
  -p 127.0.0.1:3313:3306 \
  -e MYSQL_ROOT_PASSWORD=lab12-root-only \
  -e MYSQL_DATABASE=shop -e MYSQL_USER=etl \
  -e MYSQL_PASSWORD=lab12-etl-only \
  mysql:8.4
