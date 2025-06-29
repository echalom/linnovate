FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# Install ffmpeg and git (fixes whisper install issue)
RUN apt-get update && apt-get install -y ffmpeg git && \
    pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["python", "app/main.py"]
