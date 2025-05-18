# Dockerfile in asr/
FROM python:3.9-slim

WORKDIR /app

# Copy requirements from root
COPY requirements.txt .

RUN apt-get update && apt-get install -y ffmpeg
RUN pip install --no-cache-dir -r requirements.txt

# Copy ASR script from asr folder
COPY asr/asr_api.py .

CMD ["uvicorn", "asr_api:app", "--host", "0.0.0.0", "--port", "8001"]
