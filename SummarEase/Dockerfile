# ---- Base Image ----
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

# ---- Expose port ----
EXPOSE 10000

# ---- Start FastAPI server ----
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
