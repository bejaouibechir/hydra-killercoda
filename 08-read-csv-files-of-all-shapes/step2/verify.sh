#!/bin/bash
set -euo pipefail
[ -f /tmp/hydra-lab08-ready ] || exit 1
exec /opt/hydra/bin/python /root/lab/lab08-resources/lab08.py check semicolon
