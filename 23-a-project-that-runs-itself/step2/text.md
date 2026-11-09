# 2. Watch a clock, a file and another project

Keep `hdrctl watch` running in the first tab. A cron rule matches **every minute**; wait for the `minute_clock` run to finish. The consumer should then run under `after_producer`.

In the second tab, create a **new** CSV file after the watcher is ready:

~~~bash
printf 'id,value\n1,hello\n' > /root/lab/project-triggers/producer/inbox/new-orders-$(date +%s).csv
~~~

Wait for `inbox_file` and then `after_producer` to appear in the first tab. File polling takes a few seconds. You can also inspect the same events:

~~~bash
hdrctl trigger history --project /root/lab/project-triggers/producer
hdrctl trigger history --project /root/lab/project-triggers/consumer
~~~

Press **Check** after both the clock and file runs, plus a consumer run, succeed.
