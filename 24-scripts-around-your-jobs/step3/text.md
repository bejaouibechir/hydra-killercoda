# 3. Run the remote action on node01

~~~bash
/opt/hydra/bin/python /root/lab/lab24-resources/lab24.py enable-ssh
/opt/hydra/bin/python /root/lab/lab24-resources/lab24.py run remote
~~~

Hydra connects to root@node01 using the two-node environment's SSH access. The command writes only /root/lab24-remote/receipt.txt on node01. Read it:

~~~bash
ssh node01 cat /root/lab24-remote/receipt.txt
~~~

Press Check after the run and receipt succeed.
