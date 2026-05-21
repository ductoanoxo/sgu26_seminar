# ==========================================
# STAGE 1: Builder
# ==========================================
FROM python:3.10-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

RUN sed -i 's/deb.debian.org/mirrors.linode.com/g' /etc/apt/sources.list 2>/dev/null || \
    sed -i 's/deb.debian.org/mirrors.linode.com/g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || true

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt


# ==========================================
# STAGE 2: Development
# ==========================================
FROM python:3.10-slim AS dev

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

RUN sed -i 's/deb.debian.org/mirrors.linode.com/g' /etc/apt/sources.list 2>/dev/null || \
    sed -i 's/deb.debian.org/mirrors.linode.com/g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || true

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


# ==========================================
# STAGE 3: Production
# ==========================================
FROM python:3.10-slim AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

RUN sed -i 's/deb.debian.org/mirrors.linode.com/g' /etc/apt/sources.list 2>/dev/null || \
    sed -i 's/deb.debian.org/mirrors.linode.com/g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || true

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl

RUN groupadd -g 1001 python && \
    useradd -u 1001 -g python -s /bin/sh -m python

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv

COPY core/ ./core/
COPY adapters/ ./adapters/
COPY routers/ ./routers/
COPY schemas/ ./schemas/
COPY services/ ./services/
COPY main.py .

RUN chown -R python:python /app
USER python

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
