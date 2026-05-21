# 🐋 Hướng dẫn Hạ tầng Docker - Agent SQL

Tài liệu này chi tiết cách hệ thống **Agent SQL** được đóng gói, điều phối và tối ưu hóa bằng Docker.

## 1. Tổng quan Kiến trúc Container
Hệ thống sử dụng mô hình microservices, trong đó mỗi thành phần chạy trong một container riêng biệt, giao tiếp qua mạng nội bộ Docker.

| Service | Port (Host) | Vai trò | Công nghệ |
| :--- | :--- | :--- | :--- |
| **frontend** | 3000 | Giao diện Dashboard | Next.js 14 |
| **api-gateway** | 8000 | Điều phối & Orchestrator | FastAPI |
| **nl2sql-service** | 8002 | Xử lý AI Multi-Agent | Python (CrewAI) |
| **query-service** | 8001 | Thực thi SQL & Kết nối DB | Python (Psycopg2) |
| **kafka** | 9092 | Message Broker | KRaft Mode |
| **kafka-ui** | 8080 | Giao diện quản lý & Monitor Kafka | - |

---

## 2. Chiến lược Build Dockerfile (Production-Ready)

Tất cả các Python services (`api-gateway`, `nl2sql-service`, `query-service`) đều tuân thủ các tiêu chuẩn nghiêm ngặt:

### 🚀 Multi-stage Builds
Chúng tôi chia quá trình build thành 3 giai đoạn rõ rệt:
1.  **`builder` stage**: 
    - Cài đặt công cụ build (`build-essential`, `libpq-dev`).
    - Tạo virtual environment (`/opt/venv`).
    - Cài đặt dependencies từ `requirements.txt`.
2.  **`runner` stage** (Dành cho môi trường Production):
    - Chỉ copy virtual environment và mã nguồn cần thiết từ stage builder.
    - Sử dụng image `python:3.10-slim` để tối giản kích thước.
    - Không chứa các công cụ build dư thừa, giảm diện tích tấn công (Attack Surface).
3.  **`dev` stage** (Mặc định trong Docker Compose):
    - Kế thừa từ builder.
    - Cấu hình hỗ trợ **Hot-reload** thông qua flag `--reload` của Uvicorn.
    - Mount volume trực tiếp từ máy host để cập nhật code tức thì.

### 🛡️ Bảo mật (Security First)
- **Non-root User**: Container chạy ứng dụng dưới quyền user `python` (UID 1001). Ngay cả khi container bị xâm nhập, kẻ tấn công cũng không có quyền root trên hệ điều hành host.
- **Selective Copy**: Chỉ copy những folder cần thiết (core, domain, routers...) thay vì `COPY . .` mù quáng, tránh lọt các file nhạy cảm hoặc rác vào image.

### ⚡ Tối ưu hiệu năng Build
- **BuildKit Caching**: Sử dụng cơ chế `--mount=type=cache` cho cả `apt` và `pip`. Việc rebuild khi thêm 1 thư viện mới chỉ tốn vài giây thay vì phải tải lại toàn bộ.
- **Singapore Mirrors**: Tự động nhận diện và chuyển đổi sang các mirror tại Singapore (`mirrors.linode.com`) để đạt tốc độ tải tối đa tại Việt Nam.

---

## 3. Điều phối với Docker Compose

Tệp `docker-compose.yml` đóng vai trò là "nhạc trưởng" điều phối các service.

### Cơ chế Healthcheck & Dependency Management
Hệ thống không khởi động tất cả cùng lúc (tránh lỗi kết nối):
- `api-gateway` sẽ đợi cho đến khi `kafka`, `nl2sql-service` và `query-service` báo trạng thái **Healthy**.
- Trạng thái **Healthy** của Kafka được xác định bằng cách thực hiện lệnh kiểm tra danh sách topic thực tế bên trong container.

### Mạng nội bộ (Isolated Networking)
- Một bridge network riêng được tạo ra. Các service liên lạc với nhau bằng hostname (VD: `kafka:9092`).
- Chỉ có cổng 3000 (Frontend) và 8000 (Gateway) là được public ra ngoài. Các service AI và Query được ẩn hoàn toàn sau Gateway.

---

## 4. Hướng dẫn vận hành

### Khởi chạy nhanh (Development)
```bash
docker-compose up -d --build
```

### Xem tình trạng hệ thống
```bash
docker-compose ps
```

### Kiểm tra Logs thời gian thực
```bash
# Xem log của AI Service
docker-compose logs -f nl2sql-service
```

### Dọn dẹp hệ thống
```bash
# Xóa container và các volume dữ liệu tạm (như Kafka data)
docker-compose down -v
```

---

## 5. Lưu ý cho Developer

- **File `.dockerignore`**: Luôn đảm bảo `__pycache__`, `.env`, `.git` và các thư mục test không được đẩy vào build context.
- **Biến môi trường**: Các file `.env` được nạp tự động qua `env_file:` trong compose. Đừng bao giờ commit file `.env` chứa secret lên Git.
- **Port Mapping**: Nếu bạn muốn chạy service backend local (ngoài Docker) để debug, hãy lưu ý port mapping (8001 cho Query, 8002 cho NL2SQL).
