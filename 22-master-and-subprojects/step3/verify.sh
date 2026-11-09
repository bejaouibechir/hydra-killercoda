#!/bin/bash
set -euo pipefail
if [ ! -f /tmp/hydra-lab22-ready ] || [ -f /tmp/hydra-lab22-failed ]; then
 cat /tmp/hydra-lab22-status 2>/dev/null || true
 echo 'Wait for Ready before using Check.'
 exit 1
fi
/opt/hydra/bin/python /root/lab/lab22-resources/lab22.py check cycle
