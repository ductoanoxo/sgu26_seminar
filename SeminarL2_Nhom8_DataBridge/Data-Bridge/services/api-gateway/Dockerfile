# ==========================================
# STAGE 1: Builder
# ==========================================
FROM python:3.10-slim AS builder

# Set build-time environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Optimize: Use Singapore mirrors for faster downloads in SEA (handles both old and new Debian formats)
RUN sed -i 's/deb.debian.org/mirrors.linode.com/g' /etc/apt/sources.list 2>/dev/null || \
    sed -i 's/deb.debian.org/mirrors.linode.com/g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || true && \
    sed -i 's/security.debian.org/mirrors.linode.com/g' /etc/apt/sources.list 2>/dev/null || \
    sed -i 's/security.debian.org/mirrors.linode.com/g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || true

# Install system dependencies needed for building (e.g., compilers for psycopg2)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
# setuptools required by openai-whisper (uses legacy setup.py with pkg_resources)
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade setuptools && \
    pip install -r requirements.txt


# ==========================================
# STAGE 2: Runner
# ==========================================
FROM python:3.10-slim AS runner

# Set production environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Optimize: Use Singapore mirrors for runner stage as well
RUN sed -i 's/deb.debian.org/mirrors.linode.com/g' /etc/apt/sources.list 2>/dev/null || \
    sed -i 's/deb.debian.org/mirrors.linode.com/g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || true && \
    sed -i 's/security.debian.org/mirrors.linode.com/g' /etc/apt/sources.list 2>/dev/null || \
    sed -i 's/security.debian.org/mirrors.linode.com/g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || true

# Install runtime dependencies (e.g., libpq for psycopg2)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    ffmpeg

# Create a non-root user for security
RUN groupadd -g 1001 python && \
    useradd -u 1001 -g python -s /bin/sh -m python

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application source code (selective copy)
# This assumes the Dockerfile is inside the service directory
COPY core/ ./core/
COPY domain/ ./domain/
COPY routers/ ./routers/
COPY schemas/ ./schemas/
COPY services/ ./services/
COPY main.py .

# Set ownership to non-root user
RUN chown -R python:python /app

# Switch to non-root user
USER python

# Expose the application port
EXPOSE 8000

# Production-grade healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Launch the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# ==========================================
# STAGE 3: Development
# ==========================================
FROM python:3.10-slim AS dev

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

RUN sed -i 's/deb.debian.org/mirrors.linode.com/g' /etc/apt/sources.list 2>/dev/null || \
    sed -i 's/deb.debian.org/mirrors.linode.com/g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || true && \
    sed -i 's/security.debian.org/mirrors.linode.com/g' /etc/apt/sources.list 2>/dev/null || \
    sed -i 's/security.debian.org/mirrors.linode.com/g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || true

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    ffmpeg

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
