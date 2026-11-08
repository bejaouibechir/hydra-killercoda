# Three ways to combine data

Compare the recorded outputs:

```bash
cd /root/lab/combine-data
for file in evidence/stage*.csv; do echo "$file"; cat "$file"; done
```

| Operation | Result row | Why it appears |
| --- | --- | --- |
| join | Order 1, Alice | C100 matches Alice. |
| join | Order 2, Bob | C101 matches Bob. |
| join | Order 3, Alice | C100 matches again; two orders belong to Alice. |
| join | Order 4, no name | The left join keeps C102 even though `customers.csv` has no C102. The CSV writer displays that missing value as `nan`. |
| merge | Orders 1, 3, 4 | Their IDs have no update, so their original rows remain. |
| merge | Order 2 | The full update row replaces amount 80/cancelled with 90/paid. |
| merge | Order 5 | Its ID is new, so the full row is added. |
| union | Orders 1, 2, 3, 4 | These are the original rows. |
| union | Order 5 | This is the new row from `more_orders.csv`. |

`more_orders.csv` also repeats order 1 exactly. `distinct: true` removes the duplicate; it does not replace order 1. A customer lookup alone cannot serve as the complete replacement rows required by `merge` or as additional orders for `union`.