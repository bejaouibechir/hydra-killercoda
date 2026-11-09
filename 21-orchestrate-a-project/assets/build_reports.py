import csv,json
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'data'/'output'
def read(name):
 with (out/name).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
sales=read('sales.csv')
report={'sales_source':'backup' if all(r['region']=='BACKUP' for r in sales) else 'postgres',
        'sales_rows':len(sales),'stock_rows':len(read('stock.csv')),'reference_rows':len(read('refs.csv'))}
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
