# 09 - Read from a SQL database

Whitebook reference: **LAB lab-02-02**, chapter **02-jobs-part1.md**.

Status: local preparation for author review. No commit or publication is automatic.

## Requested scope

This lab follows the author's revised scenario: **MySQL source -> transformation -> PostgreSQL destination**. It replaces the placeholder's two-source/seven-day-query idea.

- Source: `shop.product(id, name, unit_price, quantity)`.
- Destination: `warehouse.public.product_totals(id, product_name, total)`.
- Calculation: `total = quantity * unit_price`.
- Five sample products include decimal prices and a zero quantity.
- Three guided steps: inspect connections, create transformations, transfer and verify.
- The supplied job uses `replace`; rerunning keeps five rows.

## Resources

`assets/` contains the manifests, reference transformation, SQL initialization scripts, expected results, helper, database launcher, and editor extension.

`setup/` installs pinned Hydra with MySQL/PostgreSQL drivers, starts dedicated containers, waits for seeded tables and reports failures.

The learner creates `transformations.yaml`. The other manifests are supplied. Checks validate data, not only exit codes.

Synthetic passwords are published only for this disposable lab. MySQL's reader has SELECT permission. Database ports bind to localhost: 3309 and 5439.

## Local review

With Python 3.10+:

```bash
python -m pip install -r requirements.txt
python tests/check_offline.py
```

For the complete database test, start a dedicated pair of containers:

```bash
docker compose -f assets/docker-compose.yml up -d --wait
python tests/check_live.py
```

The live test requires the destination to be empty, populates only this lab's dedicated table, validates all rows, and tests a second run. It also checks that incorrect totals and names are rejected before restoring the correct result.

After reviewing the test output:

```bash
docker compose -f assets/docker-compose.yml down -v
```

This cleanup applies only to this lab's Compose project.

For manual exploration, set `HYDRA_LAB09_ROOT` to a new or empty directory, then run `python assets/lab09.py prepare`. Keep that variable set for subsequent helper commands. The helper refuses to overwrite a non-empty directory.

## Killercoda review

After publication is approved, check the complete Ubuntu setup and Editor tab in Killercoda. Setup log: `/tmp/hydra-lab09-setup.log`.
