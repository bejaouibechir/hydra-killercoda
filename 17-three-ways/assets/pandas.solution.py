from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
orders = pd.read_csv(ROOT / 'data/orders.csv')
orders['country'] = orders['country'].str.strip().str.upper()
orders['status'] = orders['status'].str.strip().str.lower()
orders['amount'] = pd.to_numeric(orders['amount'], errors='raise')
paid = orders[orders['status'] == 'paid']
latest = paid.sort_values('id', ascending=False).drop_duplicates('customer_id')
result = (latest.groupby('country', as_index=False)['amount']
          .sum().rename(columns={'amount': 'revenue'})
          .sort_values('country'))
(ROOT / 'output').mkdir(exist_ok=True)
result.to_csv(ROOT / 'output/pandas.csv', index=False)
print(result.to_string(index=False))
