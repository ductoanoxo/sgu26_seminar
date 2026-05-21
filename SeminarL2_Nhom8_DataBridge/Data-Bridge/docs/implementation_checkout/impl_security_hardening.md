# Implementation Plan: Security Hardening & Non-root Docker

## 1. Overview (Tổng quan)
Module Security Hardening & Non-root Docker là thành phần tối quan trọng đảm bảo an toàn cho toàn bộ hệ thống Agent_SQL. Dựa trên PRD (S1, S2, S3), module này giải quyết các rủi ro về tấn công SQL Injection, leo thang đặc quyền trong container và rò rỉ thông tin hệ thống. Đây là điều kiện tiên quyết (Blocker) trước khi triển khai lên môi trường Production.

---

## 2. Các bước triển khai chi tiết

### Bước 1: Kiểm soát SQL & Validation Chặt chẽ
**Mục tiêu:** Đảm bảo mọi câu lệnh SQL sinh ra bởi AI đều an toàn trước khi thực thi.
- **Tác vụ 1:** Audit hàm `validate_sql` trong Query Service - Kiểm tra các pattern injection, chặn multi-statement và các từ khóa nguy hiểm (DDL/DML: DROP, TRUNCATE, DELETE).
- **Tác vụ 2:** Verify tính năng Hard Limit - Đảm bảo mọi câu lệnh SELECT luôn được tự động thêm `LIMIT` để tránh treo DB.

> **Prompt gửi AI Agent:**
> ```text
> "Dựa trên mã nguồn tại services/query-service, hãy thực hiện Audit và nâng cấp hàm validate_sql. Đảm bảo chặn đứng các hành vi multi-statement và SQL injection. Ngoài ra, hãy kiểm tra logic tự động chèn LIMIT vào cuối câu lệnh SELECT. Kết quả: Query Service an toàn hơn."
> ```

### Bước 2: Hardening Docker & Non-root User
**Mục tiêu:** Giảm thiểu bề mặt tấn công bằng cách chạy container dưới quyền user hạn chế.
- **Tác vụ 1:** Cập nhật Dockerfile cho cả 3 services (Gateway, NL2SQL, Query) và Frontend - Thiết lập `USER appuser` thay vì chạy mặc định bằng root.
- **Tác vụ 2:** Sanitize Error Messages - Chỉnh sửa code Backend để bắt lỗi và trả về thông báo thân thiện, tuyệt đối không lộ stack trace hoặc thông tin DB ra ngoài.

> **Prompt gửi AI Agent:**
> ```text
> "Hãy kiểm tra toàn bộ Dockerfile trong workspace. Thực hiện tạo group/user 'appuser' và chuyển quyền thực thi sang user này (USER appuser). Đồng thời, cập nhật middleware xử lý lỗi để ẩn các thông tin kỹ thuật nhạy cảm khỏi response API. Kết quả: Docker images đạt chuẩn bảo mật Non-root."
> ```

### Bước 3: Trivy Security Scanning & Verification
**Mục tiêu:** Quét lỗ hổng bảo mật tự động trên các bản đóng gói (Images).
- **Tác vụ 1:** Sử dụng skill Trivy Security Scanning để quét toàn bộ các Docker images đã build.
- **Tác vụ 2:** Phân tích kết quả scan và khắc phục các lỗ hổng mức Critical/High.

> **Prompt gửi AI Agent:**
> ```text
> "Sử dụng skill Trivy Security Scanning, hãy thực hiện quét bảo mật cho 4 images: frontend, gateway, nl2sql, query. Mục tiêu: Không còn lỗ hổng mức Critical nào tồn tại. Kết quả: Báo cáo scan Trivy sạch (Pass)."
> ```

---

# Progress Report: Security Hardening & Non-root Docker
**Ngày cập nhật:** 16/05/2026
**Trạng thái tổng thể:** Đang triển khai (Priority: Critical)

## 📈 Tiến trình tổng quan (Progress Overview)
- **Tổng số tác vụ:** 5
- **Đã hoàn thành:** 1
- **Tiến độ (Completion):** 20%

---

## 📊 Chỉ số đánh giá (Evaluation Criteria)
| Chỉ số | Mục tiêu | Kết quả hiện tại | Đạt yêu cầu? |
| :--- | :--- | :--- | :--- |
| **Trivy Scan** | 0 Critical/High | Chưa quét | ⏳ |
| **Non-root Status** | 100% services | 0/4 | ❌ |
| **SQL Validation** | 100% patterns | Đã có cơ bản | ⚠️ |

---

## ✅ Các hạng mục đã hoàn thành (Done)
- [x] **Cơ chế Validation**: Hàm `validate_sql` đã được khởi tạo bước đầu ở Query Service.

## 🚧 Đang triển khai (In Progress)
- [ ] **Docker Refactoring**: Đang thử nghiệm chuyển đổi Gateway sang Non-root.
- [ ] **Error Sanitization**: Đang viết class xử lý lỗi tập trung.

## 🛑 Khó khăn & Khuyến nghị (Blockers & Recommendations)
- **Trivy Blocker**: PRD yêu cầu pass scan 100% mới được release. Cần ưu tiên quét sớm để xử lý các thư viện lỗi thời.

## 📅 Kế hoạch tiếp theo (Next Steps)
1. Thực hiện quét Trivy ngay lập tức để lấy baseline bảo mật.
2. Cập nhật đồng loạt các Dockerfile sang Non-root.
3. Chạy bộ test case SQL Injection để kiểm chứng hàm validation.
