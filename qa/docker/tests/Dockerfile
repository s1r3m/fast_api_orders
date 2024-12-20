# Base image
FROM python:3.10-slim

RUN apt-get update && apt-get install -y nginx && apt-get clean

# Create working directory
WORKDIR /app

COPY pyproject.toml poetry.lock /

# Install dependencies
RUN poetry install --no-root

# Run the application
CMD ["poetry", "run", "pytest", "tests"]
