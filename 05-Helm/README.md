# 🎯 Goal

Helm helps us automate the deployment of complex k8s from **charts** which can be seen like recipes for settings up complex structures on k8s. You can have a look at available **charts** on https://artifacthub.io/

🎯 In this challenge we will use helm to deploy a complex `airflow` setup to our cluster!

<br>

# 1️⃣ Setup

To install helm use:

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

Then make sure we have a fresh **minikube** cluster running and ready to go!

To add the **airflow chart** to our local computer

```bash
helm repo add airflow-stable https://airflow-helm.github.io/charts
helm repo update
```

Next make a copy of the `.env.sample` as your own `.env`. We are going to fill out some of the values. The `AIRFLOW_NAME` is what we will name our deployed `chart`. Then we will also use `AIRFLOW_NAMESPACE` to use kubectl namespaces. The following environment variables are for security:

```bash
AIRFLOW__WEBSERVER__SECRET_KEY=###
AIRFLOW__CORE__FERNET_KEY=###
```

Generate the `AIRFLOW__WEBSERVER__SECRET_KEY` with:

```bash
python -c 'import os; print(os.urandom(16))'
```

And the `AIRFLOW__CORE__FERNET_KEY` with:

```python
from cryptography.fernet import Fernet

fernet_key = Fernet.generate_key()
print(fernet_key.decode())
```

Now also clone the `helm-value.yaml.copy` and we are ready to go!

<br>

# 2️⃣ Creating Airflow

Lets create our own namespace.

```bash
kubectl create namespace $AIRFLOW_NAMESPACE
```

To access stuff in this namespace we have to append every `kubectl` with `-n airflow`. Lets instead set this as our current namespace:

```bash
kubectl config set-context --current --namespace=airflow
```

Creating our **secrets** 🔐

```bash
kubectl create secret generic airflow-fernet-key --namespace="$AIRFLOW_NAMESPACE" --from-literal=value=$AIRFLOW__CORE__FERNET_KEY
```

```bash
kubectl create secret generic airflow-webserver-secret-key --namespace="$AIRFLOW_NAMESPACE" --from-literal=value=$AIRFLOW__WEBSERVER__SECRET_KEY
```

Now we can apply our chart and options 👇

```bash
helm install "$AIRFLOW_NAME" airflow-stable/airflow \
  --namespace "$AIRFLOW_NAMESPACE" \
  --version "8.9.0" \
  --values ./helm-values.yaml
```

This will take a little while to fully spin up. A perfect opportunity to grab a drink or make a coffee ☕️

When you come back and checkout your cluster you will see all the **pods** you need created!

The previous command should have detailed a command to access the Web GUI in your Airflow cluster. It should look similar to:

```bash
Use these commands to port-forward the Services to your localhost:
  * Airflow Webserver:  kubectl port-forward svc/airflow-cluster-web 8080:8080 --namespace airflow
```

<br>

# 3️⃣ Making ready for production

The helm chart also comes with a build in postgres service that will spin up with the Helm chart if some secrets exist.

Let's add a metadata DB 💿

```bash
kubectl create secret generic airflow-pg-password --namespace="$AIRFLOW_NAMESPACE" --from-literal=password=$POSTGRES_PASSWORD
```

```bash
kubectl create secret generic airflow-pg-user --namespace="$AIRFLOW_NAMESPACE" --from-literal=username=$POSTGRES_USER
```

You may have noticed the initialisation note that the embedded Postgres instance shouldn't be used for production! There is also the option to use an external metadata database, more common in production for fault tolerance and fail over, in the helm chart. Have a look at the bottom of `helm-values.yaml`

<br>

# 4️⃣ Teardown

Make sure to pull down the cluster if you aren't using it to free up system resources:

```bash
# Teardown resources created by helm
helm uninstall "$AIRFLOW_NAME" --namespace "$AIRFLOW_NAMESPACE"

# Stop minikube
minikube stop

# Delete minikube VM
minikube delete
```

<br>

# 🏁 Finishing up

This is the bare basics of spinning up an Airflow cluster with Helm, and there are a few more things you'd need to make it production ready like:
- Using an external metadata database
- Create liveness probes
- Create Persistent Volume's and Claims for worker logging

But with your existing Airflow knowledge and new found Kubernetes skills you should be capable of taking on that challenge!

<br>
