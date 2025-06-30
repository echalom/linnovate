FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# Install ffmpeg, git, and system libraries required by moviepy
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    libsm6 \
    libxext6 \
    libgl1 && \
    pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["python", "main.py"]
