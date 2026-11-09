# 4. Restart PostgreSQL

Restart only the database container for this lab. Wait until it accepts connections, then run the thread again:

~~~bash
cd /root/lab/orchestrate-project
docker start hydra-lab21-postgres
for attempt in $(seq 1 30); do
  docker exec hydra-lab21-postgres pg_isready -U lab21 -d hydra_lab21 >/dev/null 2>&1 && break
  sleep 1
done
docker exec hydra-lab21-postgres pg_isready -U lab21 -d hydra_lab21
/opt/hydra/bin/python /root/lab/lab21-resources/lab21.py run restored
cat reports/restored.json
cat data/output/report.json
~~~

Live sales runs twice again; the fallback is not selected. Press Check.
