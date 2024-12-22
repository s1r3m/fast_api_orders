FROM python:3.10-slim

RUN apt-get update && apt-get install -y nginx && apt-get clean

RUN pip install poetry==1.7.1

# Create working directory.
WORKDIR /trader

COPY pyproject.toml poetry.lock /
COPY qa/docker/app/start.sh /usr/local/bin/

# Install dependencies.
RUN poetry install --without dev

ENV PYTHONPATH=/trader

# Run the application.
ENTRYPOINT ["start.sh"]
