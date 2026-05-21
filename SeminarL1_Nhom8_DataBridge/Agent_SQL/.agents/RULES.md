# AGENT RULES - Agent SQL Project

## 0. Bắt buộc đọc trước khi làm bất cứ điều gì

Trước khi thực hiện bất kỳ task nào, agent **phải** đọc các file sau để nắm context toàn dự án:

- `.agents/skills/init/AGENTS.md` — Quy tắc hành vi chung của agent
- `.agents/skills/init/CLAUDE.md` — Cấu hình & hướng dẫn dành cho Claude
- `.agents/skills/init/GEMINI.md` — Cấu hình & hướng dẫn dành cho Gemini
- `README.md` — Tổng quan kiến trúc, tech stack, và mục tiêu dự án

> Không đọc các file trên đồng nghĩa với việc làm việc thiếu context và sẽ dẫn đến sai sót.

---

## 1. Skill theo ngữ cảnh (Context-based Skills)

### 1.1 Làm việc với Database / Supabase
Khi task liên quan đến database, truy vấn SQL, kết nối Supabase, hoặc schema:
- Đọc toàn bộ nội dung trong thư mục `.agents/skills/supabase/`
- Ưu tiên dùng Pooler Host (Session Mode) để hỗ trợ IPv4 trong Docker
- Không hardcode credentials — luôn đọc từ biến môi trường

### 1.2 Tóm tắt Feature / Workflow
Khi người dùng yêu cầu tạo tài liệu, tóm tắt luồng xử lý, hoặc giải thích một chức năng:
- Làm theo hướng dẫn tại `.agents/skills/Summary/tom-tat.md`
- Lưu output tại `.agents/skills/Summary/content/<tên-file-kebab-case>.md`
- Không đoán — nếu thiếu thông tin, ghi rõ "Cần xác minh"

### 1.3 Build Frontend / UI
Khi task liên quan đến giao diện, component, hay layout:
- Tuân thủ toàn bộ quy tắc trong `.agents/skills/frontend/SKILLS.md`
- Bắt buộc: dùng `requestAnimationFrame` cho animation video, không dùng CSS transitions
- Bắt buộc: giữ đúng hệ thống typography, spacing, và glassmorphism đã định nghĩa
- Không tự ý thay đổi design system nếu không có yêu cầu rõ ràng từ người dùng

### 1.4 Cập nhật / Sử dụng API & Thư viện mới
Khi task liên quan đến OpenRouter, Google Gemini, Groq, Tavily, hoặc bất kỳ thư viện AI nào trong project:
- Đọc file `.agents/skills/context/LLM_Gemini_openrouter_groq_tavily.md`
- Ưu tiên pattern code mới nhất trong file này, không dùng code pattern cũ từ training data
- Không hallucinate tên tham số hay API method — chỉ dùng những gì có trong tài liệu

---

## 2. Bảo mật & Git Hygiene

### 2.1 Tuyệt đối không để lộ secrets
- **KHÔNG BAO GIỜ** commit các file: `.env`, `.env.local`, `.env.production`, hay bất kỳ file chứa API key/credentials nào lên GitHub
- Trước khi tạo commit, kiểm tra `git status` để đảm bảo không có file nhạy cảm bị stage
- Nếu phát hiện secrets trong code, thay thế ngay bằng biến môi trường và ghi chú vào `.env.example`

### 2.2 Không push file rác
Các loại file sau **không được** commit:
- `*.log`, `*.tmp`, `*.cache`
- Thư mục: `__pycache__/`, `.pytest_cache/`, `node_modules/`, `.next/` (build artifacts)
- File IDE cá nhân: `.vscode/settings.json` (nếu chứa config local), `.idea/`
- File OS: `.DS_Store`, `Thumbs.db`
- Đảm bảo các pattern này đều có trong `.gitignore` trước khi làm việc

### 2.3 Commit message rõ ràng
- Dùng định dạng: `<type>: <mô tả ngắn>` (VD: `feat: add NL2SQL retry logic`)
- Các type hợp lệ: `feat`, `fix`, `refactor`, `docs`, `chore`, `style`, `test`
- Không commit code đang broken hoặc chưa test

---

## 3. Quy tắc code chung

### 3.1 Biến môi trường
- Mọi config nhạy cảm (API key, DB URL, port) phải được đọc từ biến môi trường
- Mỗi service phải có file `.env.example` cập nhật khi thêm biến mới
- Không đặt giá trị mặc định là secret thật trong code

### 3.2 Không thêm tính năng không được yêu cầu
- Chỉ làm đúng những gì task yêu cầu
- Không refactor code ngoài phạm vi task
- Không thêm abstraction, helper, hay feature "phòng hờ" khi chưa có nhu cầu thực tế

### 3.3 Không thêm comment không cần thiết
- Chỉ comment khi lý do (WHY) không hiển nhiên từ code
- Không comment mô tả WHAT (code đọc được là đủ)
- Không để lại comment debug như `# TODO`, `# FIXME` khi commit

### 3.4 Xử lý lỗi đúng tầng
- Chỉ validate input tại system boundary (API endpoints, user input)
- Không wrap mọi thứ bằng try/catch nếu không có xử lý cụ thể
- Log lỗi đủ thông tin để debug nhưng không expose stack trace ra client

---

## 4. Kiến trúc Multi-Service

- **Port mapping** cố định: Frontend `3000`, Query Service `8001`, NL2SQL `8002`, API Gateway `8000`
- Các service giao tiếp qua HTTP nội bộ (Docker network) — không gọi trực tiếp ra ngoài khi không cần
- Thay đổi schema hoặc API contract giữa các service phải cập nhật tất cả các bên liên quan đồng thời
- Không thay đổi Docker Compose config mà không có lý do và không thông báo cho người dùng

---

## 5. Kiểm tra trước khi báo hoàn thành

Trước khi nói "Đã xong", agent phải tự kiểm tra:
- [ ] Code có chạy được không? (syntax errors, import errors)
- [ ] Có để lộ secret hay push file rác không?
- [ ] Có đúng với skill/design system đã quy định không?
- [ ] Có vi phạm kiến trúc multi-service không?
- [ ] Với UI task: có test trên browser chưa (golden path + edge cases)?
