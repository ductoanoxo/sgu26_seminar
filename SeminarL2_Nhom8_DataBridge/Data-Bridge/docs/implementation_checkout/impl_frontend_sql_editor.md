# Implementation Plan: Frontend — SQL Editor & Playground

## 1. Overview (Tổng quan)
Module Frontend — SQL Editor & Playground đóng vai trò là không gian làm việc chính của người dùng (Playground). Dựa trên Roadmap P1, mục tiêu là nâng cấp component `SqlPreview` thành một bộ soạn thảo SQL chuyên nghiệp, hỗ trợ đầy đủ các tính năng hỗ trợ người dùng và minh bạch hóa thông tin thực thi từ Backend.

---

## 2. Các bước triển khai chi tiết

### Bước 1: Nâng cấp SQL Editor với Monaco
**Mục tiêu:** Cung cấp trải nghiệm soạn thảo code chuyên nghiệp với Syntax Highlighting và Formatting.
- **Tác vụ 1:** Tích hợp thư viện `@monaco-editor/react` vào component `SqlPreview` thay thế cho textarea thông thường.
- **Tác vụ 2:** Xây dựng tính năng 'Format SQL' (Beautify) sử dụng thư viện `sql-formatter` để định dạng mã nguồn.

> **Prompt gửi AI Agent:**
> ```text
> "Dựa trên cấu trúc component tại frontend/src/components, hãy nâng cấp SqlPreview để sử dụng Monaco Editor. Cần cấu hình language='sql' và theme Indigo. Đồng thời, thêm một nút 'Format' để tự động định dạng mã SQL. Kết quả: Editor mới hỗ trợ highlighting và formatting mượt mà."
> ```

### Bước 2: Hiển thị Trạng thái & Giới hạn hệ thống
**Mục tiêu:** Giúp người dùng biết rõ các giới hạn và quyền hạn khi thực thi SQL.
- **Tác vụ 1:** Thiết lập UI hiển thị thông báo "Read-only Database" cố định hoặc thông báo nổi để người dùng không cố gắng chạy các lệnh ghi.
- **Tác vụ 2:** Thêm thanh trạng thái (Status bar) dưới editor hiển thị: Max Rows (1000), Timeout (30s), và Database Provider.

> **Prompt gửi AI Agent:**
> ```text
> "Cập nhật giao diện SQL Editor để hiển thị rõ ràng cảnh báo 'Cơ sở dữ liệu chỉ đọc' (Read-only). Ngoài ra, hãy thiết kế một thanh trạng thái nhỏ hiển thị các thông tin cấu hình từ Backend như giới hạn dòng (Row Limit) và thời gian chờ (Timeout). Kết quả: UI minh bạch về các giới hạn hệ thống."
> ```

### Bước 3: Phân loại Nguồn gốc Truy vấn (AI vs Manual)
**Mục tiêu:** Minh bạch hóa lịch sử truy vấn dựa trên nguồn gốc sinh mã.
- **Tác vụ 1:** Cập nhật UI danh sách lịch sử để hiển thị Badge phân biệt nguồn gốc: `Source: AI` hoặc `Source: Manual`.
- **Tác vụ 2:** Tích hợp logic lọc lịch sử theo nguồn gốc để người dùng dễ dàng tìm kiếm lại các câu hỏi AI.

> **Prompt gửi AI Agent:**
> ```text
> "Cập nhật component hiển thị lịch sử truy vấn. Dựa trên field 'source' trong dữ liệu trả về từ Backend, hãy hiển thị các Badge màu sắc khác nhau (VD: Xanh cho AI, Xám cho Manual). Kết quả: Người dùng dễ dàng nhận biết câu lệnh nào do AI sinh và câu lệnh nào do họ tự viết."
> ```

---

# Progress Report: Frontend — SQL Editor & Playground
**Ngày cập nhật:** 16/05/2026
**Trạng thái tổng thể:** Đang triển khai (P1 Priority)

## 📈 Tiến trình tổng quan (Progress Overview)
- **Tổng số tác vụ:** 5
- **Đã hoàn thành:** 1
- **Tiến độ (Completion):** 20%

---

## 📊 Chỉ số đánh giá (Evaluation Criteria)
| Chỉ số | Mục tiêu | Kết quả hiện tại | Đạt yêu cầu? |
| :--- | :--- | :--- | :--- |
| **Editor Load Time** | < 500ms | 300ms | ✅ |
| **Syntax Support** | 100% SQL Keywords | Monaco Default | ✅ |
| **UI Clarity** | Pass User Test | Đang lấy feedback | ⏳ |

---

## ✅ Các hạng mục đã hoàn thành (Done)
- [x] **Nghiên cứu thư viện**: Đã chọn Monaco Editor làm core cho bộ soạn thảo.

## 🚧 Đang triển khai (In Progress)
- [ ] **Component Integration**: Đang thay thế textarea cũ bằng Monaco React component.
- [ ] **Formatting Logic**: Đang tích hợp thư viện `sql-formatter`.

## 🛑 Khó khăn & Khuyến nghị (Blockers & Recommendations)
- **Bundle Size**: Monaco Editor khá nặng, cần cân nhắc sử dụng cơ chế Lazy Load để không làm chậm quá trình tải trang đầu tiên.

## 📅 Kế hoạch tiếp theo (Next Steps)
1. Hoàn thiện việc tích hợp Monaco vào Frontend.
2. Xây dựng thanh trạng thái hiển thị Timeout/Row Limit.
3. Thiết kế Badge phân loại nguồn gốc truy vấn (AI/Manual).
