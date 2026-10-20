#!/bin/bash
cd /root/lab || exit 1
J=chainproject/jobs/job2
test -f $J/sources.yaml && test -f $J/destinations.yaml && test -f $J/pipeline.yaml \
  && grep -q "../job1/data/output.csv" $J/sources.yaml \
  && grep -q "from: src_job1_output" $J/pipeline.yaml \
  && grep -q "value > 150" $J/transformations.yaml
