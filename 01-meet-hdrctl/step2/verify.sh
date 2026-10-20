#!/bin/bash
cd /root/lab || exit 1
J=myproject/jobs/job1
test -f $J/sources.yaml && test -f $J/destinations.yaml && test -f $J/pipeline.yaml \
  && test -f myproject/workflows/workflow1.yaml && test -d myproject/.hydra
