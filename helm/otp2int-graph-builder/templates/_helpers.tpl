{{/* vim: set filetype=mustache: */}}

{{/* Generate graph-builder labels */}}
{{- define "graph.builder.labels" }}
app: graph-builder-otp2int
release: graph-builder-otp2int
team: ror
slack: talk-ror
type: api
namespace: {{ .Release.Namespace }}
app.kubernetes.io/managed-by: Helm
{{- end }}

{{/* Generate common Helm ownership annotations */}}
{{- define "common.annotations" }}
meta.helm.sh/release-name: {{ .Release.Name }}
meta.helm.sh/release-namespace: {{ .Release.Namespace }}
{{- end }}
