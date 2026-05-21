---
name: docker-expert
description: Triggers whenever the user asks to write, optimize, fix, or configure Dockerfile, docker-compose.yml, or Docker infrastructure. Contains directives for optimal containerized environments.
---

# Docker & Docker Compose: AI Assistant Directives

Khi người dùng yêu cầu tạo, cập nhật, hoặc tối ưu hóa file `Dockerfile` hay `docker-compose.yml`, bạn **PHẢI** tuân thủ nghiêm ngặt các chỉ thị và nguyên tắc (Best Practices) sau đây.

---

## 1. Hướng dẫn và Chỉ thị cho `Dockerfile`

### 1.1 Sử dụng Multi-stage Builds

Luôn phân tách thành nhiều stage, thông thường gồm `builder`, `runner` (production) và `dev`:

```dockerfile
FROM python:3.10-slim AS builder   # Cài dependencies
FROM python:3.10-slim AS runner    # Production image gọn nhẹ
FROM python:3.10-slim AS dev       # Dev image với --reload
```

- Chỉ copy `/opt/venv` từ `builder` sang `runner`/`dev` — **KHÔNG** cài lại pip ở runtime stage.
- Chỉ định `target: dev` trong `docker-compose.yml` để chọn đúng stage.

### 1.2 Base Image Nhẹ (Lightweight)

- **Bắt buộc** dùng `alpine` hoặc `slim`: `node:20-alpine`, `python:3.10-slim`.
- Chỉ dùng full OS khi thực sự cần C-bindings phức tạp.

### 1.3 Tối ưu Layer Cache — Quy tắc QUAN TRỌNG NHẤT

**Thứ tự COPY phải đúng:**

```dockerfile
# ✅ ĐÚNG — copy dependency file trước, source code sau
COPY requirements.txt .
RUN pip install -r requirements.txt   # ← Cache hit nếu requirements.txt không đổi
COPY . .                              # ← Chỉ layer này rebuild khi sửa code

# ❌ SAI — copy toàn bộ trước thì pip luôn bị invalidate
COPY . .
RUN pip install -r requirements.txt
```

**NGHIÊM CẤM dùng `PIP_NO_CACHE_DIR=1` cùng với `--mount=type=cache`:**

```dockerfile
# ❌ SAI — conflict: 2 setting triệt tiêu nhau, pip redownload mỗi lần build
ENV PIP_NO_CACHE_DIR=1
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# ✅ ĐÚNG — chỉ dùng cache mount, không set PIP_NO_CACHE_DIR
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

**Sử dụng cache mount cho apt và npm:**

```dockerfile
# apt cache
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends <packages>

# npm cache
RUN --mount=type=cache,target=/root/.npm \
    npm ci
```

### 1.4 Bảo mật với Non-root User

```dockerfile
RUN groupadd -g 1001 python && \
    useradd -u 1001 -g python -s /bin/sh -m python
RUN chown -R python:python /app
USER python
```

### 1.5 `.dockerignore` — PHẢI CÓ và PHẢI ĐÚNG

**Lỗi phổ biến:** Pattern `__pycache__/` chỉ match thư mục root, KHÔNG match nested.

```dockerignore
# ✅ ĐÚNG — dùng ** để match tất cả subdirectories
__pycache__/
**/__pycache__/
*.py[cod]
.pytest_cache/
**/.pytest_cache/

# Tests không cần trong production
tests/

# Git history
.git
.gitignore

# Secrets
.env

# Docker files chính nó
Dockerfile
.dockerignore
```

**Cho Node/Frontend:**
```dockerignore
.git
.gitignore
node_modules
.next
.env*
Dockerfile
.dockerignore
```

### 1.6 Xử lý Legacy Packages (ví dụ: openai-whisper)

Package dùng `setup.py` cũ cần `setuptools` (cung cấp `pkg_resources`):

```dockerfile
# setuptools required by openai-whisper (uses legacy setup.py with pkg_resources)
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade setuptools && \
    pip install -r requirements.txt
```

### 1.7 Hot Reload trong Dev Stage

**Python (uvicorn):**
```dockerfile
FROM python:3.10-slim AS dev
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
# Source code sẽ được override bởi volume mount
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**Node.js/Next.js:**
```dockerfile
FROM node:20-alpine AS deps
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci

FROM deps AS dev
WORKDIR /app
ENV NODE_ENV=development
COPY . .    # Baseline — volume mount sẽ override
CMD ["npm", "run", "dev"]
```

---

## 2. Hướng dẫn và Chỉ thị cho `docker-compose.yml`

### 2.1 Hot Reload trên Windows + Docker Desktop

File system events (inotify) **KHÔNG được propagate** từ Windows host vào container qua WSL2 volume mounts. **PHẢI** bật polling mode:

```yaml
services:
  # Python services (uvicorn)
  api-gateway:
    environment:
      - WATCHFILES_FORCE_POLLING=true   # Bắt buộc trên Windows

  # Frontend (Next.js)
  frontend:
    environment:
      - WATCHPACK_POLLING=true          # Webpack polling
      - CHOKIDAR_USEPOLLING=true        # Legacy fallback
```

**Và trong `next.config.ts`:**
```typescript
const nextConfig: NextConfig = {
  // KHÔNG dùng turbopack: {} — nó override webpack và phá polling
  webpack: (config, { dev }) => {
    if (dev) {
      config.watchOptions = {
        poll: 1000,           // Kiểm tra mỗi 1 giây
        aggregateTimeout: 300,
      };
    }
    return config;
  },
};
```

### 2.2 Cấu trúc Volume cho Dev

```yaml
services:
  # Python service — chỉ mount source, venv từ image
  api-gateway:
    volumes:
      - ./services/api-gateway:/app   # Source code mount

  # Frontend — bảo vệ node_modules bằng anonymous volume
  frontend:
    volumes:
      - ./frontend:/app               # Source code mount
      - /app/node_modules             # ← Anonymous volume bảo vệ node_modules
```

### 2.3 Restart Policy

```yaml
# ✅ ĐÚNG cho Development — chỉ restart khi crash
restart: unless-stopped

# ❌ TRÁNH — containers tự start mỗi lần reboot máy, tốn RAM
restart: always
```

### 2.4 Quản lý Environment Variables

```yaml
# ✅ ĐÚNG — nạp từ file, không hardcode
env_file:
  - ./services/api-gateway/.env
environment:
  - SERVICE_PORT=8000   # Chỉ override các giá trị không secret
```

- **NGHIÊM CẤM** hardcode credentials (password, JWT secret, API key) trực tiếp trong `environment:`.
- File `.env` phải có trong `.gitignore`.

### 2.5 Healthcheck và depends_on

```yaml
services:
  api-gateway:
    depends_on:
      kafka:
        condition: service_healthy    # ← Đợi kafka healthy thực sự
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
```

---

## 3. Checklist Trước Khi Commit

| Hạng mục | Kiểm tra |
|---|---|
| `PIP_NO_CACHE_DIR` | ❌ KHÔNG có — dùng `--mount=type=cache` thay thế |
| Thứ tự COPY | `requirements.txt` → `pip install` → `COPY . .` |
| `.dockerignore` | Có `**/__pycache__/`, `.git`, `tests/`, `.env` |
| import-service | Có `.dockerignore` riêng (thường bị quên) |
| `restart` policy | `unless-stopped` (không dùng `always` cho dev) |
| Hot reload Windows | `WATCHFILES_FORCE_POLLING` + `WATCHPACK_POLLING` |
| `turbopack` | KHÔNG có trong `next.config.ts` nếu dùng polling |
| Non-root user | `USER python` / `USER nextjs` trong production stage |
| Legacy packages | `pip install --upgrade setuptools` trước pip install |
