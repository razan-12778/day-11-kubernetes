FROM python:3.12.8-slim

#Do not use env as this would persist after the build and would impact your containers, children images
ARG DEBIAN_FRONTEND=noninteractive

# force the stdout and stderr streams to be unbuffered.
ENV PYTHONUNBUFFERED=1

#Setup workdir
WORKDIR /app

COPY api api
COPY pyproject.toml poetry.lock ./

RUN pip3 install --upgrade --no-cache-dir pip \
    && pip3 install poetry \
    && poetry install --only main

EXPOSE 8000

ENTRYPOINT [ "poetry", "run" ]

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

#size: 231 MB
