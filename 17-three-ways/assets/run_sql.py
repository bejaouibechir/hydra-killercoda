"""Load the CSV into in-memory SQLite and execute the learner's SQL file."""
import csv,os,pathlib,sqlite3,sys
ROOT=pathlib.Path(os.environ.get('HYDRA_LAB17_ROOT','/root/lab/three-ways'))
db=sqlite3.connect(':memory:')
db.execute('CREATE TABLE orders(id INTEGER, customer_id TEXT, country TEXT, amount TEXT, status TEXT)')
with (ROOT/'data/orders.csv').open(newline='',encoding='utf-8') as f:
 rows=list(csv.DictReader(f))
db.executemany('INSERT INTO orders VALUES (:id,:customer_id,:country,:amount,:status)',rows)
query=(ROOT/'query.sql').read_text()
result=db.execute(query)
(ROOT/'output').mkdir(exist_ok=True)
with (ROOT/'output/sql.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow([d[0] for d in result.description]);w.writerows(result)
print((ROOT/'output/sql.csv').read_text())
