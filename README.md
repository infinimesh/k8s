# Infinimesh on Kubernetes

The cluster install of [core](https://github.com/infinimesh/core). Same processes as Docker Compose: ArangoDB, RabbitMQ, Redis, `repo`, `shadow`, `mqtt-bridge`, `web`, `console`, and `handsfree`.

Images are `ghcr.io/infinimesh/core/<service>:latest`. A core release tag also pushes that tag. `imagePullPolicy: Always` is set so a rollout takes the new image.

```bash
kubectl apply -k base
```

The auth secret uses the Compose defaults (`openSesame`, `infinimesh`, `seeeecreet`). Change `base/secret.yaml` before you expose the cluster. The MQTT bridge loads `base/certs`, the same sample certificate as `core` `hack/server.crt`. Replace that secret for a real deployment.

| Service | Port |
|---|---|
| `infinimesh-web` | 8000 |
| `infinimesh-console` | 80 |
| `infinimesh-repo` | 8000 |
| `infinimesh-mqtt` | 1883, 8883 |

A default StorageClass is required. ArangoDB, RabbitMQ, and Redis each request a 10Gi volume.

The [platform operator](https://github.com/infinimesh/platform-operator) reconciles a Platform into this same stack. It does not install Kafka or Dgraph.

Apache-2.0.
