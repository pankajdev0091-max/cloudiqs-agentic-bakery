# =============================================================================
# CloudiQS Agentic AI Bakery - Backend Docker Image
# =============================================================================
# Multi-stage build for minimal production image size.
#
# Build:   docker build -t cloudiqs-backend -f backend/deploy/Dockerfile .
# Run:     docker run -p 8000:8000 cloudiqs-backend
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1 - Builder: install Python dependencies into a virtual-env
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /build

# System packages required by some wheels (cryptography, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libffi-dev && \
    rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip setuptools wheel && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# ---------------------------------------------------------------------------
# Stage 2 - Runtime: lean production image
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

LABEL maintainer="CloudiQS <info@cloudiqs.com>"
LABEL description="CloudiQS Agentic AI Bakery - FastAPI Backend"

# Non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

WORKDIR /app

# Copy the virtual-env from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Ensure Python can resolve ``backend.*`` imports
ENV PYTHONPATH="/app"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy application source
COPY backend/ /app/backend/

# Switch to non-root user
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Health check - hit the /api/health endpoint every 30 s
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" || exit 1

# Run with uvicorn; workers configurable via env
CMD ["uvicorn", "backend.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "2", \
     "--log-level", "info"]
