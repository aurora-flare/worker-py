FROM python:3.11.6-slim
RUN apt-get update && apt-get install netcat-traditional -y && apt-get autoremove -y && apt-get clean

WORKDIR /code
COPY ./pyproject.toml ./poetry.lock* ./logging.ini /code/
COPY ./src/  /code/src/
COPY ./docker/  /code/docker/

RUN mkdir -p /code/logs && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

WORKDIR /code/src
ENTRYPOINT ["python", "worker.py"]
