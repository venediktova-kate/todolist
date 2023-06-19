FROM python:3.10.7-slim

ENV POETRY_VERSION=1.5.1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /opt/todolist

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . .

EXPOSE 8006

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]