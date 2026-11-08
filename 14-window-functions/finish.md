# Window functions complete

Compare the four recorded outputs:

```bash
cd /root/lab/window-functions
for file in evidence/stage*.csv; do echo "$file"; cat "$file"; done
```

`row_number` and `cumsum` use the order within a partition. Whole-partition `sum` gives the same country total to every row of that country.
