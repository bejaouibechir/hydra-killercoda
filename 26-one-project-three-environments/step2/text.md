# 2. Create dev, test and prod

Write three environment files. The project and workflow remain the same.

~~~bash
cat > /root/lab/three-environments/environments/dev.yaml <<'YAML'
parameters:
  min_amount: 0
  country: FR
  batch_label: dev
  sample_size: 2
YAML
cat > /root/lab/three-environments/environments/test.yaml <<'YAML'
parameters:
  min_amount: 25
  country: DE
  batch_label: test
  sample_size: 3
YAML
cat > /root/lab/three-environments/environments/prod.yaml <<'YAML'
parameters:
  min_amount: 100
  country: US
  batch_label: prod
  sample_size: 4
YAML
~~~

Review the files, then press Check.
