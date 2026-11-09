# 3. Use an external secrets file

Write the value held in this shell to a private file outside the Git project. Then unset the environment variable so Hydra must use --secrets-file.

~~~bash
install -d -m 700 /root/lab27-private
umask 077
printf 'db.password=%s\n' "$DB_PASSWORD" > /root/lab27-private/secrets
unset DB_PASSWORD
/opt/hydra/bin/python /root/lab/lab27-resources/lab27.py run external
cd /root/lab/secrets-without-leaks
git status --short --untracked-files=all
~~~

The helper invokes hdrctl run with --secrets-file /root/lab27-private/secrets. It checks that the password is not printed and that Git never lists either secret file. Press Check.
