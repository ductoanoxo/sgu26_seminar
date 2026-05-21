# Week7-Microservices

## 1. Giới thiệu

Đây là workspace tổng hợp cho seminar về kiến trúc **Microservices** với Java Spring Boot.
Nội dung bao gồm:

- Tài liệu yêu cầu và giải thích từng service
- Demo hệ thống microservices cơ bản
- Dự án backend thương mại điện tử theo mô hình microservices
- Tài nguyên hình ảnh, PDF và tài liệu markdown phục vụ báo cáo

## 2. Công nghệ chính

- Java 17
- Spring Boot
- Spring Cloud Gateway
- Eureka Service Discovery
- PostgreSQL / MongoDB (tùy service)
- Kafka
- Docker, Docker Compose
- Kubernetes (với bộ manifest trong thư mục k8s)
- Maven

## 3. Cấu trúc thư mục chính

```text
Week7-Microservices/
|- README.md
|- docs/
|- Explain/
|  |- notification-service.md
|  |- Product-Service-Explanation.md
|- image/
|- markdown_requirements/
|  |- api-gateway.md
|  |- discovery-server.md
|  |- notification-service.md
|  |- order-service.md
|  \- product-service.md
|- PDF_requirements/
|- microservices_api_demo/
|  \- microservices_api_demo/
|     |- docker-compose.yml
|     |- pom.xml
|     |- api-gateway/
|     |- discovery-server/
|     |- inventory-service/
|     |- notification-service/
|     |- order-service/
|     \- product-service/
|  \- microservices_api_demo;C/
|- ProjectWeb-BE/
|  |- docker-compose.yml
|  |- api-gateway/
|  |- eureka-server/
|  |- notification-service/
|  |- order-service/
|  |- payment-service/
|  |- product-service/
|  |- user-service/
|  \- k8s/
|- ProjectWeb-main/
|  |- README.md
|  |- BE/
|  \- FE/react-e-commerce/
|- slides/
\- video/
   \- link_video.txt
```

## 4. Hai cụm backend chính trong workspace

### 4.1 Cụm demo: microservices_api_demo

Mục tiêu: minh họa luồng đặt hàng cơ bản trong môi trường microservices.

Các service chính:

- API Gateway: định tuyến request vào các service
- Discovery Server: đăng ký và khám phá service
- Product Service: quản lý thông tin sản phẩm
- Inventory Service: quản lý tồn kho
- Order Service: xử lý đơn hàng
- Notification Service: gửi thông báo liên quan đến đơn hàng

### 4.2 Cụm backend mở rộng: ProjectWeb-BE

Mục tiêu: backend hoàn chỉnh hơn cho bài toán thương mại điện tử.

Các service chính:

- API Gateway
- Eureka Server
- User Service
- Product Service
- Order Service
- Payment Service
- Notification Service

Thư mục `k8s/` chứa các file triển khai Kubernetes cho từng service.

## 5. Tài liệu học tập và báo cáo

- `markdown_requirements/`: mô tả yêu cầu chức năng theo từng service
- `Explain/`: giải thích chi tiết một số service
- `docs/`, `PDF_requirements/`, `image/`: tài liệu, hình minh họa và nguồn tham khảo cho seminar
- `slides/`: slide dùng cho phần trình bày tuần 7
- `video/link_video.txt`: liên kết video demo hệ thống

## 6. Thư mục bổ sung mới trong Week7

- `ProjectWeb-main/`: mã nguồn dự án tổng hợp (bao gồm backend và frontend React)
- `slides/`: bộ slide phục vụ báo cáo seminar microservices
- `video/`: tài nguyên video minh họa và demo
- `microservices_api_demo/microservices_api_demo;C/`: thư mục phát sinh trong quá trình làm việc local

## 7. Hướng dẫn chạy nhanh (tham khảo)

### 7.1 Chạy cụm microservices_api_demo

```bash
cd microservices_api_demo/microservices_api_demo
mvn clean install
docker compose up -d
```

Hoặc chạy từng service:

```bash
cd microservices_api_demo/microservices_api_demo/product-service
mvn spring-boot:run
```

Lặp lại tương tự cho các service còn lại.

### 7.2 Chạy cụm ProjectWeb-BE

```bash
cd ProjectWeb-BE
mvn clean install
docker compose up -d
```

Nếu muốn chạy local từng service:

```bash
cd ProjectWeb-BE/user-service
mvn spring-boot:run
```

## 8. Gợi ý thứ tự tìm hiểu cho seminar

- Bước 1: đọc yêu cầu trong `markdown_requirements/`
- Bước 2: xem code theo luồng Product -> Inventory -> Order -> Notification
- Bước 3: tìm hiểu định tuyến qua API Gateway và đăng ký service với Eureka
- Bước 4: chạy Docker Compose để demo toàn hệ thống
- Bước 5: mở rộng triển khai bằng các manifest trong `ProjectWeb-BE/k8s/`

## 9. Ghi chú

- Một số thư mục có thể chứa output build (`target/`) và file cấu hình triển khai.
- Tùy môi trường máy, bạn cần cài sẵn Java 17+, Maven và Docker trước khi chạy.
