{{/* vim: set filetype=mustache: */}}
{{- define "app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "app.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/* Generate basic labels */}}
{{- define "common.labels" }}
app: {{ template "app.name" . }}
release: {{ .Release.Name }}
team: ror
slack: talk-ror
type: api
namespace: {{ .Release.Namespace }}
app.kubernetes.io/managed-by: Helm
{{- end }}

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