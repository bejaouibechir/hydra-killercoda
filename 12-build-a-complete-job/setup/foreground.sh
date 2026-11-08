#!/bin/bash
set -euo pipefail
for attempt in $(seq 1 90); do
  [ -s /root/lab/lab12-resources/wait-ready.sh ] && break
  sleep 1
done
exec bash /root/lab/lab12-resources/wait-ready.sh
