#!/bin/bash
set -euo pipefail
if [ ! -f /tmp/hydra-lab15-ready ] || [ -f /tmp/hydra-lab15-failed ]; then
 cat /tmp/hydra-lab15-status 2>/dev/null || true
 echo 'Wait for Ready before using Check.'
 exit 1
fi
exec /opt/hydra/bin/python /root/lab/lab15-resources/lab15.py check 3
