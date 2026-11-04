#!/bin/bash
echo "Installing Hydra and starting MySQL and PostgreSQL for lab 09..."
echo "Please wait for Ready before starting the exercises."
previous_status=""
for elapsed in $(seq 1 600); do
  status="$(cat /tmp/hydra-lab09-status 2>/dev/null || true)"
  if [ -n "$status" ] && [ "$status" != "$previous_status" ]; then
    echo "$status"
    previous_status="$status"
  elif [ $((elapsed % 30)) -eq 0 ]; then
    echo "Setup is still running ($elapsed seconds). ${status:-Waiting for the setup script...}"
  fi
  if [ -f /tmp/hydra-lab09-failed ]; then
    echo "Setup failed. Details:"
    tail -n 40 /tmp/hydra-lab09-setup.log
    echo "Diagnostic: docker ps -a"
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
  echo "Latest status: ${status:-no status received from the setup script}"
  tail -n 20 /tmp/hydra-lab09-setup.log 2>/dev/null || true
  exit 1
fi
