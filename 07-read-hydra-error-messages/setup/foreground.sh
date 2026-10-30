#!/bin/bash
echo "Installing Hydra ETL 0.16.0 and preparing lab 07..."
for _ in $(seq 1 300); do
  if [ -f /tmp/hydra-lab07-failed ]; then
    echo "Setup failed. Details:"
    tail -n 30 /tmp/hydra-lab07-setup.log
    exit 1
  fi
  if [ -f /tmp/hydra-lab07-ready ]; then
    source /opt/hydra/bin/activate
    export HYDRA_LANG=en
    cd /root/lab/error-messages || exit 1
    echo "Ready. You are in /root/lab/error-messages."
    echo "All exercises use --dry-run; no webhook is called."
    break
  fi
  sleep 1
done
if [ ! -f /tmp/hydra-lab07-ready ]; then
  echo "Setup is taking longer than expected. Inspect /tmp/hydra-lab07-setup.log."
  exit 1
fi
