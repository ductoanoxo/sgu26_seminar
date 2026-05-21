# Product Requirements Document (PRD) - Agent SQL

## 1. Tổng quan Sản phẩm (Product Overview)
**Agent SQL** là một nền tảng phân tích dữ liệu tự phục vụ (Self-service Analytics Platform) được vận hành bởi AI. Sản phẩm giải quyết bài toán cốt lõi: Làm thế nào để người dùng không có kiến thức lập trình vẫn có thể truy vấn các cơ sở dữ liệu phức tạp một cách nhanh chóng, trong khi vẫn đảm bảo **an toàn tuyệt đối** cho hệ thống Database gốc.

Tầm nhìn của Agent SQL là "Bình dân hóa dữ liệu" (Democratizing data) thông qua giao tiếp bằng ngôn ngữ tự nhiên (NL2SQL), đồng thời thiết lập một "Vùng đệm an toàn" (Zero-Risk Proxy) cho giới quản trị viên IT.

---

## 2. Đối tượng Người dùng (Target Personas)

Sản phẩm tập trung phục vụ 2 nhóm người dùng có lợi ích đan xen nhau:

### 2.1 Người dùng cuối (End-User: Business, PM, Data Analyst)
- **Nỗi đau:** Chờ đợi đội IT xuất báo cáo dữ liệu quá lâu; không rành viết SQL.
- **Mục tiêu:** Gõ câu hỏi bằng tiếng Việt -> Nhận dữ liệu dạng bảng/biểu đồ ngay lập tức -> Lưu lịch sử và chia sẻ cho team.

### 2.2 Quản trị viên Hệ thống (Admin: DBA, Data Engineer)
- **Nỗi đau:** Bị làm phiền bởi các yêu cầu xuất dữ liệu lặt vặt (ad-hoc); rủi ro sập Server nếu cấp quyền DB trực tiếp cho người ngoài.
- **Mục tiêu:** Nhập cấu hình kết nối 1 lần duy nhất; ép buộc các giới hạn tài nguyên khắt khe (chặn lệnh Ghi/Xóa, giới hạn timeout) để bảo vệ hệ thống gốc.

---

## 3. Kiến trúc Multi-Agent (AI Orchestration)

Điểm khác biệt cốt lõi của Agent SQL là hệ thống được vận hành bởi **3 AI Agent chuyên trách**, hoạt động theo chuỗi dây chuyền công nghiệp:

1. 🧠 **SQL Agent (Core Engine - Não bộ)**: 
   - Nhiệm vụ: Đọc cấu trúc Database (Schema), xử lý chuyển đổi từ Ngôn ngữ tự nhiên sang SQL an toàn (Chỉ SELECT/CTE). Dịch ngược SQL sang tiếng Việt để giải thích cho End-user và gợi ý biểu đồ hiển thị.
2. 🕵️ **QA Expert Agent (Gatekeeper - Gác cổng)**: 
   - Nhiệm vụ: Phụ trách toàn bộ vòng đời kiểm thử tự động. Khi có tính năng mới, Agent này tự động chạy chuỗi 5 bước: Sinh Test Case -> Test API (Pytest) -> Test Performance (K6) -> Test Frontend UI (Playwright) -> Xuất Báo cáo.
3. 🛡️ **DevSecOps Expert Agent (Backbone - Xương sống)**: 
   - Nhiệm vụ: Xử lý đóng gói hệ thống (Docker) bắt buộc theo chuẩn Non-root. Tự động rà soát bảo mật (Trivy Scan) để dò tìm lỗ hổng phần mềm, cấu hình sai hoặc lộ lọt Secret Key/Mật khẩu trước khi đưa lên Production.

---

## 4. Yêu cầu Chức năng (Functional Requirements)

### 4.1 Khối Chức năng Quản trị (Admin)
- **F1. Quản lý Kết nối Data:** Cho phép nhập Connection String (PostgreSQL/Supabase) hoặc tải lên file dữ liệu (CSV/JSON). Mật khẩu được mã hóa ở tầng Backend.
- **F2. Khoanh vùng Schema (Masking):** Cho phép chỉ định các bảng/cột được phép đưa vào Metadata cho AI học, ẩn đi các bảng nhạy cảm (Ví dụ: Mật khẩu người dùng).
- **F3. Thiết lập Rào cản:** Cấu hình giới hạn thời gian chạy lệnh (Timeout) và số dòng trả về mặc định (Max Rows Limit).

### 4.2 Khối Chức năng Người dùng (End-User)
- **F4. Khung Truy vấn (NL2SQL):** Giao diện Chat để nhập câu hỏi bằng văn bản tiếng Việt/Anh.
- **F5. Không gian Kết quả:** 
  - Hiển thị kết quả truy vấn dưới dạng Bảng (Table).
  - Cung cấp Box hiển thị code SQL thô và giải thích chi tiết bằng tiếng Việt.
- **F6. Trực quan hóa Dữ liệu:** Chuyển đổi một click từ dữ liệu Bảng sang Biểu đồ (Line, Bar, Pie chart).
- **F7. Lịch sử Truy vấn:** Lưu trữ lịch sử các câu hỏi đã hỏi để tái sử dụng và cung cấp đường dẫn chia sẻ nội bộ.

---

## 5. Yêu cầu Phi chức năng & Kỹ thuật (Non-Functional Requirements)

### 5.1 Kiến trúc & Tech Stack
- **Frontend:** React / Next.js. Giao diện ưu tiên phong cách Glassmorphism (Vibrant colors, blur effects).
- **Backend:** FastAPI (Python) phục vụ API Gateway và NL2SQL service.
- **Database:** Supabase (Ưu tiên dùng Pooler Host / Session Mode để hỗ trợ IPv4).
- **AI / LLM:** Tích hợp đa mô hình qua OpenRouter / Gemini API.

### 5.2 Yêu cầu An toàn Dữ liệu (Security & Safety)
- **S1. Cơ chế Read-only Proxy:** Bắt buộc áp dụng bộ lọc từ chối (Drop Filter) ở tầng Backend. Bất kỳ câu truy vấn nào chứa từ khóa `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER` đều bị báo lỗi *Unauthorized* ngay lập tức, không được phép chạm tới Database gốc.
- **S2. Hard Limit (Ép tài nguyên):** Backend phải tự động ép thêm mệnh đề `LIMIT` (VD: `LIMIT 500`) vào cuối mọi câu lệnh SQL để chống tràn RAM máy chủ.
- **S3. Non-root Execution:** Mọi service Docker phải được cấu hình chạy dưới quyền user tạo riêng (`appuser`), cấm chạy dưới quyền root.

### 5.3 Yêu cầu Chất lượng (QA Standard)
- Không có đoạn code nào được phép đưa lên Production nếu chưa vượt qua Báo cáo (Test Report) của **QA Expert Agent** (Bao gồm Pass 100% API Integration và không dính lỗi CRITICAL từ Trivy Scan của DevSecOps Agent).
