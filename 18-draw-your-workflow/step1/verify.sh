#!/bin/bash
set -euo pipefail
if [ ! -f /tmp/hydra-lab18-ready ] || [ -f /tmp/hydra-lab18-failed ]; then
 cat /tmp/hydra-lab18-status 2>/dev/null || true
 echo 'Wait for Ready before using Check.'
 exit 1
fi
/opt/hydra/bin/python -c "from hydra_etl.workflow.parser import load_workflow; w=load_workflow('/root/lab/draw-workflow/workflow.yaml'); assert len(w.steps)==5; print('PASS: five valid workflow steps')"
