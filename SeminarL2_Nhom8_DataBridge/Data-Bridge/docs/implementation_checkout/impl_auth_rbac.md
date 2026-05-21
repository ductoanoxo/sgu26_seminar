# Implementation Plan: Quản lý Người dùng & Phân quyền (Auth & RBAC)

## 1. Overview (Tổng quan)
Module Quản lý Người dùng & Phân quyền nhằm thiết lập hệ thống định danh và kiểm soát truy cập an toàn cho Agent_SQL. Việc tích hợp Supabase Auth kết hợp với Row Level Security (RLS) đảm bảo dữ liệu của người dùng được bảo vệ tuyệt đối, đồng thời phân định rõ quyền hạn giữa người dùng thông thường và quản trị viên (Admin).

---

## 2. Các bước triển khai chi tiết

### Bước 1: Tích hợp Supabase Auth
**Mục tiêu:** Cho phép người dùng đăng ký và đăng nhập hệ thống một cách an toàn.
- **Tác vụ 1:** Thiết lập phương thức đăng nhập Email/Password và Google OAuth trên Supabase Dashboard.
- **Tác vụ 2:** Xây dựng giao diện Login/Register và tích hợp Supabase Client vào Frontend.

> **Prompt gửi AI Agent:**
> ```text
> "Sử dụng skill supabase, hãy thực hiện tích hợp Supabase Auth vào dự án. Cần hỗ trợ đăng nhập qua Email và Google OAuth. Sau khi đăng nhập, thông tin session phải được lưu trữ để sử dụng cho các request API tiếp theo. Đầu ra: Trang Login hoạt động và xác thực được người dùng."
> ```

### Bước 2: Thiết lập Row Level Security (RLS) & Audit Trail
**Mục tiêu:** Bảo vệ dữ liệu lịch sử truy vấn và ghi lại nhật ký hoạt động.
- **Tác vụ 1:** Kích hoạt RLS trên bảng `query_history` và tạo policy `auth.uid() = user_id`.
- **Tác vụ 2:** Xây dựng bảng `audit_logs` để lưu vết mọi câu lệnh SQL được thực thi (ai chạy, lúc nào, kết quả).

> **Prompt gửi AI Agent:**
> ```text
> "Sử dụng skill supabase, hãy viết mã SQL Migration để kích hoạt RLS trên bảng 'query_history' sao cho người dùng chỉ có quyền xem dữ liệu của chính mình. Đồng thời, tạo bảng 'audit_logs' để ghi nhận lịch sử thực thi SQL từ backend. Đầu ra: Database schema an toàn và có khả năng giám sát."
> ```

### Bước 3: Phân quyền Admin & Cấu hình bảo mật
**Mục tiêu:** Giới hạn các tính năng cấu hình hệ thống nhạy cảm chỉ dành cho Admin.
- **Tác vụ 1:** Thiết lập Role 'admin' trong bảng profiles hoặc metadata của Supabase Auth.
- **Tác vụ 2:** Kiểm tra quyền Admin tại Gateway API trước khi cho phép truy cập các endpoint Connection String và Schema Masking.

> **Prompt gửi AI Agent:**
> ```text
> "Xây dựng logic kiểm tra quyền Admin tại Gateway API. Chỉ những người dùng có metadata role='admin' mới được phép gọi các API cấu hình database (Connection String, Schema Masking). Các user thường sẽ nhận lỗi 403 Forbidden. Mục tiêu: Bảo vệ các cấu hình nhạy cảm của hệ thống."
> ```

---

# Progress Report: Quản lý Người dùng & Phân quyền
**Ngày cập nhật:** 16/05/2026
**Trạng thái tổng thể:** Đang triển khai

## 📈 Tiến trình tổng quan (Progress Overview)
- **Tổng số tác vụ:** 4
- **Đã hoàn thành:** 0
- **Tiến độ (Completion):** 0%

---

## 📊 Chỉ số đánh giá (Evaluation Criteria)
| Chỉ số | Mục tiêu | Kết quả hiện tại | Đạt yêu cầu? |
| :--- | :--- | :--- | :--- |
| **Auth Success Rate** | 100% | N/A | ⏳ |
| **RLS Leak Check** | 0 leaks | Chưa kiểm tra | ⏳ |
| **Audit Coverage** | 100% SQL queries | 0% | ❌ |

---

## ✅ Các hạng mục đã hoàn thành (Done)
- (Chưa có hạng mục nào hoàn thành)

## 🚧 Đang triển khai (In Progress)
- [ ] **Auth Integration**: Đang nghiên cứu cấu hình Google OAuth.
- [ ] **RLS Policy Design**: Đang phác thảo các quy tắc bảo mật cho bảng history.

## 🛑 Khó khăn & Khuyến nghị (Blockers & Recommendations)
- **JWT Management**: Cần đảm bảo token được truyền và kiểm tra đồng nhất giữa các microservices.

## 📅 Kế hoạch tiếp theo (Next Steps)
1. Hoàn thành cấu hình Supabase Auth Project.
2. Viết SQL migration cho RLS và Audit logs.
3. Cập nhật Frontend Dashboard để hiển thị thông tin User/Admin.
