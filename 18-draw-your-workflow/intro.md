# Draw your workflow

This workflow has five named steps with different `depends_on` lists. Hydra executes its `delay` actions so the start and end times are easy to see. The lesson's timing wrapper records these times around the real workflow runner; Hydra's native result contains step durations but not their start/end timestamps.

Wait for **Ready**. No external service is used. All terminal commands below are part of the lesson.

```bash
cd /root/lab/draw-workflow
cat workflow.yaml
```
