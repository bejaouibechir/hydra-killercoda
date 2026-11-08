# Clean a messy file

You will clean five CSV records with `trim`, `clean`, `deduplicate`, and `fill_null`. The file has extra spaces, mixed case, a duplicate ID, and a missing amount. After each run, inspect `output/result.csv` and save a checked snapshot of that stage.

Setup installs Hydra 0.19.1 and places the file in `/root/lab/clean-file/data`. Wait for **Ready** before starting. All terminal commands in this lab are lesson commands.

```bash
cd /root/lab/clean-file
cat data/orders.csv
```
