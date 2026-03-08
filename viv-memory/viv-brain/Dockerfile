FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY viv_brain/ ./viv_brain/
COPY config/ ./config/

# Set environment
ENV PYTHONPATH=/app
ENV VIV_CONFIG_PATH=/app/config

# Default command
CMD ["python", "-m", "viv_brain.orchestrator"]
