# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application files
COPY server_postgresql.py .
COPY index_professional.html .
COPY search.html .
COPY about.html .
COPY contact.html .
COPY methodology.html .
COPY privacy.html .
COPY terms.html .
COPY sources.html .
COPY service-worker.js .
COPY manifest.json .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Environment variables
ENV PORT=8080
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"

# Run with Gunicorn
CMD exec gunicorn --bind :$PORT --workers 2 --threads 4 --timeout 120 --access-logfile - --error-logfile - server_postgresql:app
