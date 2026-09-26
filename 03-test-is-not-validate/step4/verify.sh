#!/bin/bash
cd /root/lab || exit 1
if hdrctl run dbjob >/dev/null 2>&1; then
  exit 1
else
  exit 0
fi
