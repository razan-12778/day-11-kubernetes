# backend/Dockerfile image available at `image: europe-west1-docker.pkg.dev/data-engineering-students/student-images/style-backend`

FROM python:3.10.1-slim

WORKDIR /app

RUN apt-get update

# 'ffmpeg', 'libsm6', and 'libxext6' are required for OpenCV.
RUN apt-get install \
    'ffmpeg' \
    'libsm6' \
    'libxext6' \
    'curl'  -y

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN ./getmodels.sh

EXPOSE 8080

CMD ["python", "main.py"]
