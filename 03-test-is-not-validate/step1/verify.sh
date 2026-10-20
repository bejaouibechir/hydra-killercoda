#!/bin/bash
cd /root/lab || exit 1
grep -q "mode: upsret" dbproject/jobs/job1/destinations.yaml
