# Scaffold a database job

`hdrctl init dbjob --template mysql`{{exec}}

`find dbjob -type f`{{exec}}

`cat dbjob/sources.yaml`{{exec}}

`cat dbjob/.env.example`{{exec}}

Only `.env.example` exists — nobody has copied it to `.env` yet, so `DB_HOST`, `DB_USER` and `DB_PASS` are not set anywhere. That is deliberate: keep it this way for the next two steps.
