# otp2int Helm chart

This chart deploys the `otp2int` journey planner and its graph builder CronJobs in the `otp2int` namespace.

Do not deploy the chart manually.
The `deploy.yml` workflow deploys it with `entur/gha-helm` as the release `otp2int`.
See the [repository README](../README.md) for the deploy flow, rollback and the graph builds.

## Images

The chart has two image values in `otp2int/values.yaml`:

- `image.identifier` is the image of the journey planner pods.
- `cronjobGraphBuilder.image` is the image of the graph builder CronJobs.

Update the OTP image in two commits: first `cronjobGraphBuilder.image`, then `image.identifier`.
See [Updating the OTP image](../README.md#updating-the-otp-image).

## Print the templates

To see the rendered templates for dev, run this from the repository root:

```bash
helm template otp2int ./helm/otp2int \
  -f helm/otp2int/env/values-kub-ent-jp-dev.yaml \
  --namespace otp2int
```

## Lint the chart

```bash
helm lint helm/otp2int -f helm/otp2int/env/values-kub-ent-jp-dev.yaml
```

## Release history

To see the deployed revisions:

```bash
helm history otp2int --namespace otp2int
```

To roll back, use the `deploy.yml` workflow with a repository tag.
A `helm rollback` does not update the repository tag annotations on the deployment, and the next deploy overwrites it.
