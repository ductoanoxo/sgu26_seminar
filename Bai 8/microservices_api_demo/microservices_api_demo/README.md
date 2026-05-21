# microservices_api_demo

## Tổng Quan

`microservices_api_demo` là cụm demo microservices cho Bài 8 của môn Seminar chuyên ngành. Dự án mô phỏng một hệ thống thương mại điện tử với các service tách biệt, giao tiếp qua Eureka, Kafka và API Gateway.

Cụm này được dùng để chứng minh các requirement đã phân tích ở Bài 7, bao gồm service discovery, routing, xử lý đơn hàng, đồng bộ tồn kho, gửi thông báo và quan sát hệ thống.

## Mục Lục

1. [Kiến trúc tổng quan](#kiến-trúc-tổng-quan)
2. [Các service chính](#các-service-chính)
3. [Công nghệ sử dụng](#công-nghệ-sử-dụng)
4. [Cấu trúc thư mục](#cấu-trúc-thư-mục)
5. [Hướng dẫn chạy nhanh](#hướng-dẫn-chạy-nhanh)
6. [API chính](#api-chính)
7. [Tài liệu liên quan](#tài-liệu-liên-quan)

## Kiến Trúc Tổng Quan

Hệ thống gồm 5 service nghiệp vụ và 1 tầng hạ tầng trung tâm:

- Discovery Server: đăng ký và tìm kiếm service.
- API Gateway: định tuyến request từ client.
- Product Service: quản lý thông tin sản phẩm.
- Order Service: xử lý đặt hàng và phát sự kiện.
- Inventory Service: kiểm tra và cập nhật tồn kho.
- Notification Service: nhận sự kiện và mô phỏng gửi email.

Luồng chính của hệ thống:

Client -> API Gateway -> Service đích -> Kafka -> Notification Service

## Các Service Chính

| Service | Vai trò | Port mặc định |
| :--- | :--- | :---: |
| Discovery Server | Service registry | 8761 |
| API Gateway | Cổng vào hệ thống | 8181 |
| Product Service | CRUD sản phẩm | 8081 |
| Order Service | Tạo đơn hàng | 8082 |
| Inventory Service | Quản lý tồn kho | 8083 |
| Notification Service | Nhận event và gửi thông báo | 8084 |

## Công Nghệ Sử Dụng

- Spring Boot 3
- Spring Cloud Gateway
- Spring Cloud Eureka
- Spring Data JPA / MongoDB theo từng service
- Apache Kafka
- Redis
- Spring Security / OAuth2
- Actuator, Prometheus, Zipkin
- Docker và Docker Compose

## Cấu Trúc Thư Mục

```text
microservices_api_demo/
├── api-gateway/
├── discovery-server/
├── inventory-service/
├── notification-service/
├── order-service/
├── product-service/
├── docker-compose.yml
├── pom.xml
├── init-databases.sh
├── seed_data.ps1
├── kafka-data/
└── README.md
```

## Hướng Dẫn Chạy Nhanh

### Yêu cầu tối thiểu

- Java 21
- Docker và Docker Compose
- Maven

### Chạy bằng Docker Compose

```bash
docker compose up -d
```

### Chạy từng service bằng Maven

```bash
cd discovery-server
mvn spring-boot:run
```

Tùy nhu cầu, bạn có thể khởi động các service còn lại tương tự: `api-gateway`, `product-service`, `order-service`, `inventory-service`, `notification-service`.

## API Chính

### Product Service

- `POST /api/product`: tạo sản phẩm mới
- `GET /api/product`: lấy danh sách sản phẩm

### Inventory Service

- `GET /v1/api/inventory?skuCode=...`: kiểm tra tồn kho

### Order Service

- `POST /api/order`: đặt đơn hàng

### API Gateway

- `/api/product/**` -> `product-service`
- `/api/order/**` -> `order-service`
- `/api/inventory/**` -> `inventory-service`

## Tài Liệu Liên Quan

- [README tổng Bài 8](../README.md)
- [Báo cáo tổng](../../docs/_MConverter.eu_Báo%20cáo%20tổng.md)
- [Requirement API Gateway](../../markdown_requirements/api-gateway.md)
- [Requirement Discovery Server](../../markdown_requirements/discovery-server.md)
- [Requirement Product Service](../../markdown_requirements/product-service.md)
- [Requirement Order Service](../../markdown_requirements/order-service.md)
- [Requirement Notification Service](../../markdown_requirements/notification-service.md)
- [Test results](../../test_requirements/test_results.md)

## Ghi Chú

Đây là README tổng cho cụm demo microservices trong Bài 8. Phần báo cáo chi tiết hơn nằm ở thư mục `docs/`, còn yêu cầu và kết quả kiểm thử nằm trong `markdown_requirements/` và `test_requirements/`.

