# Đề bài: Xây dựng Order Service trong hệ thống Microservices

## Mục tiêu:
- Hiểu và áp dụng kiến thức về Spring Boot để xây dựng một microservice quản lý đơn hàng.
- Sử dụng Spring Data JPA để lưu trữ thông tin đơn hàng trong cơ sở dữ liệu quan hệ (MySQL hoặc PostgreSQL).
- Tích hợp với Eureka Discovery Server để đăng ký và quản lý service.
- Sử dụng Resilience4j để xử lý lỗi và tăng tính ổn định của hệ thống.
- Tích hợp Kafka để gửi thông báo khi đơn hàng được đặt thành công.
- Thực hành viết unit test và integration test.

---

## Yêu cầu chi tiết:

### 1. Tạo ứng dụng Spring Boot
- Spring Web
- Spring Data JPA
- Spring Cloud Eureka Client
- Spring Cloud Circuit Breaker (Resilience4j)
- Spring Kafka
- Lombok
- Spring Boot Actuator
- Micrometer Tracing (Zipkin)
- Micrometer Registry Prometheus

---

### 2. Xây dựng các REST API

#### Đặt đơn hàng:
- API: POST /api/order

```json
{
  "orderLineItemsDtoList": [
    {
      "skuCode": "iphone_13",
      "price": 1200,
      "quantity": 1
    }
  ]
}
```

- Response: HTTP 201 - "Order Placed"

---

### 3. Database Models

#### Order:
- id (Long)
- orderNumber (String)
- orderLineItemsList (List<OrderLineItems>)

#### OrderLineItems:
- id (Long)
- skuCode (String)
- price (BigDecimal)
- quantity (Integer)

---

### 4. Eureka Config

```properties
eureka.client.serviceUrl.defaultZone=http://localhost:8761/eureka
spring.application.name=order-service
```

---

### 5. Kafka
- Topic: notificationTopic

---

### 6. Resilience4j
- Circuit Breaker
- Retry
- Timeout

---

### 7. Actuator & Prometheus
- /actuator/health
- /actuator/prometheus

---

### 8. Testing
- Success case
- Fail case
- Coverage >= 80%

---

### 9. Docker
- Dockerfile
- Docker Compose

---

## Project Structure

```bash
order-service/
├── src/
│   ├── main/
│   ├── test/
└── pom.xml
```
