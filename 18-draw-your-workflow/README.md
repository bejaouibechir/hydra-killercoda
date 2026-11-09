# LAB lab-03-01 — Draw your workflow

Killercoda scenario 18 for `03-workflows.md`. The five-step workflow uses Hydra's built-in `delay` action to create an observable DAG without external services. A small wrapper subclasses the real WorkflowRunner to record step start/end timestamps in `report.json`; it does not change any engine file. The lesson shows a complete five-step boxed ASCII graph; the learner recreates it in `graph.txt` using the terminal. Check validates the drawing and timing order.
