FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    GPIOZERO_PIN_FACTORY=lgpio

# build-essential + swig : pour compiler lgpio (relais). libgpiod2 : pour lire les DHT22.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential swig libgpiod2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements-pi.txt ./
RUN pip install --no-cache-dir -r requirements-pi.txt

COPY . .

EXPOSE 8000
CMD ["sh", "docker/entrypoint.sh"]
