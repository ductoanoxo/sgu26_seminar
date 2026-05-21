---
name: Docker Management
description: Hướng dẫn quản lý Docker Compose, thiết lập Hot-reload và quản lý Ports cho môi trường phát triển.
---

# Quản lý Docker (Compose, Hot-reload, Ports)

Tài liệu này hướng dẫn cách cấu hình, khởi chạy và quản lý môi trường phát triển cục bộ bằng Docker và Docker Compose cho hệ thống gồm Frontend và Backend.

## 1. Quản lý Docker Compose
Dùng `docker-compose.yml` (hoặc `docker-compose.dev.yml` cho môi trường phát triển) để định nghĩa toàn bộ stack.

**Các lệnh cơ bản thường dùng:**
- **Build và khởi động hệ thống dạng ngầm (detached):**
  ```bash
  docker compose up --build -d
  ```
- **Xem logs theo thời gian thực:**
  ```bash
  docker compose logs -f [service_name]
  ```
- **Dừng và xóa các container, network liên quan:**
  ```bash
  docker compose down
  ```
- **Xóa toàn bộ volumes (LƯU Ý: thao tác này sẽ xóa sạch dữ liệu của database cục bộ):**
  ```bash
  docker compose down -v
  ```

## 2. Thiết lập Hot-Reload (Môi trường Dev)
Hot-reload giúp code tự động cập nhật ngay khi bạn lưu file trên máy host mà không cần build lại image.

### 2.1 Backend (FastAPI / Uvicorn)
- **Mount volume:** Map thư mục code gốc vào container.
- **Lệnh chạy:** Sử dụng tùy chọn `--reload` của uvicorn.
```yaml
services:
  backend:
    build:
      context: ./backend
      target: development
    volumes:
      - ./backend:/app  # Mount source code
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2.2 Frontend (Vite / React)
- **Mount volume:** Map thư mục mã nguồn. Ngoại trừ `node_modules` (dùng named volume) để tránh xung đột hệ điều hành giữa Host và Container.
- **Lệnh chạy:** Sử dụng máy chủ dev mặc định của Vite. Thêm tham số `--host` để map được ra ngoài.
```yaml
services:
  frontend:
    build:
      context: ./frontend
    volumes:
      - ./frontend:/app
      - /app/node_modules # Giữ node_modules bên trong container
    command: npm run dev -- --host
```

## 3. Quản lý Ports (Cổng giao tiếp)
Quy tắc map port trong `docker-compose.yml`:
`"HOST_PORT:CONTAINER_PORT"`

- Tránh xung đột với các service đang chạy sẵn trên máy host.
- **Frontend (Vite):** Thường map `5173:5173` hoặc `3000:5173`.
- **Backend (FastAPI):** Thường map `8000:8000`.
- **Database (PostgreSQL):** Thường map `5432:5432`.

### Xử lý lỗi "Port is already allocated"
1. Kiểm tra tiến trình nào đang chiếm cổng trên host (trên Linux/macOS):
   ```bash
   lsof -i :8000
   ```
2. Dừng tiến trình đó (`kill -9 <PID>`) hoặc thay đổi số `HOST_PORT` trong file compose (ví dụ đổi sang `8001:8000`).

## 4. Quản lý `.env` trong Docker
Để truyền biến môi trường vào container một cách bảo mật, sử dụng thuộc tính `env_file`:
```yaml
services:
  backend:
    env_file:
      - .env
```
Docker Compose sẽ tự động load tất cả các biến môi trường từ file `.env` nằm cùng cấp. Không nên commit file `.env` này lên Git (hãy đảm bảo đã thêm vào `.gitignore`).
