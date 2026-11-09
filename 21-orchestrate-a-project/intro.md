# Orchestrate a project

Build a three-stage Hydra thread with four primary workflows. The middle stage runs sales and stock in parallel and repeats twice. A fifth workflow, kept outside the thread, supplies backup sales when PostgreSQL is unavailable.

You will run the project with PostgreSQL available, stop only this lab's database container, then observe the fallback. Finally restart the container and see the live route return.

Work in /root/lab/orchestrate-project. Wait for Ready before pressing Check. The Check scripts read only this lab's files and reports.
