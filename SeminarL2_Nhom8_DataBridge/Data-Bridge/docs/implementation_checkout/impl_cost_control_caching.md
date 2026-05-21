# Implementation Plan: Kiểm soát Chi phí & Caching (Cost Control)

## 1. Overview (Tổng quan)
Module Kiểm soát Chi phí & Caching tập trung vào việc tối ưu hóa hiệu năng và tiết kiệm chi phí vận hành bằng cách giảm thiểu số lượng request gửi tới LLM. Đồng thời, module này thiết lập các rào cản kỹ thuật để bảo vệ tài nguyên hệ thống (DB/API) khỏi việc bị lạm dụng hoặc spam.

---

## 2. Các bước triển khai chi tiết

### Bước 1: Triển khai Semantic Caching với Redis
**Mục tiêu:** Lưu trữ các câu hỏi đã trả lời. Nếu có câu hỏi tương đồng về ngữ nghĩa, trả về kết quả ngay lập tức.
- **Tác vụ 1:** Cấu hình Redis trong môi trường Docker.
- **Tác vụ 2:** Tích hợp logic Vector Search (semantic similarity) vào cache layer. Nếu độ tương đồng > 95%, sử dụng kết quả cũ.

> **Prompt gửi AI Agent:**
> ```text
> "Hãy thiết kế một lớp Caching cho NL2SQL Service. Sử dụng Redis để lưu trữ cặp 'Question Embedding' và 'SQL Result'. Khi có câu hỏi mới, thực hiện tìm kiếm độ tương đồng. Nếu tìm thấy câu hỏi tương tự (>0.95 similarity), hãy trả về kết quả ngay mà không gọi LLM API. Đầu ra: Cache Layer hoạt động ổn định."
> ```

### Bước 2: Rate Limiting & Query Timeout
**Mục tiêu:** Giới hạn tần suất đặt câu hỏi của người dùng và bảo vệ Database khỏi các câu lệnh SQL quá nặng.
- **Tác vụ 1:** Triển khai middleware Rate Limit (ví dụ: 50 câu/ngày/user) sử dụng IP hoặc User ID.
- **Tác vụ 2:** Cấu hình Query Timeout cho database driver (ngắt sau 30 giây).

> **Prompt gửi AI Agent:**
> ```text
> "Thực hiện viết một Middleware cho Gateway API để giới hạn số lượng câu hỏi của mỗi người dùng (Rate Limiting). Ngoài ra, hãy cấu hình Query Service để tự động ngắt (TIMEOUT) các truy vấn SQL chạy quá 30 giây. Mục tiêu: Ngăn chặn spam và treo database."
> ```

### Bước 3: Token Tracking & Cost Analytics
**Mục tiêu:** Ghi lại số lượng token sử dụng cho mỗi request để tính toán chi phí theo User/Department.
- **Tác vụ 1:** Trích xuất thông tin `usage` (prompt_tokens, completion_tokens) từ response của LLM.
- **Tác vụ 2:** Lưu thông tin token vào bảng `audit_logs` trên Supabase để Admin có thể xem báo cáo chi phí.

> **Prompt gửi AI Agent:**
> ```text
> "Cập nhật logic gọi LLM API để trích xuất số lượng token tiêu thụ. Lưu các thông số này kèm theo user_id vào bảng logs trong database. Xây dựng một view thống kê đơn giản để xem tổng chi phí theo phòng ban. Mục tiêu: Kiểm soát ngân sách sử dụng AI."
> ```

---

# Progress Report: Kiểm soát Chi phí & Caching
**Ngày cập nhật:** 16/05/2026
**Trạng thái tổng thể:** Đang triển khai (Giai đoạn thiết lập)

## 📈 Tiến trình tổng quan (Progress Overview)
- **Tổng số tác vụ:** 4
- **Đã hoàn thành:** 0
- **Tiến độ (Completion):** 5%

---

## 📊 Chỉ số đánh giá (Evaluation Criteria)
| Chỉ số | Mục tiêu | Kết quả hiện tại | Đạt yêu cầu? |
| :--- | :--- | :--- | :--- |
| **Cache Hit Rate** | > 30% | 0% | ❌ |
| **Average Latency** | < 1.0s (cached) | N/A | ⏳ |
| **Token Savings** | > 20% cost | 0% | ❌ |

---

## ✅ Các hạng mục đã hoàn thành (Done)
- [x] **Xác định công nghệ**: Quyết định sử dụng Redis cho Caching và Middleware cho Rate Limiting.

## 🚧 Đang triển khai (In Progress)
- [ ] **Redis Setup**: Đang viết cấu hình Docker Compose cho Redis service.
- [ ] **Timeout Logic**: Đang kiểm tra cấu hình timeout của SQLalchemy/Postgres driver.

## 🛑 Khó khăn & Khuyến nghị (Blockers & Recommendations)
- **Semantic Mapping**: Cần đảm bảo các câu hỏi mang tính thời điểm (vd: 'Doanh thu hôm nay') không bị cached sai cho ngày mai.

## 📅 Kế hoạch tiếp theo (Next Steps)
1. Hoàn thành việc tích hợp Redis vào hệ thống.
2. Viết logic tính toán độ tương đồng câu hỏi (Embedding Search).
3. Triển khai bảng thống kê Token Usage trên Supabase Dashboard.
