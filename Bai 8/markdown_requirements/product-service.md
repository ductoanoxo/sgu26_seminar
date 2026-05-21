# Đề bài: Xây dựng Product Service trong hệ thống Microservices

## 🎯 Mục tiêu
- Hiểu và áp dụng kiến thức về Spring Boot để xây dựng một microservice  
- Sử dụng PostgreSQL làm cơ sở dữ liệu để lưu trữ thông tin sản phẩm  
- Triển khai các REST API cơ bản để quản lý sản phẩm  

---

## 📌 Yêu cầu chi tiết

### 1. Tạo ứng dụng Spring Boot
- Sử dụng Spring Initializr hoặc IntelliJ IDE để khởi tạo dự án với các dependency:
  - Spring Web  
  - Spring Data  
  - Lombok  

---

### 2. Xây dựng các REST API

#### ➤ Tạo sản phẩm mới
- **API:** `POST /api/product`
- **Request body:**
```json
{
  "name": "iPhone 13",
  "description": "iPhone 13",
  "price": 1200
}
```
- **Response:** HTTP Status `201 (Created)`

#### ➤ Lấy danh sách tất cả sản phẩm
- **API:** `GET /api/product`
- **Response:**
```json
[
  {
    "id": "12345",
    "name": "iPhone 13",
    "description": "iPhone 13",
    "price": 1200
  }
]
```

---

### 3. Sử dụng cơ sở dữ liệu

- Tạo model **Product** với các trường:
  - `id` (String)  
  - `name` (String)  
  - `description` (String)  
  - `price` (BigDecimal)  

- Sử dụng **Spring Data MongoDB** để thao tác với database  
- Tạo interface `ProductRepository` kế thừa từ `MongoRepository`

---

### 4. Tích hợp Actuator và Prometheus

- Cấu hình Actuator để expose các endpoint:
  - Health check: `/actuator/health`  
  - Metrics: `/actuator/prometheus`  

- Sử dụng **Micrometer** để tích hợp với:
  - Prometheus  
  - Zipkin  

---

### 5. Triển khai với Docker

- Tạo `Dockerfile` để đóng gói ứng dụng  
- Sử dụng `Docker Compose` để chạy:
  - Application  
  - MongoDB  
  - Eureka Server  

---

## 💡 Gợi ý

### Công nghệ sử dụng
- Spring Boot  
- Spring Data  
- Lombok  
- Docker  

### Tài liệu tham khảo
- https://spring.io/projects/spring-boot  
- https://www.testcontainers.org/  

---

## 📁 Cấu trúc dự án tham khảo

```bash
product-service/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   ├── com.hdbank.productservice/
│   │   │   │   ├── controller/
│   │   │   │   ├── model/
│   │   │   │   ├── repository/
│   │   │   │   ├── service/
│   │   │   │   ├── dto/
│   │   │   │   ├── util/
│   │   │   │   └── ProductServiceApplication.java
│   │   └── resources/
│   │       ├── application.properties
│   │       └── banner.txt
│   └── test/
│       └── java/
│           └── com.hdbank.productservice/
│               └── ProductServiceApplicationTests.java
└── pom.xml
```

---

## 🚀 Phần mở rộng (optional)
- Thêm Circuit Breaker (Resilience4j)  
- Triển khai lên Kubernetes  
- Logging & Tracing với ELK Stack hoặc Jaeger  
