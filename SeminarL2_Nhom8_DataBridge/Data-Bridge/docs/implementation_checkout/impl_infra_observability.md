# Implementation Plan: Hạ tầng & Observability

## 1. Overview (Tổng quan)
Module Hạ tầng & Observability đảm bảo hệ thống Agent_SQL hoạt động ổn định, an toàn và dễ dàng giám sát. Việc tích hợp OpenTelemetry giúp trace các luồng xử lý phức tạp xuyên suốt các microservices, kết hợp CI/CD tự động và bảo mật RLS trên database.

---

## 2. Các bước triển khai chi tiết
### Bước 1: Tích hợp OpenTelemetry tracing
**Mục tiêu:** Cung cấp distributed tracing xuyên suốt 3 backend services (Gateway → NL2SQL → Query).
- **Tác vụ 1:** Thiết lập OTel SDK trên các dịch vụ.
- **Tác vụ 2:** Gắn span cho các xử lý chính và export trace sang Alloy/Tempo.

> **Prompt gửi AI Agent:**
> ```text
> "Sử dụng kiến thức Python/OTel, hãy thực hiện tích hợp OpenTelemetry cho 3 backend services (Gateway, NL2SQL, Query). Mục tiêu: Trace được request từ Gateway sang NL2SQL rồi đến Query. Đầu ra: Các service có gửi trace data sang endpoint của Alloy."
> ```

### Bước 2: Query fingerprint caching
**Mục tiêu:** Cải thiện performance bằng cách cache các truy vấn tương tự nhau dựa vào fingerprint.
- **Tác vụ 1:** Tính fingerprint (hash/semantic) cho NL2SQL query.
- **Tác vụ 2:** Lưu cache trên Redis hoặc DB, nếu có cache thì trả về ngay.

> **Prompt gửi AI Agent:**
> ```text
> "Sử dụng kiến thức Redis/Caching, hãy thực hiện tính toán fingerprint cho các yêu cầu NL2SQL và lưu cache. Mục tiêu: Giảm tải cho model sinh SQL. Đầu ra: Chức năng cache hoạt động ở NL2SQL service."
> ```

### Bước 3: RLS hardening trên Supabase
**Mục tiêu:** Đảm bảo chỉ người dùng có quyền mới được đọc/ghi dữ liệu tương ứng.
- **Tác vụ 1:** Review các bảng hiện tại trên Supabase.
- **Tác vụ 2:** Áp dụng policies RLS chặt chẽ theo user_id hoặc role.

> **Prompt gửi AI Agent:**
> ```text
> "Sử dụng skill supabase, hãy thực hiện review và cập nhật RLS policies trên database. Mục tiêu: Đảm bảo dữ liệu không bị lộ chéo giữa các user. Đầu ra: Mã SQL migration cập nhật RLS."
> ```

### Bước 4: CI/CD pipeline chạy test + Trivy scan tự động
**Mục tiêu:** Tự động hóa quá trình kiểm thử và rà soát bảo mật.
- **Tác vụ 1:** Tạo file cấu hình CI (vd: `.github/workflows/ci.yml`).
- **Tác vụ 2:** Tích hợp Pytest và Trivy scan vào luồng build.

> **Prompt gửi AI Agent:**
> ```text
> "Sử dụng skill Trivy Security Scanning và api-integration-expert, hãy thực hiện viết luồng CI/CD (GitHub Actions) để chạy tự động test và bảo mật. Mục tiêu: Có pipeline tự động kích hoạt khi push code. Đầu ra: File YAML workflow hoàn chỉnh."
> ```

---

# Progress Report: Hạ tầng & Observability
**Ngày cập nhật:** 16/05/2026
**Trạng thái tổng thể:** Đang triển khai

## 📈 Tiến trình tổng quan (Progress Overview)
- **Tổng số tác vụ:** 6
- **Đã hoàn thành:** 2
- **Tiến độ (Completion):** 33%

---

## 📊 Chỉ số đánh giá (Evaluation Criteria)
| Chỉ số | Mục tiêu | Kết quả hiện tại | Đạt yêu cầu? |
| :--- | :--- | :--- | :--- |
| **Uptime (Observability)** | > 99% | Đang thiết lập | ⏳ |
| **Tracing Coverage** | 100% services | 0% | ❌ |
| **Pipeline Success Rate** | 100% | Chưa có | ⏳ |

---

## ✅ Các hạng mục đã hoàn thành (Done)
- [x] **Thiết lập Docker Compose dev**: Môi trường dev cục bộ đã được thiết lập.
- [x] **Triển khai Kafka & Observability Core**: Grafana, Prometheus, Alloy đã được triển khai ở Docker Swarm riêng.

## 🚧 Đang triển khai (In Progress)
- [ ] **Tích hợp OpenTelemetry tracing**: Tích hợp vào 3 backend services (trace Gateway → NL2SQL → Query).
- [ ] **Query fingerprint caching**: Triển khai cơ chế caching dựa trên query fingerprint.
- [ ] **RLS hardening trên Supabase**: Củng cố các chính sách bảo mật RLS.
- [ ] **CI/CD pipeline**: Tự động chạy test + Trivy scan tự động.

## 🛑 Khó khăn & Khuyến nghị (Blockers & Recommendations)
- **Cấu hình OpenTelemetry**: Cần đảm bảo context propagation giữa các service đi qua Kafka/gRPC hoạt động trơn tru.

## 📅 Kế hoạch tiếp theo (Next Steps)
1. Tích hợp OpenTelemetry vào Gateway Service trước để làm chuẩn.
2. Xây dựng CI pipeline cơ bản (chạy Pytest + Trivy) trên GitHub Actions/GitLab CI.
3. Review và củng cố cấu hình RLS trên Supabase.
