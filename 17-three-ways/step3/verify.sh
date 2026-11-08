#!/bin/bash
set -euo pipefail
if [ ! -f /tmp/hydra-lab17-ready ] || [ -f /tmp/hydra-lab17-failed ]; then
 cat /tmp/hydra-lab17-status 2>/dev/null || true
 echo 'Wait for Ready before using Check.'
 exit 1
fi
exec /opt/hydra/bin/python /root/lab/lab17-resources/lab17.py check 3
