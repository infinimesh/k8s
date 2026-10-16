# Infinimesh on Kubernetes

The cluster install of [core](https://github.com/infinimesh/core). Same processes as Docker Compose: ArangoDB, RabbitMQ, Redis, `api`, `shadow`, `mqtt-bridge`, `gateway`, `console`, `pairing`, `rules`, `http-fs`, and `coap-gateway`.

## Kustomize

Images are `ghcr.io/infinimesh/core/<service>:latest`. A core release tag also pushes that tag. `imagePullPolicy: Always` is set so a rollout takes the new image.

```bash
kubectl apply -k base
```

The auth secret uses the Compose defaults (`openSesame`, `infinimesh`, `seeeecreet`). Change `base/secret.yaml` before you expose the cluster.

## Helm

`charts/infinimesh` installs the same Services into the `infinimesh` namespace (`namespace.create`, `namespace.name`). Core images are `ghcr.io/infinimesh/core/<service>:v3.4.2` (`image.tag`). Until v3.4.0 ships the default is the release candidate `v3.4.0-rc.10`, and the v3.4.0 release moves it. Later release candidates are not written into the chart, set `image.tag` to one when you want it. `imagePullPolicy` is `IfNotPresent`, or `Always` when the tag is `latest`. `api`, `shadow`, and `mqtt-bridge` default to 2 replicas and have a PodDisruptionBudget (`minAvailable: 1`) when that replica count is greater than 1. `gateway`, `console`, `pairing`, `rules`, and `http-fs` default to 1 replica. `http-fs` listens on 8000 and stores files on a 10Gi volume unless `httpFs.s3.bucket` is set. Set `httpFs.publicURL` to the browser URL of that service so the gateway advertises `HTTP_FS`. CoAP is off unless `coap.enabled` is true. Its Service is ClusterIP on UDP 5683. MQTT publishes 8883. Set `mqtt.plaintext` to also publish 1883.

ArangoDB (`arangodb/arangodb:latest`), RabbitMQ (`rabbitmq:3.9-management`), and Redis (`redis:latest`) run in-cluster, each with a 10Gi volume. Set `external.arangodb`, `external.rabbitmq`, or `external.redis` to skip that workload. Service env then uses `external.hosts.arangodb` (`DB_HOST`, `host:port`), `external.hosts.redis` (`REDIS_HOST`, `host:port`), or `external.hosts.rabbitmq` (`host:port` in `RABBITMQ_CONN`).

```bash
helm install infinimesh charts/infinimesh
```

Chart auth defaults match Compose and `base/secret.yaml`: database password `openSesame`, root password `infinimesh`, signing key `seeeecreet`. Change `auth` before you expose the cluster.

Readiness and liveness are TCP probes on the service port. Every core container has a `metrics` port on 2112. Set `metrics.serviceMonitor` to create a ServiceMonitor that scrapes port 2112.

## MQTT TLS

Create the MQTT TLS secret before the bridge can start. The chart does not create it. The sample pair in core is `hack/server.crt` and `hack/server.key`:

```bash
kubectl -n infinimesh create secret tls infinimesh-mqtt-tls --cert=hack/server.crt --key=hack/server.key
```

| Service | Port |
|---|---|
| `infinimesh-gateway` | 8000 |
| `infinimesh-console` | 80 |
| `infinimesh-api` | 8000 |
| `infinimesh-mqtt` | 8883 |
| `infinimesh-rules` | 2112 |
| `infinimesh-http-fs` | 8000 |
| `infinimesh-coap` | 5683/udp when `coap.enabled` |

A default StorageClass is required for in-cluster ArangoDB, RabbitMQ, Redis, and http-fs volumes.

The [platform operator](https://github.com/infinimesh/platform-operator) reconciles a Platform into this same stack. It does not install Kafka or Dgraph.

Apache-2.0.
