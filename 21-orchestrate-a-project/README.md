# 21 — Orchestrate a project

Killercoda lab for LAB lab-03-04 in 03-workflows.md. It has four primary workflows in a three-stage thread and one fallback workflow file outside the thread. Stage 2 is parallel and loops twice. The live sales job reads from a dedicated PostgreSQL container; its fallback reads a local CSV when source_available('sales_db') is false.

Setup waits for deployed resources, installs published hydra-etl[postgres]==0.19.1, creates the project, starts one PostgreSQL 16 container on 127.0.0.1:5445, seeds lab21.sales, and signals Ready. The learner stops and restarts only hydra-lab21-postgres. Check scripts read only the lab's project files and reports.

Local review precedes any commit or push.
