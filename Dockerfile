# ----- BASE IMAGE -----
FROM python:3.10-slim

# Avoid buffering
ENV PYTHONUNBUFFERED=1

# ----- SYSTEM DEPENDENCIES -----
# Install tesseract + poppler + required libs
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ----- WORK DIRECTORY -----
WORKDIR /app

# ----- COPY FILES -----
COPY . .

# ----- INSTALL PYTHON PACKAGES -----
RUN pip install --no-cache-dir -r requirements.txt

# ----- PORT -----
EXPOSE 10000

# ----- START SERVER -----
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
