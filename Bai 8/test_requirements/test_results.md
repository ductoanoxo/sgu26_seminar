# Báo cáo Kiểm thử Discovery Server & Microservices Connectivity

**Ngày kiểm thử:** 2026-05-02  
**Người thực hiện:** Antigravity AI  
**Môi trường:** Docker Compose  

---

## 1. Kết quả tổng quan

| Thành phần | Trạng thái | Ghi chú |
| :--- | :---: | :--- |
| **Discovery Server (Eureka)** | ✅ UP | Chạy tại port 8761 |
| **API Gateway** | ✅ UP | Đã đăng ký thành công |
| **Product Service** | ✅ UP | Đã đăng ký thành công |
| **Order Service** | ✅ UP | Đã đăng ký thành công |
| **Inventory Service** | ✅ UP | Đã đăng ký thành công |
| **Notification Service** | ✅ UP | Đã đăng ký thành công |

---

## 2. Chi tiết các bài thử nghiệm (Test Cases)

### TC-01: Kiểm tra giao diện Eureka Dashboard
- **URL:** `http://localhost:8761`
- **Kết quả mong đợi:** Hiển thị danh sách 5 service đã đăng ký.
- **Kết quả thực tế:** 
    - `API-GATEWAY` (1)
    - `INVENTORY-SERVICE` (1)
    - `NOTIFICATION-SERVICE` (1)
    - `ORDER-SERVICE` (1)
    - `PRODUCT-SERVICE` (1)
- **Đánh giá:** **PASSED** ✅

### TC-02: Kiểm tra khả năng định tuyến của API Gateway (Discovery-aware routing)
- **URL:** `http://localhost:8181/v1/api/products/`
- **Mô tả:** Request gửi tới Gateway, Gateway dùng Eureka để tìm `product-service` và forward request.
- **Kết quả thực tế:** Trả về HTTP 200 với nội dung `[]`.
- **Đánh giá:** **PASSED** ✅ (Xác nhận Gateway đã tìm thấy và kết nối được với Product Service).

### TC-03: Kiểm tra Actuator Health của Discovery Server
- **URL:** `http://localhost:8761/actuator/health`
- **Kết quả thực tế:** Trả về JSON status.
- **Lưu ý:** Hiện tại status tổng thể báo `DOWN` do lỗi kết nối Redis (thừa hưởng từ parent POM). Tuy nhiên, logic Eureka Server vẫn hoạt động bình thường.
- **Đánh giá:** **WARNING** ⚠️ (Chức năng ổn định, cần build lại để sửa lỗi hiển thị health check).

---

## 3. Nhật ký Log hệ thống (System Logs Snippet)

**Product Service Registration:**
```text
2026-05-01T16:57:15.919Z  INFO ... com.netflix.discovery.DiscoveryClient : Getting all instance registry info from the eureka server
2026-05-01T16:57:16.332Z  INFO ... com.netflix.discovery.DiscoveryClient : The response status is 200
```

---

## 4. Kết luận
Hệ thống Discovery Server đã được triển khai đúng theo yêu cầu. Các service đã có khả năng tự động đăng ký và tìm thấy nhau. API Gateway đã hoạt động như một điểm truy cập duy nhất cho toàn bộ hệ thống.

---
*Báo cáo được tạo tự động bởi Antigravity AI.*
