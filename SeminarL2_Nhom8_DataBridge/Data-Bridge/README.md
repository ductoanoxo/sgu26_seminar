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

## 🧪 Hướng dẫn Test Connect Data Source

### Khởi động test databases

```bash
docker compose -f docker-compose.test.yml up -d
```

### Thông tin kết nối

Mở **http://localhost:3000** → Click **Connect Data Source** → nhập thông tin bên dưới:

| Database | Host | Port | Database Name | Username | Password |
|---|---|---|---|---|---|
| **PostgreSQL** | `test-postgres` | `5432` | `shopdb` | `testuser` | `testpass` |
| **MySQL** | `test-mysql` | `3306` | `shopdb` | `testuser` | `testpass` |
| **MongoDB** | `test-mongodb` | `27017` | `shopdb` | _(bỏ trống)_ | _(bỏ trống)_ |
| **Redis** | `test-redis` | `6379` | `0` | _(bỏ trống)_ | _(bỏ trống)_ |
| **SQLite** | _(bỏ trống)_ | _(bỏ trống)_ | `/data/shopdb.db` | _(bỏ trống)_ | _(bỏ trống)_ |

> **Lưu ý SQLite**: `test-sqlite-init` chỉ chạy 1 lần để tạo file DB rồi tự thoát (`Exited 0`) — đây là **bình thường**, không phải lỗi.

### Dữ liệu test có sẵn

Mỗi database đều có 3 bảng với cùng nội dung:
- **orders** — 15 đơn hàng (Electronics & Fashion, các thành phố Việt Nam)
- **products** — 10 sản phẩm kèm giá và tồn kho
- **customers** — 8 khách hàng

### Gợi ý câu query để test NL2SQL

Sau khi import xong, thử các câu hỏi:
- *"Tổng doanh thu theo từng category"*
- *"Top 5 sản phẩm bán chạy nhất"*
- *"Doanh thu theo thành phố"*
- *"So sánh doanh thu tháng 1 và tháng 2"*

### Xóa test databases

```bash
docker compose -f docker-compose.test.yml down -v
```

---

## 💡 Tính năng Nổi bật

*   **Multi-Agent Pipeline**: Tách biệt nhiệm vụ giữa việc tạo SQL và thực thi để đảm bảo tính an toàn và chính xác.
*   **Hot Reload Everywhere**: Mọi thay đổi code ở Backend hay Frontend đều được cập nhật tức thì bên trong Docker container.
*   **Supabase Integration**: Tối ưu hóa kết nối qua Session Pooler giúp vượt qua rào cản IPv6 trong môi trường Docker.
*   **Rich UI/UX**: Giao diện Dashboard cao cấp với khả năng hiển thị kết quả dạng bảng và biểu đồ.

---

## 🔗 Các tác giả & Tài khoản Github

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=120&section=header" alt="header" />
</p>

| | | | |
| :---: | :---: | :---: | :---: |
| <a href="https://github.com/ductoanoxo"><img src="https://github-readme-stats.vercel.app/api?username=ductoanoxo&show_icons=true&hide_title=true&hide=issues,contribs,prs&rank_icon=github&hide_border=true"/></a> | <a href="https://github.com/Kietnehi"><img src="https://github-readme-stats.vercel.app/api?username=Kietnehi&show_icons=true&hide_title=true&hide=issues,contribs,prs&rank_icon=github&hide_border=true"/></a> | <a href="https://github.com/phatle224"><img src="https://github-readme-stats.vercel.app/api?username=phatle224&show_icons=true&hide_title=true&hide=issues,contribs,prs&rank_icon=github&hide_border=true"/></a> | <a href="https://github.com/nhdotvn"><img src="https://github-readme-stats.vercel.app/api?username=nhdotvn&show_icons=true&hide_title=true&hide=issues,contribs,prs&rank_icon=github&hide_border=true"/></a> |
| <img src="https://github.com/ductoanoxo.png" width="80"/> | <img src="https://github.com/Kietnehi.png" width="80"/> | <img src="https://github.com/phatle224.png" width="80"/> | <img src="https://github.com/nhdotvn.png" width="80"/> |
| <b><a href="https://github.com/ductoanoxo">Đức Toàn</a></b> | <b><a href="https://github.com/Kietnehi">Trương Phú Kiệt</a></b> | <b><a href="https://github.com/phatle224">Phát Lê</a></b> | <b><a href="https://github.com/nhdotvn">Lê Ngọc Hiệp</a></b> |
| Leader & Developer | AI Researcher | Data Engineer | AI Developer |
| <p align="center"><img src="https://img.shields.io/github/followers/ductoanoxo?style=for-the-badge"/> <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github-star-counter.workers.dev%2Fuser%2Fductoanoxo&query=%24.stars&style=for-the-badge&color=yellow&label=Stars&logo=github"/> <a href="https://github.com/ductoanoxo"><img src="https://img.shields.io/badge/Profile-GitHub-181717?style=for-the-badge&logo=github"/></a></p> | <p align="center"><img src="https://img.shields.io/github/followers/Kietnehi?style=for-the-badge"/> <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github-star-counter.workers.dev%2Fuser%2FKietnehi&query=%24.stars&style=for-the-badge&color=yellow&label=Stars&logo=github"/> <a href="https://github.com/Kietnehi"><img src="https://img.shields.io/badge/Profile-GitHub-181717?style=for-the-badge&logo=github"/></a></p> | <p align="center"><img src="https://img.shields.io/github/followers/phatle224?style=for-the-badge"/> <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github-star-counter.workers.dev%2Fuser%2Fphatle224&query=%24.stars&style=for-the-badge&color=yellow&label=Stars&logo=github"/> <a href="https://github.com/phatle224"><img src="https://img.shields.io/badge/Profile-GitHub-181717?style=for-the-badge&logo=github"/></a></p> | <p align="center"><img src="https://img.shields.io/github/followers/nhdotvn?style=for-the-badge"/> <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github-star-counter.workers.dev%2Fuser%2Fnhdotvn&query=%24.stars&style=for-the-badge&color=yellow&label=Stars&logo=github"/> <a href="https://github.com/nhdotvn"><img src="https://img.shields.io/badge/Profile-GitHub-181717?style=for-the-badge&logo=github"/></a></p> |

<p align="center">
  <a href="https://github.com/ductoanoxo/Agent_SQL">
    <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=236AD3&center=true&vCenter=true&width=500&lines=Agent+SQL+Project;Multi-Agent+NL2SQL+System;SGU+Seminar+Chuyen+De" alt="Typing SVG" />
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/SGU-Sai_Gon_University-0056D2?style=flat-square" alt="SGU" />
  <img src="https://img.shields.io/badge/Base-Ho_Chi_Minh_City-FF4B4B?style=flat-square" alt="HCMC" />
</p>

### 🛠 Tech Stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=docker,python,react,nextjs,supabase,postgres,fastapi,git" alt="Tech Stack" />
</p>

### 📘 AGENT SQL

<p align="center">
  <a href="https://github.com/ductoanoxo/Agent_SQL">
    <img src="https://img.shields.io/github/stars/ductoanoxo/Agent_SQL?style=for-the-badge&color=yellow" alt="Stars" />
    <img src="https://img.shields.io/github/forks/ductoanoxo/Agent_SQL?style=for-the-badge&color=orange" alt="Forks" />
    <img src="https://img.shields.io/github/issues/ductoanoxo/Agent_SQL?style=for-the-badge&color=red" alt="Issues" />
  </a>
</p>


<!-- Quote động -->
  <p align="center">
    <img src="https://quotes-github-readme.vercel.app/api?type=horizontal&theme=dark" alt="Daily Quote"/>
  </p>

  <p align="center">
  <i>Thank you for stopping by! Don’t forget to give this repo a <b>⭐️ Star</b> if you find it useful.</i>
  </p>

  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=80&section=footer"/>

  </div>



postgresql://postgres.dfrygylckiuxzmvyvcqv:Bacxiux349@@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres
mongodb+srv://toantra141:toantoan123@cnlthd.ijxnmqz.mongodb.net/?appName=CNLTHD
