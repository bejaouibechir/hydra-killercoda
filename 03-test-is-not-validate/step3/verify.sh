#!/bin/bash
hdrctl validate dbjob >/dev/null 2>&1
test $? -eq 0
