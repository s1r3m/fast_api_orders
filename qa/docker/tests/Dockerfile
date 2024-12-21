# Base image.
FROM python:3.10-slim

RUN apt-get update && apt-get install -y nginx curl && apt-get clean
RUN pip install poetry==1.7.1

# Create working directory.
WORKDIR /qa

# Install dependencies.
COPY . .
COPY pyproject.toml poetry.lock /
COPY docker/tests/start_tests.sh .

RUN poetry install --no-root

CMD ["echo", "This is a placeholder CMD; use docker-compose.yml to define the actual command"]
