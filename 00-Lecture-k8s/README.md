# Can't push a docker image to GCP Artifact Registry

Make sure that docker is authenticated with GCP.

```bash
# Change the location to one that makes sense for you
LOCATION=europe-west1

gcloud auth configure-docker $(LOCATION)-docker.pkg.dev
# gcloud auth configure-docker europe-west1-docker.pkg.dev
```
