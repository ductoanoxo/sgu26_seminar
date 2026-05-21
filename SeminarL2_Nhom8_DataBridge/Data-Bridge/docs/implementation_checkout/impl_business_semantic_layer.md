# Implementation Plan: Tầng ngữ nghĩa (Business Semantic Layer)

## 1. Overview (Tổng quan)
Module Tầng ngữ nghĩa (Business Semantic Layer) đóng vai trò là "cầu nối" giúp AI hiểu được các khái niệm kinh doanh thay vì chỉ làm việc trên các bảng và cột kỹ thuật thô. Mục tiêu là giúp AI trả lời chính xác các câu hỏi nghiệp vụ phức tạp thông qua việc tra cứu Business Logic và học từ các ví dụ mẫu (Few-shot).

---

## 2. Các bước triển khai chi tiết

### Bước 1: Giao diện Từ điển thuật ngữ (Glossary) cho Admin
**Mục tiêu:** Cung cấp nơi để Admin định nghĩa các thuật ngữ, tên cột thân thiện và mô tả nghiệp vụ.
- **Tác vụ 1:** Thiết kế UI Dashboard để quản lý danh sách thuật ngữ (CRUD).
- **Tác vụ 2:** Lưu trữ thông tin glossary vào database và đồng bộ hóa với metadata của AI.

> **Prompt gửi AI Agent:**
> ```text
> "Hãy xây dựng một trang quản trị (Admin UI) trong Dashboard để quản lý 'Business Glossary'. Trang này cho phép Admin thêm các mục như: 'Tên thuật ngữ', 'Mô tả nghiệp vụ', 'Mapping với cột kỹ thuật'. Đầu ra: Giao diện quản lý Glossary hoàn chỉnh tích hợp vào Dashboard."
> ```

### Bước 2: Lưu trữ Business Logic vào Vector DB
**Mục tiêu:** Sử dụng RAG (Retrieval-Augmented Generation) để AI tra cứu các công thức tính toán phức tạp trước khi sinh SQL.
- **Tác vụ 1:** Triển khai pgvector trên database hiện tại (Supabase/Postgres).
- **Tác vụ 2:** Viết script chuyển đổi Business Logic (VD: Lợi nhuận = Doanh thu - Chi phí) thành embedding và lưu vào Vector DB.

> **Prompt gửi AI Agent:**
> ```text
> "Sử dụng pgvector trên Supabase, hãy tạo bảng 'business_rules_vector' để lưu trữ các quy tắc nghiệp vụ. Viết một service nhỏ để khi user hỏi, hệ thống sẽ thực hiện vector search để tìm các logic liên quan và đưa vào prompt của LLM. Mục tiêu: AI hiểu được các công thức tính toán mà không cần hard-code."
> ```

### Bước 3: Cấu hình Few-shot Samples (Câu hỏi mẫu)
**Mục tiêu:** Cung cấp các cặp "Câu hỏi - SQL" mẫu để AI học hỏi cách xử lý các yêu cầu đặc thù hoặc khó.
- **Tác vụ 1:** Xây dựng hệ thống quản lý các Few-shot samples.
- **Tác vụ 2:** Tích hợp logic Dynamic Few-shot Selection (chọn ví dụ gần nhất với câu hỏi của user) vào pipeline NL2SQL.

> **Prompt gửi AI Agent:**
> ```text
> "Xây dựng chức năng 'Few-shot Management'. Khi sinh SQL, hãy lấy ra 3 ví dụ có độ tương đồng cao nhất với câu hỏi của người dùng (sử dụng vector search) và đưa vào prompt làm ngữ cảnh. Mục tiêu: Tăng độ chính xác của SQL sinh ra cho các trường hợp phức tạp."
> ```

---

# Progress Report: Tầng ngữ nghĩa
**Ngày cập nhật:** 16/05/2026
**Trạng thái tổng thể:** Đang triển khai (Nghiên cứu)

## 📈 Tiến trình tổng quan (Progress Overview)
- **Tổng số tác vụ:** 3
- **Đã hoàn thành:** 0
- **Tiến độ (Completion):** 10%

---

## 📊 Chỉ số đánh giá (Evaluation Criteria)
| Chỉ số | Mục tiêu | Kết quả hiện tại | Đạt yêu cầu? |
| :--- | :--- | :--- | :--- |
| **Glossary Coverage** | 100% Core tables | 0% | ❌ |
| **Logic Retrieval Accuracy**| > 85% | Chưa đo lường | ⏳ |
| **Few-shot Improvement** | + 20% Accuracy | Đang test | ⏳ |

---

## ✅ Các hạng mục đã hoàn thành (Done)
- [x] **Xác định kiến trúc**: Đã chọn pgvector làm công cụ lưu trữ ngữ nghĩa.

## 🚧 Đang triển khai (In Progress)
- [ ] **Prototype Vector Search**: Đang thử nghiệm việc nhúng (embedding) các công thức đơn giản.
- [ ] **UI Glossary**: Đang thiết kế mockup cho trang quản trị.

## 🛑 Khó khăn & Khuyến nghị (Blockers & Recommendations)
- **Embedding Quality**: Cần lựa chọn model embedding phù hợp để hiểu tốt các thuật ngữ chuyên ngành tiếng Việt.

## 📅 Kế hoạch tiếp theo (Next Steps)
1. Hoàn thiện schema database cho Glossary và Few-shot.
2. Triển khai API CRUD cho Admin quản lý dữ liệu ngữ nghĩa.
3. Tích hợp bước tra cứu Vector vào NL2SQL Service.
