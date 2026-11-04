#!/bin/bash
set -euo pipefail
[ -f /tmp/hydra-lab11-ready ] || exit 1
exec /opt/hydra/bin/python /root/lab/lab11-resources/exercise.py check partial
