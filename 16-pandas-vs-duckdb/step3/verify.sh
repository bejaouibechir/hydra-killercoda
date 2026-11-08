#!/bin/bash
set -euo pipefail
if [ ! -f /tmp/hydra-lab16-ready ] || [ -f /tmp/hydra-lab16-failed ]; then
 cat /tmp/hydra-lab16-status 2>/dev/null || true
 echo 'Wait for Ready before using Check.'
 exit 1
fi
/opt/hydra/bin/python /root/lab/lab16-resources/benchmark.py check auto
