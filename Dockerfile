FROM python:3.9-slim

WORKDIR /app

COPY ./src /app/src

COPY ./requirements.txt /app
COPY ./gunicorn_config.py /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/logs

CMD ["gunicorn", "-c", "/app/gunicorn_config.py", "src.app:app"]
