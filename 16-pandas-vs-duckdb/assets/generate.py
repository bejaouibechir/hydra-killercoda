"""Generate a deterministic 5-million-row CSV, without storing rows in memory."""
import csv,os,pathlib,sys
root=pathlib.Path(os.environ.get('HYDRA_LAB16_ROOT','/root/lab/engine-comparison'))
rows=int(os.environ.get('HYDRA_LAB16_ROWS','5000000'))
if rows<=0 or rows%4:sys.exit('Row count must be positive and divisible by four')
path=root/'data/sales.csv'
if path.exists():sys.exit('Refusing to overwrite existing sales.csv')
path.parent.mkdir(parents=True,exist_ok=True)
countries=(('FR',10),('BE',20),('DE',30),('ES',40))
with path.open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(('country','amount'))
 for _ in range(rows//4):w.writerows(countries)
print(f'Generated {rows:,} rows in {path}')
