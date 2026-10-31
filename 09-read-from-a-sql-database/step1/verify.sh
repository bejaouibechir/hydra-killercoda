#!/bin/bash
set -euo pipefail
[ -f /tmp/hydra-lab09-ready ] || exit 1
exec /opt/hydra/bin/python /root/lab/lab09-resources/lab09.py check connections
