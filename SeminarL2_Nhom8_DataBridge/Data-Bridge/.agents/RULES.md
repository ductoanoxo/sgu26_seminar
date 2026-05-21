# AGENT RULES - Agent SQL Project

## 0. Bắt buộc đọc trước khi làm bất cứ điều gì

Trước khi thực hiện bất kỳ task nào, agent **phải** đọc các file sau để nắm context toàn dự án:

- `.agents/skills/init/AGENTS.md` — Quy tắc hành vi chung của agent
- `.agents/skills/init/CLAUDE.md` — Cấu hình & hướng dẫn dành cho Claude
- `.agents/skills/init/GEMINI.md` — Cấu hình & hướng dẫn dành cho Gemini
- `README.md` — Tổng quan kiến trúc, tech stack, và mục tiêu dự án
- `docs/user_story.md` — Định hướng nghiệp vụ và phân quyền Agent (MỚI)

> Không đọc các file trên đồng nghĩa với việc làm việc thiếu context và sẽ dẫn đến sai sót.

---

## 1. Quy tắc Định tuyến Agent (Agent Routing)

Hệ thống hoạt động theo **Kiến trúc Multi-Agent**. Tuyệt đối không để một Agent ôm đồm mọi việc. Khi thực hiện task, bắt buộc phân luồng theo quy tắc sau:

- **SQL Agent (Bộ não)**: Gọi khi xử lý logic cốt lõi (NL2SQL), giao tiếp Database gốc, giải thích truy vấn hoặc thiết kế giao diện hiển thị.
- **QA Expert Agent (Người gác cổng)**: BẮT BUỘC gọi khi có yêu cầu kiểm thử. Không tự viết test lẻ tẻ. Agent này được thiết kế để chạy quy trình 5 bước: Sinh Test Case -> API Test -> K6 Load Test -> Playwright E2E -> Báo cáo.
- **DevSecOps Expert Agent (Xương sống)**: BẮT BUỘC gọi khi đụng tới Docker/Hạ tầng. Đảm bảo file được build đúng chuẩn Non-root và tự động quét bảo mật bằng Trivy (Secret leak, Vuln scan).

---

## 2. Skill theo ngữ cảnh (Context-based Skills)

### 2.1 Làm việc với Database / Supabase
- Đọc toàn bộ nội dung trong thư mục `.agents/skills/supabase/`
- Ưu tiên dùng Pooler Host (Session Mode) để hỗ trợ IPv4 trong Docker
- Không hardcode credentials — luôn đọc từ biến môi trường

### 2.2 Tóm tắt Feature / Workflow
- Làm theo hướng dẫn tại `.agents/skills/Summary/tom-tat.md`
- Lưu output tại `.agents/skills/Summary/content/<tên-file-kebab-case>.md`
- Không đoán — nếu thiếu thông tin, ghi rõ "Cần xác minh"

### 2.3 Build Frontend / UI
- Tuân thủ toàn bộ quy tắc trong `.agents/skills/frontend/SKILLS.md`
- Bắt buộc: dùng `requestAnimationFrame` cho animation video, không dùng CSS transitions
- Bắt buộc: giữ đúng hệ thống typography, spacing, và glassmorphism đã định nghĩa

### 2.4 Tích hợp AI / LLM
- Đọc file `.agents/skills/context/LLM_Gemini_openrouter_groq_tavily.md`
- Ưu tiên pattern code mới nhất trong file này. Không dùng code pattern cũ từ training data.

---

## 3. Kiến trúc Hệ thống & Vận hành An toàn (MỚI)

### 3.1 Cơ chế Read-only Proxy
- **CẤM TUYỆT ĐỐI** mọi lệnh DML/DDL (INSERT/UPDATE/DELETE/DROP) từ phía người dùng cuối. API bắt buộc phải dùng bộ lọc (filter) chặn các lệnh này ở tầng Backend trước khi truyền xuống Database gốc.
- Mọi câu truy vấn SELECT do AI sinh ra đều **PHẢI** được đính kèm giới hạn tài nguyên (Ví dụ: nối thêm `LIMIT 100`) và cấu hình Timeout chặt chẽ.

### 3.2 Cấu trúc Multi-Service
- **Port mapping** cố định: Frontend `3000`, Query Service `8001`, NL2SQL `8002`, API Gateway `8000`
- Các service giao tiếp qua HTTP nội bộ (Docker network) — không gọi trực tiếp ra ngoài khi không cần.

---

## 4. Bảo mật & Git Hygiene

### 4.1 Không để lộ Secrets
- **KHÔNG BAO GIỜ** commit các file: `.env`, `.env.local` lên GitHub.
- Trước khi tạo commit, kiểm tra `git status`. Nếu phát hiện secrets, thay thế ngay bằng biến môi trường.

### 4.2 Code rác & Message
- Các build artifacts (`node_modules/`, `.next/`, `__pycache__/`) phải nằm trong `.gitignore`.
- Dùng định dạng Commit: `<type>: <mô tả ngắn>` (VD: `feat: add NL2SQL logic`).

---

## 5. Quy tắc Code chung

### 5.1 Biến môi trường & Xử lý lỗi
- Mọi config nhạy cảm phải được đọc từ biến môi trường (cập nhật file `.env.example`).
- Lỗi phải được log lại đủ thông tin ở Backend, nhưng tuyệt đối không expose Stack Trace ra ngoài cho Client/Frontend.

### 5.2 YAGNI (You Aren't Gonna Need It)
- Chỉ làm đúng những gì task yêu cầu. Không thêm abstraction, helper, hay feature "phòng hờ" khi chưa có nhu cầu thực tế.

---

## 6. Kiểm tra trước khi báo hoàn thành

Trước khi nói "Đã xong", agent phải tự kiểm tra Checklist:
- [ ] Code có chạy được không? (syntax errors, import errors)
- [ ] Có để lộ secret hay push file rác không?
- [ ] Có đúng với phong cách Glassmorphism không?
- [ ] **(Bắt buộc)** Đã bàn giao cho **QA Expert Agent** chạy Full-stack Testing chưa?
- [ ] **(Bắt buộc)** Đã yêu cầu **DevSecOps Agent** rà soát lỗ hổng bằng Trivy chưa?
