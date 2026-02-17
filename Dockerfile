# syntax=docker/dockerfile:1

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080

RUN addgroup --system app && adduser --system --ingroup app app

WORKDIR /srv/app

COPY backend/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY backend/app ./app
COPY backend/wsgi.py .
COPY backend/pyproject.toml .

RUN chown -R app:app /srv/app

USER app

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "wsgi:app", "--workers", "2", "--threads", "4", "--timeout", "60"]
