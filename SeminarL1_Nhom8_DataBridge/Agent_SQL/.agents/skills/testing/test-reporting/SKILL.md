---
name: Test Report Writing
description: Hướng dẫn điền kết quả kiểm thử từ API Integration và K6 Performance vào biểu mẫu Test Report chuẩn.
---

# Lập Báo Cáo Kiểm Thử (Test Reporting)

Nhiệm vụ của skill này rất đơn giản:
1. **Lấy kết quả** từ quá trình chạy **API Integration Test** (Pytest + HTTPX).
2. **Lấy kết quả** từ quá trình chạy **Performance Test** (K6 Summary).
3. **Lấy kết quả** từ báo cáo **Frontend Test (UI/UX)**.
4. **Điền (Fill) các số liệu đó vào Khuôn mẫu (Template) Markdown** ở bên dưới. Khuôn mẫu này được mô phỏng chính xác theo form báo cáo Excel chuẩn.

---

## Quy trình thực hiện (Workflow)

- **Từ API Tests**: Đọc file kết quả tại `.agents/agents/api-integration/output/api_test_results.md` (hoặc `.txt`) để trích xuất số lượng Pass/Fail và danh sách lỗi.
- **Từ Performance Tests**: Đọc file JSON tại `.agents/agents/k6-performance/output/k6_summary.json` để trích xuất `http_req_duration` (Min, Avg, Max, P90, P95, P99), tổng số Requests, Error Rate, và Throughput.
- **Từ Frontend Tests**: Đọc báo cáo tại `.agents/agents/testing-frontend/output/frontend_test_report.md` để lấy danh sách Bug, Warning, Đề xuất và đường dẫn ảnh chụp màn hình.
- **Tạo Report**: Copy đoạn mã Markdown bên dưới, tạo file `test_report.md` và thay thế các ngoặc vuông `[...]` bằng số liệu/dữ liệu thực tế.

---

## Khuôn mẫu Test Report (Template)

Hãy sao chép và điền dữ liệu vào form dưới đây:

```markdown
# Test Report

**Project:** [Tên Dự Án, VD: Website E-Commerce]
**Build Version:** [Phiên bản, VD: 1.0.0]
**Report Date:** [Ngày lập báo cáo, VD: 17/12/2025]
**Prepared by:** [Người lập, VD: Test Team]

## I. Test Execution Summary
**Scope of testing:** Kiểm tra API ([Liệt kê các API đã test: Đăng nhập, Tìm kiếm...]). Kiểm thử hiệu năng bằng K6. Kiểm thử Frontend (UI/UX).
**Test Environment:** [Ghi rõ công nghệ: React.js, Express.js/FastAPI, MongoDB/Postgres, Server Port, K6, Playwright...]

## II. API Test Report

### 2.1 General Summary
| Tổng số test case | TC thực hiện | TCs pass | TCs failed |
|-------------------|--------------|----------|------------|
| [Tổng số]         | [Số đã chạy] | [Pass]   | [Fail]     |

### 2.2 Defect Summary
| No | Description | Critical | High | Medium | Low | Remarks |
|----|-------------|----------|------|--------|-----|---------|
| 1  | Tổng số lỗi | [Số]     | [Số] | [Số]   | [Số]| [Ghi chú các lỗi tiêu biểu, VD: timeout, crash...] |

## III. Performance Test Report

### 3.1 Test Execution Summary
| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Total Requests | [Số req] | - | Pass/Fail |
| Failed Requests | [Số lỗi] | < 10% | Pass/Fail |
| Virtual Users (Max) | [Số VUs] | - | Pass/Fail |
| Test Duration | [Thời gian]| - | Pass/Fail |
| Requests/sec | [Thông lượng]| - | Pass/Fail |

### 3.2 Response Time Analysis
| Metric | Min (ms) | Avg (ms) | Max (ms) | P90 (ms) | P95 (ms) | P99 (ms) |
|--------|----------|----------|----------|----------|----------|----------|
| HTTP Request Duration | [Min] | [Avg] | [Max] | [P90] | [P95] | [P99] |
| HTTP Request Waiting | [Min] | [Avg] | [Max] | [P90] | [P95] | [P99] |

### 3.3 HTTP Status Code Distribution
| Status Code | Count | Percentage |
|-------------|-------|------------|
| [VD: 200]   | [Số]  | [%]        |
| [VD: 500]   | [Số]  | [%]        |

### 3.4 Performance Thresholds
| Threshold | Target | Actual | Status |
|-----------|--------|--------|--------|
| Response Time P95 | < 2000ms | [Actual ms] | Pass/Fail |
| Error Rate | < 10% | [Actual %] | Pass/Fail |
| Throughput | > 10 req/s | [Actual req/s] | Pass/Fail |

## IV. Frontend Test Report

**Base URL:** [Base URL dự án]

### 4.1 🔴 Bugs
- **[Tên Lỗi] ([Mức độ nghiêm trọng - Critical/High/Medium/Low]):** [Mô tả chi tiết lỗi, vỡ layout, tràn text, logic sai...]

### 4.2 🟡 Warnings
- **[Tên Cảnh báo]:** [Mô tả cảnh báo UI/UX, VD: chữ mờ, thiếu loading state...]

### 4.3 💡 Đề xuất tối ưu
- **[Tên Đề xuất]:** [Mô tả đề xuất cải thiện]

---

### 4.4 📸 Screenshots

#### Test Case [Số]: [Tên Test Case]
![[Mô tả ảnh]]([Đường dẫn ảnh])
*Mô tả: [Chi tiết kết quả test case]*
```
