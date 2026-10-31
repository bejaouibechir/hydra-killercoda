#!/bin/bash
echo "Installing Hydra and starting MySQL and PostgreSQL for lab 09..."
for _ in $(seq 1 600); do
  if [ -f /tmp/hydra-lab09-failed ]; then
    echo "Setup failed. Details:"
    tail -n 40 /tmp/hydra-lab09-setup.log
    exit 1
  fi
  if [ -f /tmp/hydra-lab09-ready ]; then
    source /opt/hydra/bin/activate
    export HYDRA_LANG=en
    cd /root/lab/sql-products || exit 1
    echo "Ready. You are in /root/lab/sql-products."
    echo "MySQL: five products. PostgreSQL: an empty product_totals table."
    break
  fi
  sleep 1
done
if [ ! -f /tmp/hydra-lab09-ready ]; then
  echo "Setup exceeded ten minutes. Inspect /tmp/hydra-lab09-setup.log."
  exit 1
fi
