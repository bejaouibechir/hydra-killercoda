#!/bin/bash
set -euo pipefail
if [ ! -f /tmp/hydra-lab18-ready ] || [ -f /tmp/hydra-lab18-failed ]; then
 cat /tmp/hydra-lab18-status 2>/dev/null || true
 echo 'Wait for Ready before using Check.'
 exit 1
fi
/opt/hydra/bin/python /root/lab/lab18-resources/check.py report
