# Implementation Plan: Kết nối Dữ liệu Động (Connect Modal / Data Import)

## 1. Overview (Tổng quan)
Module Kết nối Dữ liệu Động là cửa ngõ đầu vào của hệ thống Agent_SQL, cho phép người dùng kết nối với các nguồn dữ liệu bên ngoài (Postgres, MySQL, v.v.) hoặc tải lên các tệp tin (CSV, JSON). Trọng tâm của module này là đảm bảo việc trích xuất schema tự động, bảo mật thông tin kết nối và cung cấp quyền kiểm soát (Masking/Limit) cho Admin.

---

## 2. Các bước triển khai chi tiết

### Bước 1: Verify & Hoàn thiện luồng Connection String
**Mục tiêu:** Đảm bảo Backend có thể kết nối thành công và trích xuất Metadata từ thông tin người dùng nhập.
- **Tác vụ 1:** Kiểm tra tính hợp lệ của Connection String tại Frontend.
- **Tác vụ 2:** Backend thực hiện "Dry Run" kết nối, đọc cấu trúc bảng (Schema) và cập nhật Metadata cho LLM Context.

> **Prompt gửi AI Agent:**
> ```text
> "Hãy kiểm tra và hoàn thiện service kết nối dữ liệu. Khi nhận Connection String từ Frontend, Backend cần sử dụng SQLAlchemy để liệt kê các bảng và cột (Schema Extraction). Thông tin này phải được lưu vào Metadata store để AI có thể hiểu cấu trúc DB. Đầu ra: Luồng kết nối DB hoạt động end-to-end."
> ```

### Bước 2: Xử lý Upload CSV/JSON & Bảng tạm (Virtual Tables)
**Mục tiêu:** Cho phép người dùng phân tích dữ liệu từ tệp tin mà không cần database sẵn có.
- **Tác vụ 1:** Hoàn thiện component upload trong `DataImport.tsx`.
- **Tác vụ 2:** Backend parse tệp tin và tạo bảng tạm thời (ví dụ dùng DuckDB hoặc SQLite in-memory) để thực thi SQL.

> **Prompt gửi AI Agent:**
> ```text
> "Xây dựng logic xử lý upload tệp tin CSV/JSON. Backend nhận file, sử dụng thư viện Pandas để parse và tạo một bảng ảo (Virtual Table) trong bộ nhớ. Sau đó, cập nhật danh sách bảng hiển thị ở SQL Editor để người dùng có thể truy vấn ngay. Đầu ra: Chức năng phân tích file hoạt động."
> ```

### Bước 3: Bảo mật & Kiểm soát (Security & Control)
**Mục tiêu:** Mã hóa thông tin nhạy cảm và giới hạn phạm vi truy cập dữ liệu.
- **Tác vụ 1:** Triển khai mã hóa đối xứng (Symmetric Encryption) cho Connection Strings lưu trong database.
- **Tác vụ 2:** Xây dựng giao diện 'Schema Masking' để Admin chọn các bảng/cột được phép cho AI truy cập.
- **Tác vụ 3:** Tích hợp tham số Timeout và Max Rows vào câu lệnh thực thi SQL.

> **Prompt gửi AI Agent:**
> ```text
> "Thực hiện mã hóa Password trong Connection String bằng thư viện Cryptography trước khi lưu vào DB. Xây dựng logic Schema Masking: Chỉ gửi Metadata của các bảng mà Admin đã đánh dấu 'Allowed' cho LLM. Ngoài ra, hãy áp dụng LIMIT 1000 và TIMEOUT 30s cho mọi truy vấn. Đầu ra: Hệ thống kết nối dữ liệu an toàn và có kiểm soát."
> ```

---

# Progress Report: Kết nối Dữ liệu Động
**Ngày cập nhật:** 16/05/2026
**Trạng thái tổng thể:** Đang triển khai (Verify)

## 📈 Tiến trình tổng quan (Progress Overview)
- **Tổng số tác vụ:** 5
- **Đã hoàn thành:** 1
- **Tiến độ (Completion):** 20%

---

## 📊 Chỉ số đánh giá (Evaluation Criteria)
| Chỉ số | Mục tiêu | Kết quả hiện tại | Đạt yêu cầu? |
| :--- | :--- | :--- | :--- |
| **Connection Success** | 100% | 70% (Đang fix) | ❌ |
| **Parsing Success** | 100% (Standard) | 90% | ✅ |
| **Encryption Status** | 100% encrypted | 0% | ❌ |

---

## ✅ Các hạng mục đã hoàn thành (Done)
- [x] **Frontend UI**: Đã có component `DataImport.tsx` cơ bản.

## 🚧 Đang triển khai (In Progress)
- [ ] **Schema Extraction**: Đang verify luồng đọc metadata từ Postgres.
- [ ] **Security Layer**: Đang thiết kế module mã hóa thông tin kết nối.

## 🛑 Khó khăn & Khuyến nghị (Blockers & Recommendations)
- **Database Variations**: Cần xử lý các kiểu dữ liệu đặc thù của từng hệ quản trị DB khác nhau khi trích xuất schema.

## 📅 Kế hoạch tiếp theo (Next Steps)
1. Hoàn thiện việc mã hóa thông tin kết nối ở Backend.
2. Xây dựng UI cho Schema Masking (F2) và Timeout Config (F3).
3. Test end-to-end luồng upload CSV lớn (> 50MB).
