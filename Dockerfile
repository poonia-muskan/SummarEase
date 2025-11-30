FROM python:3.10-slim

# ---- Install system dependencies ----
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ---- Set work directory ----
WORKDIR /app

# ---- Copy backend folder ----
COPY backend/ /app/

# ---- Install Python dependencies ----
RUN pip install --no-cache-dir -r requirements.txt

# Cloud Run will set PORT. Default to 8080.
ENV PORT=8080

# ---- Start FastAPI server ----
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080}"]
