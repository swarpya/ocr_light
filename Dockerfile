# Use a lightweight Python base
FROM python:3.10-slim

# Prevent Python from buffering stdout (helps with logs)
ENV PYTHONUNBUFFERED=1

# 1. Install System Dependencies
# tesseract-ocr: The lightweight OCR engine
# poppler-utils: Required to convert PDF to images
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Python Libraries
# We DO NOT install torch or surya (too heavy for Free Tier)
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    python-multipart \
    requests \
    pillow \
    pytesseract \
    pypdfium2 \
    pandas \
    openpyxl \
    python-pptx

WORKDIR /app
COPY api_server.py /app/api_server.py

# Launch the server
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]