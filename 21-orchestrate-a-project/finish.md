# What you observed

The thread ordered three stages. Sales and stock shared a parallel stage, and the loop replayed that stage twice. Stopping PostgreSQL made the source probe choose the backup sales workflow before the live sales workflow started. The project still completed. Restarting the container restored the live route.

The backup workflow is a separate file outside the thread's four primary workflows.
