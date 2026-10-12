{{- define "infinimesh.coreImage" -}}
{{- printf "%s/%s:%s" .registry .service .tag -}}
{{- end -}}

{{- define "infinimesh.pullPolicy" -}}
{{- if eq (toString .tag) "latest" -}}
Always
{{- else -}}
IfNotPresent
{{- end -}}
{{- end -}}

{{- define "infinimesh.dbHost" -}}
{{- if .Values.external.arangodb -}}
{{- required "external.hosts.arangodb is required when external.arangodb is true" .Values.external.hosts.arangodb -}}
{{- else -}}
infinimesh-arango:8529
{{- end -}}
{{- end -}}

{{- define "infinimesh.redisHost" -}}
{{- if .Values.external.redis -}}
{{- required "external.hosts.redis is required when external.redis is true" .Values.external.hosts.redis -}}
{{- else -}}
infinimesh-redis:6379
{{- end -}}
{{- end -}}

{{- define "infinimesh.rabbitHost" -}}
{{- if .Values.external.rabbitmq -}}
{{- required "external.hosts.rabbitmq is required when external.rabbitmq is true" .Values.external.hosts.rabbitmq -}}
{{- else -}}
infinimesh-rabbitmq:5672
{{- end -}}
{{- end -}}

{{- define "infinimesh.rabbitConn" -}}
{{- printf "amqp://%s:%s@%s/" .Values.auth.rabbitmqUser .Values.auth.rabbitmqPass (include "infinimesh.rabbitHost" .) -}}
{{- end -}}
