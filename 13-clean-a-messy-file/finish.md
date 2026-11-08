# File cleaned

You have four snapshots in `evidence/`, one after each operation. Compare them to see which change each step made:

```bash
cd /root/lab/clean-file
for file in evidence/stage*.csv; do echo "$file"; cat "$file"; done
```

The final file has four IDs, lowercase status values, trimmed text, and a zero for the missing amount.
