# Load files from gs to bq

1. From Cloud Shell, set the active project to (**zeta-period-359422**)

```bash
gcloud config set project zeta-period-359422
```

2. Create gs bucket (**yc-learning**) in **eu** region:

```bash
gsutil mb -c standard -l eu gs://yc-learning
```

3. Create bq dataset in eu region

```bash
bq mk --location=eu dataeng_assignment
```
