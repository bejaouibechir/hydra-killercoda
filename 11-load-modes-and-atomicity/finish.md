# What you verified

You loaded one CSV file with append, replace, and upsert, starting from equivalent
data in independent tables.

You then caused a real PostgreSQL constraint failure halfway through a 400-row
load. Without atomicity, the first 200 incoming rows remained. With atomicity,
the destination kept exactly its two original rows.

The final checks compare actual values, not just row counts. Logs and observed
results remain available in `/root/lab/load-modes/evidence/`.
