# Multi-stage build for frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/yarn.lock ./
# If you have patches or other install scripts
COPY frontend/ . 
RUN yarn install --frozen-lockfile
RUN yarn build

# Python backend
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies (for PDF generation, OCR, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    antiword \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn uvicorn

# Copy backend code
COPY backend/ .

# Copy built frontend assets
COPY --from=frontend-builder /app/frontend/build /app/frontend/build

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Start command
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "server:app", "--bind", "0.0.0.0:8000"]
