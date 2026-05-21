# Quy trình Xây dựng Phần mềm (Software Development Process)

Tài liệu này mô tả quy trình phát triển dự án **Agent SQL** - hệ thống đa tác vụ chuyển đổi ngôn ngữ tự nhiên thành truy vấn SQL. Quy trình này kết hợp các phương pháp Agile hiện đại và cách tiếp cận "AI-Centric Development" (Phát triển lấy AI làm trung tâm), bám sát các **User Story** và **Persona** đã đề ra.

---

## 1. Các Giai đoạn Phát triển chính

### Giai đoạn 1: Phân tích và Thiết kế (Planning & Analysis)
*   **Phân tích Persona & User Story:** Xác định nhu cầu cụ thể của từng nhóm người dùng (Người dùng nghiệp vụ, Nhà phân tích, DBA, Trưởng nhóm) dựa trên tài liệu `user_story.md`.
*   **Xác định nghiệp vụ (Business Logic):** Phân tích các câu hỏi người dùng thường gặp và cấu trúc dữ liệu tương ứng trong Supabase.
*   **Thiết kế Schema:** Thiết kế cơ sở dữ liệu PostgreSQL trên Supabase, đảm bảo các bảng có quan hệ chặt chẽ và tên cột rõ ràng để AI dễ hiểu.
*   **Thiết kế Agent:** Định nghĩa vai trò của các Agent (Architect, SQL Generator, Validator) để giải quyết các bài toán về ảo giác (hallucination) và bảo mật.

### Giai đoạn 2: Thiết lập Môi trường (Environment Setup)
*   **Cấu hình Hạ tầng:** Sử dụng Docker và Docker Compose để đồng bộ môi trường phát triển cho tất cả các microservices.
*   **Quản lý Biến môi trường:** Thiết lập các file `.env` cho API Keys (OpenRouter, Gemini) và cấu hình kết nối Database.
*   **Supabase Integration:** Cấu hình Connection Pooling để tối ưu hóa hiệu suất kết nối từ các dịch vụ Backend.

### Giai đoạn 3: Quy trình Phát triển AI-Centric (Agentic Workflow)
Đây là bước cốt lõi trong dự án, nơi con người phối hợp với AI Agent để xây dựng code:
1.  **Gửi yêu cầu kèm Context:** Cung cấp prompt chi tiết cùng với các tệp luật (`AGENTS.md`) để AI nắm bắt tiêu chuẩn dự án.
2.  **AI Phân tích và Thực thi:** AI tự động đọc các quy tắc về UI (Glassmorphism), Tech stack (Next.js, FastAPI) và đề xuất mã nguồn.
3.  **Review và Kiểm chứng:** Con người kiểm tra mã nguồn do AI tạo ra, chạy thử nghiệm trên môi trường Docker để đảm bảo tính đúng đắn.
4.  **Cập nhật Tri thức (Knowledge Loop):** Nếu có quy ước mới, cập nhật vào file `AGENTS.md` để AI học tập cho các lần sau.

### Giai đoạn 4: Phát triển Microservices & Tính năng
*   **API Gateway:** Xây dựng điểm tiếp nhận trung tâm bằng FastAPI để điều phối luồng và lưu trữ lịch sử truy vấn (User Story #5).
*   **NL2SQL Service:** Triển khai Multi-Agent Pipeline xử lý ngôn ngữ tự nhiên, tập trung vào việc hiểu Schema (User Story #3).
*   **Query Service:** Xây dựng trình thực thi SQL bảo mật, tích hợp các bộ lọc để ngăn chặn SQL Injection và cưỡng chế giới hạn thời gian/số dòng (User Story #4).
*   **Frontend:** Phát triển Dashboard bằng Next.js, hỗ trợ hiển thị SQL, giải thích tự nhiên và biểu đồ trực quan (User Story #2, #6).

### Giai đoạn 5: Kiểm thử và Đảm bảo Chất lượng (QA & Testing)
*   **Kiểm thử theo Tiêu chí Chấp nhận (Acceptance Criteria):** Đảm bảo mọi tính năng đều đạt các tiêu chí đã đề ra trong `user_story.md`.
*   **SQL Validation:** Kiểm tra nghiêm ngặt tính an toàn của các câu lệnh AI tạo ra (Chỉ cho phép lệnh `SELECT/CTE`).
*   **Integration Testing:** Kiểm thử tích hợp giữa Frontend và các dịch vụ Backend qua API Gateway.
*   **Performance Testing:** Đo lường thời gian phản hồi của LLM và tốc độ thực thi truy vấn trên Database.

### Giai đoạn 6: Triển khai và Giám sát (Deployment & Monitoring)
*   **Containerization:** Đóng gói toàn bộ hệ thống vào Docker Images.
*   **Monitoring:** Theo dõi logs của các service thông qua Docker logs hoặc các công cụ giám sát tập trung.
*   **Maintenance:** Cập nhật định kỳ các thư viện AI và tối ưu hóa Prompt để cải thiện độ chính xác của SQL.

---

## 2. Tiêu chuẩn và Quy ước (Standards)

| Thành phần | Quy ước tiêu chuẩn |
| :--- | :--- |
| **Mã nguồn** | Tuân thủ PEP8 (Python) và ESLint/Prettier (React/Next.js). |
| **Giao diện** | Phong cách Modern SaaS, Glassmorphism, hỗ trợ Dark/Light mode. |
| **Bảo mật** | **Security by Design**: Chỉ cho phép quyền Read-only (SELECT/CTE). Chặn hoàn toàn DML/DDL. |
| **Dữ liệu** | Hỗ trợ đa dạng nguồn (SQL, NoSQL, File import) theo nhu cầu nghiệp vụ. |
| **Tài liệu** | Mọi tính năng mới phải được cập nhật vào `docs/` và `README.md`. |

---

## 3. Lộ trình Cải tiến (Iterative Improvement)

Dự án không dừng lại ở bản phát hành đầu tiên mà liên tục được cải tiến theo mô hình xoắn ốc:
1.  Thu thập phản hồi từ các nhóm **Persona** khác nhau về độ chính xác và tính hữu dụng.
2.  Tinh chỉnh (Fine-tuning) Prompt hoặc cập nhật Semantic Layer (Lớp ngữ nghĩa) để AI hiểu sâu hơn về dữ liệu đặc thù.
3.  Phát triển các tính năng nâng cao (Dashboard cá nhân hóa, Hội thoại đa bước) theo `ROADMAP.md`.

---
*Tài liệu này được cập nhật dựa trên User Stories để đảm bảo quy trình phát triển luôn hướng tới người dùng cuối.*
