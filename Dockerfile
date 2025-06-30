FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    libsm6 \
    libxext6 \
    libgl1 \
    build-essential \
    python3-dev \
 && pip install --upgrade pip wheel setuptools \
 && pip install --no-cache-dir -r requirements.txt \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY app/ ./app/

CMD ["python", "app/main.py"]
