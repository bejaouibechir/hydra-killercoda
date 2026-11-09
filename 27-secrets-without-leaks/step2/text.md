# 2. Use an environment variable

Read the value into this terminal session without displaying it, then remove the project secret file. Hydra will normalize db.password to DB_PASSWORD.

~~~bash
cd /root/lab/secrets-without-leaks
export DB_PASSWORD="$(sed -n 's/^db.password=//p' .hydra/secrets)"
rm .hydra/secrets
/opt/hydra/bin/python /root/lab/lab27-resources/lab27.py run env
git status --short --untracked-files=all
~~~

Keep this terminal session open for the next step. Do not echo DB_PASSWORD. Press Check.
