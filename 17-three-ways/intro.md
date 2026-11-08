# Three ways to transform the same CSV

Write the same logic in SQL (SQLite), pandas, and Hydra DSL: normalize country and status, keep paid orders, retain the latest order per customer, then sum revenue by country. The source has spaces, mixed case, a cancelled order, and two empty amounts.

You will compare the output, source length and the errors from one misspelled column. Wait for **Ready**. All terminal commands in this scenario belong to the lesson.

```bash
cd /root/lab/three-ways
cat data/orders.csv
```
