# TODO: I've been unable to make this work with alpine because of problems with pybind11
FROM python:3.10 AS builder
WORKDIR /app
COPY . /app
RUN apt-get update
RUN apt-get install -y --no-install-recommends libpq-dev gcc python3-dev musl-dev make libffi-dev libssl-dev git cargo g++
RUN pip install poetry

FROM builder AS development
RUN poetry install
EXPOSE 4444

FROM builder AS production
RUN poetry install --without dev
CMD ["poetry", "run", "gunicorn", "-c", "gunicorn.conf.py", "app.main:app"]
