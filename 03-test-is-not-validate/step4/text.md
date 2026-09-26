# hdrctl run is the one that actually tries

`hdrctl run dbjob`{{exec}}

```
Pipeline FAILED in 0.0s

Cause:
SecretResolutionError: Variable d'environnement manquante: DB_HOST
```

Two full "checks" passed, and the first thing that actually touches `DB_HOST` is `run` itself — and it fails in French, from an internal resolver, because nothing ever loaded `.env`.

Copying `.env.example` to `.env` (`cp dbjob/.env.example dbjob/.env`) would get past this specific error — and immediately hit the real one: there is no MySQL server listening anywhere in this lab, so `run` would then fail again, this time trying to actually open a connection. That second failure is the one `test`'s own "(connection not tested in test mode)" was warning you about all along.
