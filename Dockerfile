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
    wget \
    unzip \
 && pip install --upgrade pip wheel setuptools \
 && pip install --no-cache-dir -r requirements.txt \
 # Download and unzip Vosk model
 && wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip \
 && unzip vosk-model-small-en-us-0.15.zip \
 && mv vosk-model-small-en-us-0.15 vosk-model \
 && rm vosk-model-small-en-us-0.15.zip \
 # Clean up
 && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY app/ ./app/

CMD ["python", "app/main.py"]
