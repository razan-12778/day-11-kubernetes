# What the Dockerfile in the lecture looks like
# europe-west1-docker.pkg.dev/data-engineering-students/student-images/k8s-lecture-app:dev
# It might be based on python:3.8.12, unsure - doesn't make a meaningful difference

FROM python:3.12.11-slim

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install fastapi uvicorn

COPY main.py main.py

RUN mkdir pv-data

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
