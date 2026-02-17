# Monitoring Stack

Use Helm to install Prometheus and Loki for local testing:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
helm upgrade --install loki grafana/loki-stack -n monitoring
```

This project queries:
- Prometheus: `/api/v1/query`
- Loki: `/loki/api/v1/query`
