#!/bin/bash
cd /root/lab || exit 1
grep -q "mode: upsert$" dbproject/jobs/job1/destinations.yaml
