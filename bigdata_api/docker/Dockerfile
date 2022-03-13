FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/code

COPY ["bigdata_api/requirements.txt", "bigdata_api/docker/kafka_waiter.sh", "./"]

RUN apt update && apt install -y netcat \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* /tmp/* \
    && chmod +x /usr/src/code/kafka_waiter.sh

ENTRYPOINT ["/usr/src/code/kafka_waiter.sh"]

COPY ["bigdata_api/src", "./"]

CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8001"]
