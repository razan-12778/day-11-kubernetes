# 🎯 Goal

The previous exercise the **frontend** and **backend** were passing the styled images via a volume.

🎯 Instead to save us needing a volume lets put them in the same pod to share a file system!

<br>

# 1️⃣ Context

You have the backend image from before + a new `europe-west1-docker.pkg.dev/data-engineering-students/student-images/style-frontend-sidecar` image!

❓ Why?

Before we were accessing the api at the `service` instead its now available at localhost as they are on the same **pod!**

❓ How to add multiple **containers** to a **pod?**

The clue is in the `spec:` of `containers`!

```yaml
spec:
  containers:
    - image: ...
      name: backend
    - image: ...
      name: frontend
```

❓ How to access the shared file system?

Each `container` still has its own file system but we can add a mount to the pod file system!

```yaml
volumes:
- name: shared-data
  emptyDir: {}
```

Then mount it as normal! In this challenge, mount this as we mounted volumes before **at `/storage` in both containers!**

Finally you will need to override the `CMD` of the frontend and replace it with:

```bash
["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

<br>

# 2️⃣ Your turn 😅

This exercise is a lot less guided than previous ones but you should have the tools you need at this point to write your own **k8s** config files!

<br>
