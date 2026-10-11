# Infinimesh on Kubernetes

Install recipes for a cluster running the [platform operator](https://github.com/infinimesh/platform-operator).

- `microk8s/` — local microk8s via Multipass, then a Platform
- `minikube/` — local minikube, then a Platform
- `hetzner/` — Platform and Kafka manifests for a hosted cluster
- `production/` — production Kafka, Postgres, and a microk8s bootstrap script

Apply the operator first:

```bash
kubectl apply -f https://raw.githubusercontent.com/infinimesh/platform-operator/main/manifests/crd.yaml
kubectl apply -f https://raw.githubusercontent.com/infinimesh/platform-operator/main/manifests/operator.yaml
```

The Docker Compose stack for the current platform is in [core](https://github.com/infinimesh/core).

Apache-2.0.
