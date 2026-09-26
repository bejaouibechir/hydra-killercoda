#!/bin/bash
cd /root/lab || exit 1
test -f dbjob/sources.yaml && test -f dbjob/.env.example && ! test -f dbjob/.env
