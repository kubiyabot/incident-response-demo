# Dockerfile for Kubiya Incident Response Workflow
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Install the package
RUN pip install -e .

# Create a non-root user
RUN groupadd -r kubiya && useradd -r -g kubiya kubiya
RUN chown -R kubiya:kubiya /app
USER kubiya

# Set default command
CMD ["kubiya-incident", "--help"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD kubiya-incident validate --incident-id "HEALTH-CHECK" --title "Health Check" --severity "low" || exit 1

# Labels for metadata
LABEL maintainer="Kubiya <support@kubiya.ai>" \
      version="1.0.0" \
      description="Production-grade incident response workflow with intelligent service validation" \
      org.opencontainers.image.source="https://github.com/kubiya-ai/incident-response-workflow"