#!/bin/bash
set -euo pipefail
[ -f /tmp/hydra-lab07-ready ] || exit 1
exec /opt/hydra/bin/python /root/lab/lab07-resources/lab07.py check unknown-action
