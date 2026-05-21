# Đề bài: Xây dựng API Gateway trong hệ thống Microservices

## Mục tiêu
• Hiểu và áp dụng kiến trúc API Gateway trong hệ thống microservices.  
• Sử dụng Spring Cloud Gateway để định tuyến các request từ client đến các service tương ứng.  
• Tích hợp với Eureka Discovery Server để tìm và định tuyến đến các service động.  
• Tích hợp Actuator và Prometheus để giám sát hệ thống.  

---

## Yêu cầu chi tiết

### 1. Tạo ứng dụng Spring Boot
Sử dụng Spring Initializr để khởi tạo dự án với các dependency:

• Spring Cloud Gateway  
• Spring Cloud Eureka Client  
• Spring Boot Actuator  
• Micrometer Registry Prometheus  
• Lombok  

---

### 2. Cấu hình routing

Gateway phải định tuyến request đến các service sau:

| Route | Service |
|------|--------|
| /api/product/** | product-service |
| /api/order/** | order-service |
| /api/inventory/** | inventory-service |

#### Ví dụ:

Request:
```
GET /api/product
```

Gateway phải forward request đến:
```
product-service
```

---

### 3. Tích hợp với Eureka Discovery Server

Cấu hình application.properties:

```properties
spring.application.name=api-gateway
eureka.client.serviceUrl.defaultZone=http://localhost:8761/eureka
```

Gateway phải tự động tìm địa chỉ của các service thông qua Eureka.

---

### 4. Tích hợp Actuator và Prometheus

Expose các endpoint:

• Health check  
```
/actuator/health
```

• Metrics  
```
/actuator/prometheus
```

---

### 5. Triển khai ứng dụng với Docker

• Tạo Dockerfile cho API Gateway  
• Chạy cùng các service khác bằng Docker Compose  

---

## Gợi ý

### 1. Công cụ và công nghệ sử dụng

• Spring Boot  
• Spring Cloud Gateway  
• Eureka Client  
• Actuator  
• Prometheus  
• Docker  

---

### 2. Tài liệu tham khảo

Spring Cloud Gateway  
https://spring.io/projects/spring-cloud-gateway  

Service Discovery  
https://spring.io/guides/gs/service-registration-and-discovery/  

---

### 3. Cấu trúc dự án tham khảo

```bash
api-gateway/
├── src/
│ ├── main/
│ │ ├── java/
│ │ │ ├── com.hdbank.apigateway/
│ │ │ │ ├── config/
│ │ │ │ ├── filter/
│ │ │ │ └── ApiGatewayApplication.java
│ │ └── resources/
│ │ ├── application.properties
│ │ └── banner.txt
│ └── test/
│ └── java/
│ └── com.hdbank.apigateway/
│ └── ApiGatewayApplicationTests.java
└── pom.xml
```

---

## Phần mở rộng (nếu có thời gian)

• Thêm Global Filter để log request.  
• Thêm Rate Limiting.  
• Thêm JWT Authentication.  
