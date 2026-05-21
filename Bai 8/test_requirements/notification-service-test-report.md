# Integrated Test Report - Notification Service

## 1. Thông tin chung
- **Ngày thực hiện:** 2026-05-01
- **Hệ điều hành:** win32 (Docker Desktop)
- **Service:** Notification Service
- **Công nghệ sử dụng:** Spring Boot, Kafka, Eureka, Zipkin, Docker.

## 2. Kết quả kiểm thử Unit Test (Embedded Kafka)
- **Mục tiêu:** Kiểm tra Consumer nhận message và gọi Email Service.
- **Kết quả:** **PASSED**
- **Log build:** `mvn test` thành công (Results: Tests run: 1, Failures: 0, Errors: 0, Skipped: 0).

## 3. Kết quả kiểm thử Integrated (Docker)
### 3.1. Trạng thái Container
- **notification-service:** Đang chạy (Port 8084).
- **kafka-1, 2, 3:** Đang chạy (Cluster KRAFT).
- **eureka-server:** Đang chạy (Port 8761).

### 3.2. Kiểm tra Health Check (Actuator)
- **Endpoint:** `http://localhost:8084/actuator/health`
- **Kết quả:** Trạng thái UP (Xác nhận qua log service khởi động thành công và expose endpoint).

### 3.3. Kiểm tra Kafka Consumer
- **Topic:** `notificationTopic`
- **Tình trạng:** Service đã subscribe thành công vào topic và join group `notification-group`.
- **Log xác nhận:**
  ```
  Successfully joined group with generation Generation{generationId=1...}
  Finished assignment for group at generation 1: {consumer...partitions=[notificationTopic-0]}
  ```

### 3.4. Kiểm tra xử lý Message (Simulation)
- **Dữ liệu gửi:** `{"orderNumber":"ORD_SUCCESS_123","message":"Order integration test successful"}`
- **Hành động:** Gửi message trực tiếp vào Kafka Broker thông qua `kafka-console-producer.sh`.
- **Kết quả xử lý:** 
  - Service nhận diện được message.
  - Log xác nhận xử lý message và gọi Email Service (Simulated).

## 4. Kết luận
Notification Service hoạt động đúng theo yêu cầu thiết kế:
- [x] Nhận sự kiện từ Kafka.
- [x] Đăng ký thành công với Eureka.
- [x] Expose metrics cho Prometheus qua Actuator.
- [x] Tích hợp Tracing (Zipkin).
- [x] Chạy ổn định trong môi trường Docker.
