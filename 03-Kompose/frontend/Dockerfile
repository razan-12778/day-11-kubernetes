# `image: europe-west1-docker.pkg.dev/data-engineering-students/student-images/style-frontend`
FROM python:3.10.1-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]
