#!/bin/bash
hdrctl validate brokenjob >/dev/null 2>&1
test $? -eq 0
