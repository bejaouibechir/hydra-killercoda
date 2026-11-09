# 4. Override one value for this run

Run dev again, but give min_amount a value on the command line:

~~~bash
cd /root/lab/three-environments
hdrctl run . --env dev --param min_amount=100 > reports/dev-override.txt 2>&1
cat reports/dev-override.txt
~~~

Compare reports/dev.txt with reports/dev-override.txt. Write a short explanation in your own words: which value won, and how does it compare with the dev value and project default?

~~~bash
cat > /root/lab/three-environments/reports/answer.txt <<'TEXT'
Replace this line with your explanation.
TEXT
cat /root/lab/three-environments/reports/answer.txt
~~~

Edit answer.txt before pressing Check. The dev environment file should still contain min_amount: 0.
