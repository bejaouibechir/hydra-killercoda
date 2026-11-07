# Inspect the source and destination

First, let the automatic preparation finish. This command is part of the lesson;
it waits for PostgreSQL and all five tables. Continue only when it reports **Ready**.

`bash /root/lab/lab11-resources/wait-ready.sh`{{exec}}

`cd /root/lab/load-modes`{{exec}}

`/opt/hydra/bin/python /root/lab/lab11-resources/lab11.py ready`{{exec}}

`cat data/products.csv`{{exec}}

The same two incoming rows are used for all three normal loads:

| id | quantity |
| --- | --- |
| 2 | 25 |
| 3 | 30 |

ID 2 already exists in every target; ID 3 is new.

`cat jobs/append/sources.yaml jobs/append/destinations.yaml`{{exec}}

The modes write to separate tables so one experiment cannot change another's
starting state. The append table intentionally permits duplicate IDs; replace and
upsert use primary keys. An append into a table with a conflicting unique key
would fail, rather than update that key.

The three mode jobs leave `atomic` unspecified: PostgreSQL `replace` defaults
to atomic loading; `append` and `upsert` do not.
