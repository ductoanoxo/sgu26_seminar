# Implementation Plan: Kiểm thử Toàn diện (QA Automation)

## 1. Overview (Tổng quan)
Module Kiểm thử Toàn diện (QA Automation) thiết lập quy trình đảm bảo chất lượng phần mềm tự động xuyên suốt dự án Agent_SQL. Dựa trên tiêu chuẩn QA (Section 5.3), module này giải quyết vấn đề thiếu hụt test case bằng cách tận dụng 5 Skills chuyên dụng để tự động hóa việc sinh kịch bản, kiểm thử tích hợp API và đo lường hiệu năng (Load Test).

---

## 2. Các bước triển khai chi tiết

### Bước 1: Thiết lập Integration Testing Framework
**Mục tiêu:** Xây dựng bộ kiểm thử tích hợp cho toàn bộ các Endpoints của microservices.
- **Tác vụ 1:** Sử dụng skill `api-integration-expert` để viết Pytest + Httpx cho Gateway, NL2SQL và Query services.
- **Tác vụ 2:** Viết bộ Unit tests chuyên sâu cho hàm `validate_sql`, bao gồm các trường hợp injection và edge cases.

> **Prompt gửi AI Agent:**
> ```text
> "Dựa trên cấu trúc thư mục services/, hãy sử dụng skill api-integration-expert để viết bộ Integration Tests hoàn chỉnh cho 3 dịch vụ. Đặc biệt, hãy viết riêng một file test_security.py để kiểm thử hàm validate_sql với 20+ patterns injection phổ biến. Kết quả: Bộ test Pytest đạt coverage > 80%."
> ```

### Bước 2: Tự động hóa kịch bản & Hiệu năng
**Mục tiêu:** Sinh test case tự động và kiểm tra sức chịu tải của hệ thống.
- **Tác vụ 1:** Sử dụng skill `Automated Test Case Generation` để sinh kịch bản kiểm thử dựa trên PRD và Swagger API.
- **Tác vụ 2:** Sử dụng skill `k6 Performance Testing` để đo lường hiệu năng các endpoint quan trọng như `/ask` và `/query/manual`.

> **Prompt gửi AI Agent:**
> ```text
> "Sử dụng skill Automated Test Case Generation để sinh ra 50 kịch bản kiểm thử cho toàn hệ thống. Sau đó, hãy dùng skill k6-performance để chạy Load Test với 100 concurrent users cho endpoint /ask. Kết quả: File kịch bản .csv và kết quả k6 report."
> ```

### Bước 3: Tổng hợp báo cáo kiểm thử (Test Reporting)
**Mục tiêu:** Xuất báo cáo chất lượng định kỳ giúp Admin theo dõi độ tin cậy của hệ thống.
- **Tác vụ 1:** Sử dụng skill `Test Report Writing` để tổng hợp kết quả từ Pytest và k6.
- **Tác vụ 2:** Tích hợp việc chạy test vào quy trình CI/CD (nếu có) hoặc tạo script chạy toàn bộ (`run_all_tests.sh`).

> **Prompt gửi AI Agent:**
> ```text
> "Sử dụng skill Test Report Writing để tổng hợp toàn bộ kết quả kiểm thử từ Bước 1 và Bước 2 vào một file báo cáo Markdown chuyên nghiệp. Đảm bảo nêu rõ tỷ lệ Pass/Fail và các khuyến nghị về hiệu năng. Kết quả: File QA_REPORT_FINAL.md."
> ```

---

# Progress Report: Kiểm thử Toàn diện
**Ngày cập nhật:** 16/05/2026
**Trạng thái tổng thể:** Đang triển khai

## 📈 Tiến trình tổng quan (Progress Overview)
- **Tổng số tác vụ:** 5
- **Đã hoàn thành:** 0
- **Tiến độ (Completion):** 0%

---

## 📊 Chỉ số đánh giá (Evaluation Criteria)
| Chỉ số | Mục tiêu | Kết quả hiện tại | Đạt yêu cầu? |
| :--- | :--- | :--- | :--- |
| **API Coverage** | > 90% | 10% | ❌ |
| **P95 Latency** | < 1.5s | Chưa đo | ⏳ |
| **Security Test Pass**| 100% | 0% | ❌ |

---

## ✅ Các hạng mục đã hoàn thành (Done)
- (Chưa có hạng mục nào hoàn thành)

## 🚧 Đang triển khai (In Progress)
- [ ] **Infrastructure Setup**: Đang chuẩn bị môi trường chạy k6 và Pytest.
- [ ] **Test Case Drafting**: Đang viết các kịch bản test đầu tiên cho Gateway.

## 🛑 Khó khăn & Khuyến nghị (Blockers & Recommendations)
- **Test Data**: Cần một database test riêng biệt để không ảnh hưởng đến dữ liệu thực tế khi chạy Integration Tests.

## 📅 Kế hoạch tiếp theo (Next Steps)
1. Viết bộ Unit test cho `validate_sql` để đảm bảo an ninh.
2. Chạy k6 baseline để xác định hiệu năng hiện tại của hệ thống.
3. Sinh test case tự động cho module Frontend SQL Editor.
