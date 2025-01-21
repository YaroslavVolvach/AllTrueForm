FROM python:3.9-slim

RUN apt-get update && apt-get install -y libpq-dev

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

COPY alembic.ini /alembic.ini

COPY migrations /migrations

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]