FROM python:3.10-slim as builder

WORKDIR /src/app

COPY requirements.txt .

RUN pip install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

COPY batches_app core .env ./

CMD ["gunicorn", "core.wsgi", "-b", "0.0.0.0:8000"]