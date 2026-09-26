#!/bin/bash
cd /root/lab || exit 1
hdrctl validate dbjob >/dev/null 2>&1
test $? -eq 0
