# Join, merge, union

One `orders.csv` is the main flow in three independent Hydra jobs. The second source changes: `customers.csv` adds names with `join`; `order_updates.csv` replaces or adds complete orders with `merge`; `more_orders.csv` stacks complete orders with `union`.

Wait for **Ready** before starting. All terminal commands below are lesson commands.

```bash
cd /root/lab/combine-data
cat data/orders.csv data/customers.csv data/order_updates.csv data/more_orders.csv
```
