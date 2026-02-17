# healing-operator-experiments

Deployment manifests, sample app, and fault-injection/evaluation scripts.

## Contents
- `deploy/`
- `experiments/`

## Typical flow
```bash
kubectl apply -f deploy/sample-app/dependency.yaml
kubectl apply -f deploy/sample-app/api.yaml
kubectl apply -f deploy/sample-app/healingpolicy.yaml
python experiments/run_experiments.py --iterations 5
python experiments/aggregate_results.py --input experiments/results.csv
```
