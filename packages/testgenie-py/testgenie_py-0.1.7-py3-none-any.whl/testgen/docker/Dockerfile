FROM python:3.10

RUN apt-get update && apt-get install -y curl build-essential

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

ENV POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1 \
    RUNNING_IN_DOCKER=true

WORKDIR /controller

# Copy poetry files
COPY . .

ENV PYTHONPATH=/controller:/controller/testgen

RUN poetry install --no-root

# Entrypoint (Can be overridden by Docker SDK in Python)
CMD ["poetry", "run", "python", "-m", "testgen.main"]
