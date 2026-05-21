# 🛒 Week 8 – Vibe Engineering: Hệ Thống E-Commerce Microservices Toàn Diện

Chào mừng bạn đến với tài liệu kiến trúc và hướng dẫn vận hành chi tiết của dự án **Vibe Engineering E-Commerce**. Đây là một hệ thống thương mại điện tử được xây dựng theo kiến trúc **Microservices** chuẩn Doanh nghiệp (Enterprise-grade), kết hợp các công nghệ **Cloud Native** và quy trình **CI/CD** tự động hóa triển khai lên **Kubernetes**.

---

## 📂 Cấu trúc thư mục

```text
Week8 - Vibe Engineering/
├── 📄 README.md                          ← Tài liệu này
├── 📁 .claude/                           ← Cấu hình Claude AI assistant
│   └── settings.local.json
├── 📁 docs/                              ← Báo cáo Word chi tiết từng service
│   ├── A_discorvery_service.docx
│   ├── B_api_gateway.docx
│   ├── C, E_Product&Notification.docx
│   ├── D_OrderServices.docx
│   └── Báo cáo tổng.docx
├── 📁 image/                             ← Ảnh chụp màn hình kiến trúc & monitoring
│   ├── container.png, eureka.png, kafka-cluster.png
│   ├── keycloak.png, prometheus.png, zipkin.png
│   └── giaodien_web.png
├── 📁 markdown_requirements/             ← Đặc tả yêu cầu Markdown cho từng service
│   ├── api-gateway.md
│   ├── discovery-server.md
│   ├── notification-service.md
│   ├── order-service.md
│   └── product-service.md
├── 📁 PDF_requirements/                  ← Đặc tả yêu cầu PDF cho từng service
│   ├── discovery-service.pdf
│   ├── gateway-service.pdf
│   ├── notification-service.pdf
│   ├── Order-Service.pdf
│   └── Product-service.pdf
├── 📁 test_requirements/                 ← Báo cáo kiểm thử kết nối & Docker
│   ├── test_results.md
│   ├── notification-service-test-report.md
│   ├── order-service-docker-test-proof.md
│   ├── order-service-test-proof.md
│   ├── product-service-docker-live-test.md
│   └── product-service-test-report.md
├── 📁 microservices_api_demo/            ← Cụm demo microservices (HD Bank)
│   ├── docker-compose.yml               (269 dòng – Kafka, Redis, PostgreSQL, Keycloak, 6 services)
│   ├── api-gateway/, discovery-server/
│   ├── product-service/, order-service/
│   ├── inventory-service/, notification-service/
│   ├── init-databases.sh, seed_data.ps1
│   └── README.md
├── 📁 ProjectWeb-BE/                     ← 🔥 BACKEND CHÍNH (production)
│   ├── docker-compose.yml               (248 dòng – 7 services + infra)
│   ├── pom.xml                           (Maven multi-module parent – Spring Boot 3.4.4, Java 21)
│   ├── kubeconfig-ci.yaml
│   ├── .github/workflows/deploy.yml      ← CI/CD pipeline
│   ├── k8s/                              ← Kubernetes deployment manifests
│   ├── api-gateway/, eureka-server/
│   ├── user-service/, product-service/
│   ├── order-service/, notification-service/
│   └── payment-service/
└── 📁 ProjectWeb-main/                   ← 🔥 FRONTEND CHÍNH (production)
    ├── FE/react-e-commerce/              ← React 18 + Vite + Tailwind CSS
    │   ├── Dockerfile, docker-compose.yml
    │   ├── package.json, vite.config.js
    │   └── src/
    │       ├── components/               (Admin, Cart, Delivery, Home, NavBar, Payment...)
    │       ├── store/                    (Zustand: products, orders, modal, auth)
    │       ├── views/                    (HomeView, CartView, AdminView, DeliveryView...)
    │       └── helpers/
    └── README.md
```

---

## 🏗️ 1. Kiến Trúc Hệ Thống

Dự án được xây dựng dựa trên **4 lớp kiến trúc cốt lõi**:

| Lớp | Tên | Công nghệ | Mô tả |
| :--- | :--- | :--- | :--- |
| **1** | **Experience Layer** | React 18 + Vite + Tailwind CSS | Giao diện người dùng tương tác qua REST API |
| **2** | **Gateway Layer** | Spring Cloud Gateway | Định tuyến, CORS, OAuth2, caching filter |
| **3** | **Service Layer** | Spring Boot 3.4.4 (Java 21) | 7 microservices độc lập |
| **4** | **Infrastructure Layer** | Kafka, Redis, MongoDB, Keycloak, Zipkin, Prometheus | Messaging, Cache, Storage, Identity, Observability |

### Sơ đồ giao tiếp tổng quan

```
[React Frontend] ──► [API Gateway :8181] ──► [Eureka :8761] (Service Discovery)
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
   [User Service]     [Product Service]    [Order Service]
     :8081                  :8082               :8083
   MongoDB                MongoDB              MongoDB
   Redis Cache            Redis Cache          Redis Cache
                                                    │
                                          Kafka Producer
                                                    │
                                                    ▼
                                     ┌────────────────────┐
                                     │   Kafka Cluster    │
                                     │   (3-node KRaft)   │
                                     └────────────────────┘
                                                    │
                                                    ▼
                                         [Notification Service]
                                                 :8084
                                          Kafka Consumer → Email

[Payment Service :8085] ──► VNPay Integration
```

---

## 🧱 2. Danh Sách Microservices

### ProjectWeb-BE (Production Backend)

| # | Service | Port | Database | Trách nhiệm chính | Kafka Role |
| :-: | :--- | :---: | :--- | :--- | :---: |
| 1 | **Eureka Server** | 8761 | - | Service Discovery & Registry | - |
| 2 | **API Gateway** | 8181 | - | Định tuyến, CORS, OAuth2, Caching | - |
| 3 | **User Service** | 8081 | MongoDB | Quản lý User, JWT, Redis cache | - |
| 4 | **Product Service** | 8082 | MongoDB | CRUD Product, Redis cache | - |
| 5 | **Order Service** | 8083 | MongoDB | Đặt hàng, gọi Product qua Feign client | **Producer** |
| 6 | **Notification Service** | 8084 | - | Lắng nghe sự kiện đặt hàng, gửi Email | **Consumer** |
| 7 | **Payment Service** | 8085 | - | Tích hợp cổng thanh toán VNPay | - |

### Cấu trúc code mỗi service (Pattern: controller → service → repository)

```
<service-name>/
├── Dockerfile
├── pom.xml
└── src/main/java/vn/tt/practice/<service>/
    ├── <Service>Application.java
    ├── controller/          ← REST endpoints
    ├── service/             ← Business logic
    ├── repository/          ← Data access (MongoRepository)
    ├── model/               ← Entity classes
    ├── dto/                 ← Data Transfer Objects
    ├── mapper/              ← Entity ↔ DTO mapping
    ├── config/              ← SecurityConfig, RedisConfig, KafkaConfig, FeignClient
    ├── producer/            ← Kafka producer (Order Service)
    └── consumer/            ← Kafka consumer (Notification Service)
```

### microservices_api_demo (Alternative Demo with Keycloak)

Cụm demo bổ sung hỗ trợ các tính năng nâng cao:
- **Keycloak** (port 8180): Identity provider với OAuth2/OIDC + RBAC
- **Inventory Service**: Quản lý tồn kho, tích hợp với Order Service
- **PostgreSQL**: Lưu trữ cho Order, Inventory và Keycloak
- **Kafka UI** (port 8080): Giao diện giám sát Kafka messages

---

## 🔐 3. Bảo Mật & Phân Quyền (Security & RBAC)

Hệ thống sử dụng **Keycloak** kết hợp với **Spring Security**:

| Cơ chế | Mô tả |
| :--- | :--- |
| **OAuth2 & OpenID Connect** | Chuẩn bảo mật hiện đại, ủy quyền phân tán |
| **JWT (JSON Web Token)** | Token chứa thông tin user + roles, không lưu session |
| **RBAC** | `ROLE_ADMIN`: quản lý sản phẩm, đơn hàng, kho | `ROLE_CUSTOMER`: xem + mua hàng của chính mình |
| **Stateless** | Service không lưu session → scale-out dễ dàng |
| **Spring Security** | Cấu hình trên từng service và tại API Gateway |

---

## 💾 4. Thiết Kế Dữ Liệu (Database-per-service)

| Database | Service sử dụng | Lý do lựa chọn |
| :--- | :--- | :--- |
| **MongoDB** (NoSQL) | Product, User, Order | Schema-less – linh hoạt cho thuộc tính sản phẩm đa dạng |
| **PostgreSQL** (SQL) | Order, Inventory, Keycloak | ACID – đảm bảo toàn vẹn giao dịch thanh toán, tồn kho |
| **Redis** | User, Product, Order | Cache phân tán – tăng tốc độ truy xuất dữ liệu nóng |

---

## 📨 5. Event-Driven Architecture với Kafka

Hệ thống sử dụng **Kafka 3-node KRaft cluster** (không cần Zookeeper) với Kafka UI để giám sát.

### Flow đặt hàng (Order Flow):

```
[User] → POST /api/order → [Order Service]
    │
    ├── 1. Kiểm tra sản phẩm qua Feign → [Product Service]
    ├── 2. Lưu đơn hàng vào MongoDB
    └── 3. Bắn sự kiện "OrderCreatedEvent" → [Kafka: order-events topic]
                                                         │
                                              ┌──────────┴──────────┐
                                              ▼                     ▼
                                    [Notification Service]   [Inventory Service]
                                        ↓ Consumer               ↓ Consumer
                                      Gửi Email              Trừ tồn kho
```

**Lợi ích:** Nếu Email Service bị chậm, người dùng vẫn thấy "Đặt hàng thành công" ngay lập tức. Các tác vụ phụ được xử lý bất đồng bộ qua Kafka.

---

## ⚙️ 6. CI/CD Pipeline (GitHub Actions)

**Workflow file:** `.github/workflows/deploy.yml`  
**Trigger:** Push lên nhánh `BE`  
**Runtime:** `ubuntu-latest`, Java 21 (Temurin)

| Bước | Mô tả | Công cụ |
| :---: | :--- | :--- |
| 1 | **Detect Changes** | `git diff HEAD^ HEAD` – phát hiện chính xác service nào thay đổi |
| 2 | **Build** | `mvn clean package -DskipTests` – đóng gói .jar |
| 3 | **Dockerize** | `docker build -t <user>/<service>:latest` → `docker push` |
| 4 | **Deploy** | `kubectl apply -f k8s/<service>-deployment.yaml` → `kubectl rollout status` |

### K8s Deployment Manifests (7 files trong `k8s/`):

```
ProjectWeb-BE/k8s/
├── api-gateway-deployment.yaml
├── eureka-server-deployment.yaml
├── user-service-deployment.yaml
├── product-service-deployment.yaml
├── order-service-deployment.yaml
├── notification-service-deployment.yaml
└── payment-service-deployment.yaml
```

---

## 🖥️ 7. Frontend (React E-Commerce)

| Công nghệ | Mục đích |
| :--- | :--- |
| **React 18** | UI framework |
| **Vite 5** | Build tool (nhanh hơn Webpack) |
| **Tailwind CSS 3** | Utility-first CSS |
| **React Router DOM 6** | Client-side routing |
| **Zustand** | State management (products, orders, modal, auth) |
| **Headless UI** | Accessible UI components |
| **React Toastify** | Toast notifications |
| **React Paginate** | Phân trang sản phẩm |

### Các trang chính:

| Route | Component | Mô tả |
| :--- | :--- | :--- |
| `/` | `HomeView` | Trang chủ, banner, danh sách sản phẩm, filter |
| `/cart` | `CartView` | Giỏ hàng & order summary |
| `/delivery` | `DeliveryView` | Theo dõi đơn hàng |
| `/admin` | `AdminView` | Quản lý Users, Products, Orders (chỉ Admin) |
| `/payment/*` | `PaymentResult` | Kết quả thanh toán VNPay |

---

## 🚀 8. Hướng Dẫn Chạy Toàn Hệ Thống

### Yêu cầu hệ thống
- Docker & Docker Compose
- Java 21 (nếu build local)
- Maven 3.9+ (nếu build local)

### Bước 1: Tạo network chung

```bash
docker network create app-network
```

### Bước 2: Khởi động Backend (tất cả infrastructure + 7 services)

```bash
cd "Week8 - Vibe Engineering/ProjectWeb-BE"
docker compose up -d
```

Các container sẽ được khởi động theo thứ tự phụ thuộc (depend_on):
```
mongo, redis, prometheus, zipkin
  → kafka-1, kafka-2, kafka-3
    → kafka-ui, eureka-server
      → user-service, product-service
        → order-service, notification-service, payment-service
          → api-gateway
```

### Bước 3: Khởi động Frontend

```bash
cd "Week8 - Vibe Engineering/ProjectWeb-main/FE/react-e-commerce"
docker compose up --build -d
```

### Bước 4: Kiểm tra trạng thái

Theo dõi Eureka Dashboard tại `http://localhost:8761` – tất cả service phải hiển thị status `UP`.

---

## 🔗 9. Danh Sách URL Truy Cập

| Service | URL | Chức năng | Tài khoản |
| :--- | :--- | :--- | :--- |
| **Website (User)** | http://localhost:5173 | Mua hàng & giao diện | (Đăng ký mới) |
| **Eureka Dashboard** | http://localhost:8761 | Service Registry | - |
| **Kafka UI** | http://localhost:8080 | Giám sát Kafka Topics/Messages | - |
| **Keycloak Admin** | http://localhost:8180 | Quản lý Users & Roles | `admin` / `admin` |
| **Zipkin** | http://localhost:9411 | Distributed Tracing | - |
| **Prometheus** | http://localhost:9090 | Metrics & Monitoring | - |

> ⚠️ Kafka UI và Keycloak chỉ khả dụng khi chạy cụm `microservices_api_demo/` (có Keycloak + Kafka UI trong docker-compose).

---

## 🧪 10. Kiểm Thử Hệ Thống

Thư mục `test_requirements/` chứa các báo cáo kiểm thử:

| Báo cáo | Nội dung |
| :--- | :--- |
| `test_results.md` | Kiểm thử kết nối Eureka, Gateway routing, Actuator health |
| `product-service-test-report.md` | Test CRUD Product API |
| `product-service-docker-live-test.md` | Docker live test Product Service |
| `order-service-test-proof.md` | Test đặt hàng + Kafka event |
| `order-service-docker-test-proof.md` | Docker live test Order Service |
| `notification-service-test-report.md` | Test Kafka consumer + Email |

### Kết quả kiểm thử tổng quan:

| Thành phần | Trạng thái |
| :--- | :---: |
| Eureka Server | UP |
| API Gateway (Discovery-aware routing) | UP |
| Product Service (CRUD + Docker) | UP |
| Order Service (Kafka Producer + Docker) | UP |
| Notification Service (Kafka Consumer) | UP |
| Inventory Service (Microservices API Demo) | UP |

---

## 📚 11. Tài Liệu Đi Kèm

| Vị trí | Định dạng | Nội dung |
| :--- | :---: | :--- |
| `docs/A_discorvery_service.docx` | Word | Kiến trúc Eureka Discovery Server |
| `docs/B_api_gateway.docx` | Word | Kiến trúc API Gateway |
| `docs/C, E_Product&Notification.docx` | Word | Kiến trúc Product + Notification |
| `docs/D_OrderServices.docx` | Word | Kiến trúc Order Service |
| `docs/Báo cáo tổng.docx` | Word | Báo cáo tổng hợp toàn bộ dự án |
| `markdown_requirements/` | Markdown | Đặc tả yêu cầu từng service |
| `PDF_requirements/` | PDF | Đặc tả yêu cầu từng service |
| `image/` | PNG | Screenshots kiến trúc & monitoring |

---

## 🔭 12. Định Hướng Phát Triển

- [ ] **ELK Stack:** Tích hợp Elasticsearch, Logstash, Kibana để quản lý Log tập trung
- [ ] **Service Mesh (Istio):** Tăng cường bảo mật và quản lý traffic nâng cao trong Kubernetes
- [ ] **Mobile App:** Phát triển ứng dụng Flutter/React Native dùng chung API Gateway
- [ ] **API Rate Limiting:** Tích hợp rate limiting tại API Gateway
- [ ] **GraphQL Gateway:** Hỗ trợ GraphQL endpoint tại Gateway cho frontend

---

## 🛠️ 13. Tổng Hợp Tech Stack

| Hạng mục | Công nghệ |
| :--- | :--- |
| **Ngôn ngữ** | Java 21, JavaScript (React) |
| **Framework Backend** | Spring Boot 3.4.4, Spring Cloud Gateway, Spring Security |
| **Service Discovery** | Netflix Eureka |
| **Database** | MongoDB, PostgreSQL |
| **Cache** | Redis (Lettuce client) |
| **Messaging** | Apache Kafka (KRaft, 3-node cluster) |
| **Identity** | Keycloak (OAuth2 / OIDC) |
| **Inter-service Call** | OpenFeign |
| **Observability** | Micrometer, Zipkin (tracing), Prometheus (metrics) |
| **Containerization** | Docker, Docker Compose |
| **Orchestration** | Kubernetes |
| **CI/CD** | GitHub Actions (detect → build → push → deploy) |
| **Frontend** | React 18, Vite 5, Tailwind CSS 3, Zustand, React Router 6 |
| **Build Tool** | Maven (multi-module), Vite |
| **Testing** | JUnit, Testcontainers, REST Assured |

---

*Seminar chuyên đề Week 8 – Vibe Engineering. Thiết kế bởi sự đam mê kiến trúc Microservices hiện đại!*
