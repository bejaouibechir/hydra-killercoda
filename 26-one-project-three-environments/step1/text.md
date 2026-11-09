# 1. Declare four parameters

Inspect the prebuilt workflow. Its log action uses all four parameters.

~~~bash
cat /root/lab/three-environments/workflows/show_parameters.yaml
cat /root/lab/three-environments/parameters.yaml
~~~

Replace the starter declarations with four typed defaults:

~~~bash
cat > /root/lab/three-environments/parameters.yaml <<'YAML'
version: '1.0'
parameters:
  min_amount:
    type: int
    default: 50
  country:
    type: str
    default: FR
  batch_label:
    type: str
    default: baseline
  sample_size:
    type: int
    default: 5
YAML
~~~

Press Check. These are project defaults; a selected environment may replace them.
