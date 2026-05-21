# 🤖 Agent SQL: Multi-Agent NL2SQL System

Agent SQL là một hệ thống đa tác vụ (Multi-Agent) mạnh mẽ, được thiết kế để chuyển đổi ngôn ngữ tự nhiên thành các truy vấn SQL chính xác và thực thi chúng trực tiếp trên cơ sở dữ liệu Supabase. Dự án được xây dựng với kiến trúc microservices hiện đại, tối ưu hóa cho hiệu suất và khả năng mở rộng.

---

## 🏗️ Kiến trúc Hệ thống

Hệ thống bao gồm 4 thành phần chính (Microservices):

1.  **🚀 API Gateway (Port 8000)**: Điểm tiếp nhận trung tâm, chịu trách nhiệm điều phối luồng dữ liệu giữa Frontend và các dịch vụ Backend, quản lý lịch sử truy vấn.
2.  **🧠 NL2SQL Service (Port 8002)**: Hệ thống Multi-Agent Pipeline sử dụng LLM (OpenRouter/Gemini) để:
    *   Phân tích ý định người dùng.
    *   Kiểm tra Schema cơ sở dữ liệu.
    *   Tạo câu lệnh SQL tối ưu.
3.  **🗄️ Query Service (Port 8001)**: Đảm nhận việc kết nối bảo mật tới Supabase PostgreSQL và thực thi các câu lệnh SQL đã được kiểm duyệt.
4.  **🌐 Frontend (Port 3000)**: Giao diện người dùng hiện đại được xây dựng bằng Next.js, cung cấp trải nghiệm Dashboard trực quan và mượt mà.

---

## 🛠️ Tech Stack

*   **Backend**: Python (FastAPI, Pydantic, Psycopg2).
*   **Frontend**: Next.js, React, TailwindCSS.
*   **AI Engine**: OpenRouter (GPT-4o Mini), Google Gemini.
*   **Database**: Supabase (PostgreSQL) với Connection Pooling.
*   **DevOps**: Docker, Docker Compose (hỗ trợ Hot Reload cho toàn bộ services).

---

## 🚀 Hướng dẫn Cài đặt

### 1. Yêu cầu hệ thống
*   Docker & Docker Compose.
*   API Key từ OpenRouter hoặc Google Gemini.
*   Cơ sở dữ liệu Supabase đã có bảng dữ liệu.

### 2. Cấu hình Môi trường
Tạo các file `.env` dựa trên các file `.env.example` trong mỗi thư mục service:

*   **NL2SQL Service**: Cấu hình `OPENROUTER_API_KEY` và `LLM_PROVIDER`.
*   **Query Service**: Cấu hình thông tin kết nối Supabase (Sử dụng Pooler Host để hỗ trợ IPv4).

### 3. Khởi chạy với Docker
Sử dụng một lệnh duy nhất để khởi động toàn bộ hệ thống ở chế độ phát triển (Hot Reload):

```bash
docker compose up --build
```

Sau khi hoàn tất, bạn có thể truy cập:
*   Dashboard: [http://localhost:3000](http://localhost:3000)
*   API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📂 Cấu trúc Thư mục

```text
Seminar_Final/
├── frontend/               # Next.js Application
├── services/
│   ├── api-gateway/        # FastAPI Orchestrator
│   ├── nl2sql-service/     # AI Agent Engine
│   └── query-service/      # Database Executor
├── database/               # SQL Scripts & Seeds
└── docker-compose.yml      # Docker Orchestration
```

---

## 💡 Tính năng Nổi bật

*   **Multi-Agent Pipeline**: Tách biệt nhiệm vụ giữa việc tạo SQL và thực thi để đảm bảo tính an toàn và chính xác.
*   **Hot Reload Everywhere**: Mọi thay đổi code ở Backend hay Frontend đều được cập nhật tức thì bên trong Docker container.
*   **Supabase Integration**: Tối ưu hóa kết nối qua Session Pooler giúp vượt qua rào cản IPv6 trong môi trường Docker.
*   **Rich UI/UX**: Giao diện Dashboard cao cấp với khả năng hiển thị kết quả dạng bảng và biểu đồ.

---

## 📝 Giấy phép
Dự án được thực hiện cho mục đích nghiên cứu Seminar.
