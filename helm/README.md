# otp2int Helm charts

This directory has two charts.
Each chart is a separate Helm release in the `otp2int` namespace.

| Chart | Release | Deploy workflow | Contents |
|---|---|---|---|
| `otp2int` | `otp2int` | `deploy-serving-pods.yml` | Journey planner deployment, service, ingress and its configmaps |
| `otp2int-graph-builder` | `otp2int-graph-builder` | `deploy-graph-builder.yml` | Graph builder CronJobs and their configmaps |

Do not deploy the charts manually.
The workflows deploy them with `entur/gha-helm`.
See the [repository README](../README.md) for the deploy flow, rollback and the graph builds.

## Images

Each chart has its own image value, `image.identifier`, in its `values.yaml`.
Update the OTP image in both charts in the same commit.
`cd.yml` builds the graphs with the new image before it deploys the `otp2int` chart.
See [Updating the OTP image](../README.md#updating-the-otp-image).

## Print the templates

To see the rendered templates for dev, run this from the repository root:

```bash
helm template otp2int ./helm/otp2int \
  -f helm/otp2int/env/values-kub-ent-jp-dev.yaml \
  --namespace otp2int
helm template otp2int-graph-builder ./helm/otp2int-graph-builder \
  -f helm/otp2int-graph-builder/env/values-kub-ent-jp-dev.yaml \
  --namespace otp2int
```

## Lint the charts

```bash
helm lint helm/otp2int -f helm/otp2int/env/values-kub-ent-jp-dev.yaml
helm lint helm/otp2int-graph-builder -f helm/otp2int-graph-builder/env/values-kub-ent-jp-dev.yaml
```

## Release history

To see the deployed revisions:

```bash
helm history otp2int --namespace otp2int
helm history otp2int-graph-builder --namespace otp2int
```

To roll back, use the deploy workflow of the release with a repository tag.
A `helm rollback` does not update the repository tag annotations on the deployment, and the next deploy overwrites it.
