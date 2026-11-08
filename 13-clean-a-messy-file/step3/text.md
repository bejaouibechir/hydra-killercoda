# Remove duplicate IDs

`deduplicate` keeps the last record for each `id`; the two records with ID 2 become one.

Read the stage template, then put its YAML in `job/transformations.yaml`. You may edit the file directly; the template gives a working reference.

```bash
cat /root/lab/lab13-resources/stage3.yaml
cp /root/lab/lab13-resources/stage3.yaml job/transformations.yaml
hdrctl run job
cat output/result.csv
```

Compare the output with the input and the previous checked snapshot in `evidence/`. Then press **Check**.
