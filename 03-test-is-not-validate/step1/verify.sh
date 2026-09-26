#!/bin/bash
test -f dbjob/sources.yaml && test -f dbjob/.env.example && ! test -f dbjob/.env
