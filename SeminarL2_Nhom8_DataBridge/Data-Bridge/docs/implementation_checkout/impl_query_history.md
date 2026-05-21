# Implementation Plan: Lịch sử & Chia sẻ Truy vấn

## 1. Overview (Tổng quan)
Module Lịch sử & Chia sẻ Truy vấn giúp người dùng quản lý, xem lại và tái sử dụng các câu hỏi cũng như câu lệnh SQL đã thực hiện thành công. Mục tiêu chuyển đổi từ lưu trữ dạng file (.json) sang database (Supabase) để đảm bảo tính ổn định và khả năng mở rộng cho môi trường Production.

---

## 2. Các bước triển khai chi tiết

### Bước 1: Frontend - Giao diện Lịch sử truy vấn
**Mục tiêu:** Hiển thị danh sách các câu hỏi, mã SQL và kết quả tương ứng một cách trực quan.
- **Tác vụ 1:** Xây dựng một Sidebar hoặc Trang riêng để liệt kê lịch sử.
- **Tác vụ 2:** Hiển thị chi tiết từng bản ghi gồm: Câu hỏi tự nhiên, SQL đã sinh và bảng kết quả thu gọn.

> **Prompt gửi AI Agent:**
> ```text
> "Hãy xây dựng một Panel 'Lịch sử truy vấn' ở Frontend. Sử dụng dữ liệu từ API GET /history để hiển thị danh sách các câu hỏi cũ. Mỗi mục trong danh sách cần hiển thị: Câu hỏi, Thời gian thực hiện, và nút xem nhanh mã SQL. Đầu ra: Giao diện lịch sử truy vấn hoàn chỉnh."
> ```

### Bước 2: Tái chạy truy vấn & Chia sẻ kết quả
**Mục tiêu:** Giúp người dùng thực thi lại nhanh chóng các yêu cầu cũ và chia sẻ dữ liệu.
- **Tác vụ 1:** Thêm nút 'Re-run' cho mỗi bản ghi lịch sử để nạp lại SQL vào Editor và chạy ngay.
- **Tác vụ 2:** Tích hợp tính năng Copy mã SQL hoặc kết quả bảng vào Clipboard.

> **Prompt gửi AI Agent:**
> ```text
> "Thực hiện logic khi người dùng nhấn vào một bản ghi trong lịch sử: Hệ thống sẽ tự động điền mã SQL tương ứng vào Monaco Editor và kích hoạt quá trình thực thi. Đồng thời, thêm nút 'Copy SQL' để người dùng dễ dàng chia sẻ mã. Mục tiêu: Tối ưu hóa trải nghiệm tái sử dụng truy vấn."
> ```

### Bước 3: Di chuyển dữ liệu sang Supabase (Production Migration)
**Mục tiêu:** Chuyển đổi từ file-based storage sang database storage chuyên nghiệp.
- **Tác vụ 1:** Thiết kế bảng `query_history` trên Supabase với các trường: id, user_id, question, sql, result_preview, created_at.
- **Tác vụ 2:** Viết script migrate dữ liệu từ file `query_history.json` vào Supabase và cập nhật backend sử dụng Supabase SDK thay vì thao tác với file.

> **Prompt gửi AI Agent:**
> ```text
> "Sử dụng skill supabase, hãy tạo bảng 'query_history' với đầy đủ các trường cần thiết. Viết một script Python để đọc dữ liệu từ file query_history.json hiện tại và insert toàn bộ vào bảng mới trên Supabase. Sau đó, cập nhật Query Service để thực hiện lưu/lấy dữ liệu từ database. Đầu ra: Hệ thống lưu trữ lịch sử chính thức chuyển sang Supabase."
> ```

---

# Progress Report: Lịch sử & Chia sẻ Truy vấn
**Ngày cập nhật:** 16/05/2026
**Trạng thái tổng thể:** Đang triển khai (Giai đoạn chuyển đổi)

## 📈 Tiến trình tổng quan (Progress Overview)
- **Tổng số tác vụ:** 4
- **Đã hoàn thành:** 1
- **Tiến độ (Completion):** 25%

---

## 📊 Chỉ số đánh giá (Evaluation Criteria)
| Chỉ số | Mục tiêu | Kết quả hiện tại | Đạt yêu cầu? |
| :--- | :--- | :--- | :--- |
| **Migration Success** | 100% data | Đang chờ | ⏳ |
| **UI Responsiveness** | < 200ms | N/A | ⏳ |
| **Re-run Success Rate**| 100% | Đang test | ⏳ |

---

## ✅ Các hạng mục đã hoàn thành (Done)
- [x] **Backend API**: Đã có endpoint `GET /history` đọc từ file JSON.

## 🚧 Đang triển khai (In Progress)
- [ ] **Frontend UI**: Đang xây dựng mockup cho Panel lịch sử.
- [ ] **Supabase Migration**: Đang chuẩn bị SQL schema cho bảng history.

## 🛑 Khó khăn & Khuyến nghị (Blockers & Recommendations)
- **Data Consistency**: Cần đảm bảo dữ liệu khi migrate từ JSON không bị lỗi format ngày tháng.

## 📅 Kế hoạch tiếp theo (Next Steps)
1. Hoàn thiện giao diện Sidebar hiển thị lịch sử ở Frontend.
2. Thực hiện migration dữ liệu sang Supabase vào tuần tới.
3. Tích hợp tính năng Copy/Share kết quả trực tiếp từ bảng dữ liệu.
