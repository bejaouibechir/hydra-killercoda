#!/bin/bash
echo "Installing Hydra ETL 0.16.0 and preparing lab 08..."
for _ in $(seq 1 300); do
  if [ -f /tmp/hydra-lab08-failed ]; then
    echo "Setup failed. Details:"
    tail -n 30 /tmp/hydra-lab08-setup.log
    exit 1
  fi
  if [ -f /tmp/hydra-lab08-ready ]; then
    source /opt/hydra/bin/activate
    export HYDRA_LANG=en
    cd /root/lab/csv-shapes || exit 1
    echo "Ready. You are in /root/lab/csv-shapes."
    echo "Three CSV formats, three jobs, the same expected rows."
    break
  fi
  sleep 1
done
if [ ! -f /tmp/hydra-lab08-ready ]; then
  echo "Setup is taking longer than expected. Inspect /tmp/hydra-lab08-setup.log."
  exit 1
fi
