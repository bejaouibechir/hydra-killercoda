# Normalize status case

`clean` converts `status` to lowercase. The existing trim step remains first.

Read the stage template, then put its YAML in `job/transformations.yaml`. You may edit the file directly; the template gives a working reference.

```bash
cat /root/lab/lab13-resources/stage2.yaml
cp /root/lab/lab13-resources/stage2.yaml job/transformations.yaml
hdrctl run job
cat output/result.csv
```

Compare the output with the input and the previous checked snapshot in `evidence/`. Then press **Check**.
