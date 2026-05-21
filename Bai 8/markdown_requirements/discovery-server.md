# Đề bài: Xây dựng Discovery Server trong hệ thống Microservices

## Mục tiêu
• Hiểu cơ chế Service Discovery trong kiến trúc microservices.  
• Sử dụng Eureka Server để đăng ký và quản lý các service.  
• Cho phép các service tự động tìm thấy nhau thông qua Discovery Server.  

---

## Yêu cầu chi tiết

### 1. Tạo ứng dụng Spring Boot
Khởi tạo dự án với các dependency:

• Spring Cloud Netflix Eureka Server  
• Spring Boot Actuator  
• Lombok  

---

### 2. Cấu hình Eureka Server

Trong class main:
```
@EnableEurekaServer
```

Cấu hình application.properties:
```properties
spring.application.name=discovery-server
server.port=8761
```

Truy cập dashboard:
```
http://localhost:8761
```

---

### 3. Đăng ký service

Các service sau phải đăng ký vào Discovery Server:

• product-service  
• inventory-service  
• order-service  
• notification-service  
• api-gateway  

Cấu hình trong các service:
```properties
eureka.client.serviceUrl.defaultZone=http://localhost:8761/eureka
```

---

### 4. Tích hợp Actuator

Expose endpoint:
```
/actuator/health
```

---

### 5. Triển khai bằng Docker

• Tạo Dockerfile cho Discovery Server  
• Chạy cùng hệ thống bằng Docker Compose  

---

## Gợi ý

### Công nghệ

• Spring Boot  
• Eureka Server  
• Actuator  
• Docker  

---

### Tài liệu

https://spring.io/guides/gs/service-registration-and-discovery/

---

### Cấu trúc dự án tham khảo

```bash
discovery-server/
├── src/
│ ├── main/
│ │ ├── java/
│ │ │ ├── com.hdbank.discoveryserver/
│ │ │ │ └── DiscoveryServerApplication.java
│ │ └── resources/
│ │ ├── application.properties
│ │ └── banner.txt
│ └── test/
│ └── java/
│ └── com.hdbank.discoveryserver/
│ └── DiscoveryServerApplicationTests.java
└── pom.xml
```

---

## Phần mở rộng

• Triển khai cluster Eureka Server.  
• Thêm authentication cho dashboard.  
