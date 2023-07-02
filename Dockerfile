FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PYTHONUNBUFFERED 1

WORKDIR /code/

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml ./

RUN poetry install --only main

COPY . .

ENTRYPOINT ["sh", "entrypoint.sh"]
