# 🎯 Goal

There are lots of tools to help speed up our writing of k8s but kompose takes this one step further automatically generating k8s from docker compose files! 🤯

In this challenge we are going to take a **style transfer app** which applies a chosen style to a given image. Then use kompose to generate our k8s for us from docker-compose. Now we know how to move to GKE for the remaining exercises we are going to stay on minikube for time and money!

<br>

# 1️⃣ Test your app locally 💻

First try the app with:

```bash
docker compose up
```

You can checkout 🕵️‍♂️ the code the images are built from in the `backend` and `frontend` folders.

Then start a new minikube cluster

```bash
minikube delete
minikube start
```

We are ready to go!

<br>

# 2️⃣ Kompose 🎼

To create k8's files from a `docker-compose.yaml` file run:

```bash
kompose convert -f docker-compose.yaml
```

We get few warnings

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/kompose-first-attempt.png">

- The first warning is important as our backend won't have a `service` created. A `deployment` does not necessarily need a `service`, but when our pods will want to connect with each other it will makes our life much easier.
- The second warning is about our "bind mount": **kompose** cannot translate that automatically, it can only deal with managed "docker volumes".

❓ **Try to rectify both of these problems!**

You can either fix it by fixing the k8s files yourself (longer) or you can change the `docker-compose.yaml`, so that the backend service has a port and both **frontend** and **backend** services use a docker-managed volume that **kompose** can interpret more easily.

<details>
<summary markdown='span'>💡 Fixed docker-compose</summary>

```yaml
services:
  frontend:
    image: europe-west1-docker.pkg.dev/data-engineering-students/student-images/style-frontend
    ports:
      - 8501:8501
    depends_on:
      - backend
    volumes:
        - style-storage:/storage
  backend:
    image: europe-west1-docker.pkg.dev/data-engineering-students/student-images/style-backend
    volumes:
      - style-storage:/storage
    ports:
      - 8080

volumes:
  style-storage:
```

</details>

Once you have fixed the issues, apply your new files with `kubectl apply -f .`

🤯 If you have written robust `docker-compose` files its as easy as just `kompose convert -f docker-compose.yml && kubectl apply -f .`

But also with any automation tool, it is **strongly** recommended to check the translation before applying it to your cluster to see if is anything that has been missed or mis-configured.

❓ Finally access the `frontend` service and verify that it works the same as when we just did `docker compose up`.

<br>

# 🏁 Finishing up

Congrats 🎉 We've quickly translated a **docker compose** app to **k8's**!

In the next exercise we are going to see how we can bring both the frontend and backend together in a single pod!

<br>
