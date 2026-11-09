# 1. Read PostgreSQL with a project secret

The job uses a placeholder in its connection. Do not print the password itself.

~~~bash
cd /root/lab/secrets-without-leaks
cat jobs/read_products/sources.yaml
cat .gitignore
git check-ignore -v .hydra/secrets
/opt/hydra/bin/python /root/lab/lab27-resources/lab27.py run local
cat outputs/products.csv
git status --short --untracked-files=all
~~~

The database should return Mug and Lamp. Git may list the lesson's ordinary files, but it must not list .hydra/secrets. Press Check.
