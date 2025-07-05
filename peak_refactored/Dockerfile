# PEAK System Dockerfile
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PEAK_ENV=production

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY configs/ ./configs/
COPY scripts/ ./scripts/
COPY data/ ./data/
COPY models/ ./models/

# Copy configuration files
COPY setup.py ./
COPY .env.example ./.env

# Install the package
RUN pip install -e .

# Create necessary directories
RUN mkdir -p /app/logs /app/cache /var/log/peak

# Create a non-root user
RUN useradd -m -u 1000 peak && chown -R peak:peak /app
USER peak

# Expose port (if running web interface)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from peak.config.settings import Settings; Settings()" || exit 1

# Default command
CMD ["python", "-m", "peak.pipeline.training_pipeline"]