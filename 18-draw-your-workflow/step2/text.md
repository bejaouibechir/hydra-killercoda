# Run and read the times

Run the actual Hydra workflow through the timing wrapper. It records each step's UTC `started_at`, `ended_at`, and duration in `report.json`. Read the report and find the two roots that overlap.

```bash
cd /root/lab/draw-workflow
/opt/hydra/bin/python /root/lab/lab18-resources/measure.py
cat report.json
```

Then press **Check**.
