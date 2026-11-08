# Compare length and errors

Count source lines of the SQL query, pandas script, and Hydra transformation steps. This counts only transformation logic, not Hydra's three job plumbing files. Then run the provided typo experiment: it changes `amount` to `amount_typo` in temporary copies and captures what each runtime reports. Your three working solutions are preserved.

```bash
cd /root/lab/three-ways
wc -l query.sql pandas_job.py job/transformations.yaml
/opt/hydra/bin/python /root/lab/lab17-resources/errors.py
cat output/errors.json
```

Compare SQLite's missing-column error, pandas' `KeyError`, and Hydra's step/available-columns message. Press **Check**.
