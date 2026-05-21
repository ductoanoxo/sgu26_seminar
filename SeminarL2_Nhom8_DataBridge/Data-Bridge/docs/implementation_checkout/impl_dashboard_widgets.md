# Implementation Plan: Dashboard & Widget Nâng cao

## 1. Overview (Tổng quan)
Module Dashboard & Widget Nâng cao tập trung vào việc nâng cấp khả năng tương tác và cá nhân hóa giao diện phân tích cho người dùng. Mục tiêu là biến Dashboard từ một bảng hiển thị tĩnh thành một không gian làm việc động, nơi người dùng có thể tự do sắp xếp, biên tập và lọc dữ liệu theo thời gian thực mà không cần viết lại mã SQL.

---

## 2. Các bước triển khai chi tiết

### Bước 1: Drag & Drop Widget & Auto-refresh
**Mục tiêu:** Cho phép người dùng tùy biến bố cục Dashboard và tự động cập nhật dữ liệu.
- **Tác vụ 1:** Tích hợp thư viện `dnd-kit` vào `DashboardPanel` để hỗ trợ kéo thả các thẻ Widget.
- **Tác vụ 2:** Triển khai cơ chế `setInterval` (với interval tùy chỉnh) cho từng Widget để gọi API refresh định kỳ.

> **Prompt gửi AI Agent:**
> ```text
> "Hãy tích hợp thư viện dnd-kit vào DashboardPanel để người dùng có thể thay đổi thứ tự các Widget bằng thao tác kéo thả. Ngoài ra, hãy thêm tính năng 'Auto-refresh' vào mỗi Widget với tùy chọn interval (ví dụ: 5 phút, 1 giờ). Đầu ra: Dashboard có khả năng kéo thả và tự động cập nhật."
> ```

### Bước 2: Widget Editor UI & Dynamic Filters
**Mục tiêu:** Cung cấp công cụ để người dùng chỉnh sửa biểu đồ và lọc dữ liệu nhanh.
- **Tác vụ 1:** Xây dựng Modal 'Widget Editor' cho phép chọn trường dữ liệu và thay đổi Chart Type (Bar, Line, Pie).
- **Tác vụ 2:** Phát triển 'Global Filter' ở phía trên Dashboard để lọc nhanh theo Dimension hoặc Time range cho toàn bộ các Widget.

> **Prompt gửi AI Agent:**
> ```text
> "Xây dựng giao diện Widget Editor. Khi người dùng nhấn 'Edit' trên một thẻ Widget, hiện modal cho phép đổi Chart Type và cấu hình lại các trục X-Y. Đồng thời, thiết kế bộ lọc động (Filter) phía trên Dashboard để áp dụng filter nhanh cho các câu lệnh SQL của widget mà không cần LLM can thiệp lại. Đầu ra: Bộ công cụ biên tập và lọc dữ liệu hoàn chỉnh."
> ```

### Bước 3: Backend Optimization & Export
**Mục tiêu:** Tăng tốc độ phản hồi và hỗ trợ xuất bản báo cáo.
- **Tác vụ 1:** Triển khai cơ chế Caching kết quả tại Backend dựa trên `query_fingerprint` để tránh thực thi lại các truy vấn giống hệt nhau.
- **Tác vụ 2:** Tích hợp tính năng Export dữ liệu từ Widget ra tệp tin CSV hoặc Excel.

> **Prompt gửi AI Agent:**
> ```text
> "Thực hiện cài đặt lớp Caching tại Backend. Sử dụng mã băm (fingerprint) của SQL để lưu kết quả vào Redis. Nếu query giống nhau được gọi lại trong thời gian ngắn, trả về kết quả từ cache ngay. Ngoài ra, hãy viết logic cho nút 'Export' trên Widget để người dùng tải dữ liệu về máy. Đầu ra: Dashboard hoạt động nhanh hơn và hỗ trợ trích xuất dữ liệu."
> ```

---

# Progress Report: Dashboard & Widget Nâng cao
**Ngày cập nhật:** 16/05/2026
**Trạng thái tổng thể:** Đang triển khai (Nâng cấp)

## 📈 Tiến trình tổng quan (Progress Overview)
- **Tổng số tác vụ:** 6
- **Đã hoàn thành:** 1
- **Tiến độ (Completion):** 16%

---

## 📊 Chỉ số đánh giá (Evaluation Criteria)
| Chỉ số | Mục tiêu | Kết quả hiện tại | Đạt yêu cầu? |
| :--- | :--- | :--- | :--- |
| **Widget Load Time** | < 1.0s (cached) | 2.5s (average) | ❌ |
| **DND Smoothness** | 60 FPS | Đang tích hợp | ⏳ |
| **Export Accuracy** | 100% data | N/A | ⏳ |

---

## ✅ Các hạng mục đã hoàn thành (Done)
- [x] **Backend CRUD**: Đã hoàn thiện các API Create, List, Get, Update, Refresh cho Widget.

## 🚧 Đang triển khai (In Progress)
- [ ] **Drag & Drop**: Đang tích hợp dnd-kit vào layout chính.
- [ ] **Widget Editor**: Đang thiết kế giao diện modal biên tập biểu đồ.

## 🛑 Khó khăn & Khuyến nghị (Blockers & Recommendations)
- **Chart Re-rendering**: Cần tối ưu việc re-render các biểu đồ khi thay đổi kích thước hoặc vị trí widget để tránh lag UI.

## 📅 Kế hoạch tiếp theo (Next Steps)
1. Hoàn thiện tính năng kéo thả trong tuần này.
2. Xây dựng bộ lọc động (Global Filter) để người dùng thao tác dữ liệu linh hoạt.
3. Triển khai Caching Backend để giảm tải cho Database.
