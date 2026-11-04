# Load modes and atomicity

Compare `append`, `replace`, and `upsert` using one CSV file. Then deliberately
fail a larger load at batch 3 and examine what remains in PostgreSQL.

The environment prepares Hydra, two CSV files, five independent jobs, and a
dedicated PostgreSQL database. Each target starts with the same two rows:

| id | quantity |
| --- | --- |
| 1 | 10 |
| 2 | 20 |

Allow setup to report **Ready** before continuing. Downloading the database image
and installing Hydra can take several minutes.

**Duration:** approximately 15 minutes. Run each variant once, in lesson order.
