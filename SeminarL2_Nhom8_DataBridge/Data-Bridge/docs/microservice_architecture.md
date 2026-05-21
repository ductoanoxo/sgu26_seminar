# 🏗️ Kiến trúc Hệ thống Microservices - Agent SQL (Cập nhật)

Agent SQL được xây dựng trên nền tảng kiến trúc **Microservices** hiện đại, tối ưu cho việc xử lý dữ liệu bằng AI và cung cấp giao diện Dashboard phân tích mạnh mễ.

---

## 1. Sơ đồ Tổng quan (System Architecture)

Hệ thống sử dụng mô hình **Event-Driven Orchestration** kết hợp với **REST API** để đảm bảo tính thời gian thực và khả năng mở rộng.

```mermaid
graph TD
    %% Clients
    User((Người dùng)) -->|Truy cập| Frontend[🌐 Frontend - Next.js 14]
    
    %% API Gateway Layer
    subgraph "API Gateway (FastAPI)"
        Gateway[🚀 Gateway Orchestrator]
        Auth[🔐 Auth Layer]
        DashSvc[📊 Dashboard Service]
        ResponseConsumer[📥 Kafka Consumer]
    end
    
    Frontend -->|REST API| Gateway
    Gateway --> Auth
    
    %% Messaging Layer
    subgraph "Message Broker (Kafka)"
        Kafka[📨 Kafka Broker]
        NL_Req(nl2sql.requests)
        NL_Res(nl2sql.responses)
        Q_Req(query.requests)
        Q_Res(query.responses)
    end
    
    Gateway -->|Publish| NL_Req
    Gateway -->|Publish| Q_Req
    ResponseConsumer <--|Subscribe| NL_Res
    ResponseConsumer <--|Subscribe| Q_Res
    
    %% Microservices
    subgraph "NL2SQL Service (AI Engine)"
        NL_Worker[👷 Kafka Worker]
        Agents[🧠 Multi-Agent Pipeline]
    end
    NL_Worker <--|Listen| NL_Req
    NL_Worker -->|Reply| NL_Res
    NL_Worker --> Agents
    
    subgraph "Query Service (Data Engine)"
        Q_Worker[👷 Kafka Worker]
        Executor[🗄️ SQL Executor]
    end
    Q_Worker <--|Listen| Q_Req
    Q_Worker -->|Reply| Q_Res
    Q_Worker --> Executor
    DashSvc -->|Sync REST| Executor
    
    %% Storage
    LLM[🤖 LLM Providers] <--> Agents
    Executor -->|PostgreSQL| Supabase[(🗄️ Supabase DB)]
```

---

## 2. Chi tiết các Thành phần

### 🚀 1. API Gateway (The Orchestrator)
- **Công nghệ**: FastAPI, Python.
- **Vai trò**:
    - **Authentication**: Định danh người dùng qua lớp `core.auth`, hỗ trợ quản lý Dashboard theo từng User.
    - **Dashboard Management**: Cung cấp API CRUD cho Dashboard và Widget. Có cơ chế **Parallel Refresh** (làm mới nhiều widget cùng lúc qua REST đến Query Service).
    - **Async Communication**: Sử dụng `correlation_id` để điều phối các yêu cầu bất đồng bộ qua Kafka.

### 🧠 2. NL2SQL Service (The AI Brain)
- **Công nghệ**: CrewAI / LangChain, Google Gemini, OpenRouter.
- **Vai trò**:
    - **Multi-Agent Pipeline**: Chia nhỏ nhiệm vụ cho các Agent:
        - *Schema Analyst*: Phân tích cấu trúc DB.
        - *SQL Generator*: Viết câu lệnh SQL.
        - *Explainer*: Giải thích kết quả.
    - **Intermediate Tracking**: Theo dõi chi tiết từng bước xử lý của Agent để debug và tối ưu Prompt.

### 🗄️ 3. Query Service (The Data Engine)
- **Công nghệ**: Psycopg2, Connection Pooling.
- **Vai trò**:
    - **Dual Interface**: 
        - Nhận yêu cầu từ Kafka cho luồng chat AI.
        - Cung cấp REST Endpoint (`/execute`) cho luồng Dashboard refresh tốc độ cao.
    - **Security**: Kiểm soát an toàn SQL và giới hạn dữ liệu (Truncation) để tránh quá tải.

### 🌐 4. Frontend Dashboard
- **Công nghệ**: Next.js 14 (App Router), TailwindCSS, Chart.js.
- **Tính năng**:
    - **AI Chat**: Giao tiếp tự nhiên với Database.
    - **Dynamic Dashboard**: Người dùng tự tạo Dashboard, thêm Widget và chọn kiểu hiển thị (Table, Chart, Stat).
    - **SQL Preview**: Xem và chỉnh sửa SQL trước khi thực thi.

---

## 3. Cơ chế Giao tiếp & Luồng dữ liệu

Hệ thống kết hợp linh hoạt 2 cơ chế:

1.  **Luồng Chat (Bất đồng bộ qua Kafka)**:
    - Phù hợp cho các tác vụ AI tốn thời gian. Gateway gửi request vào topic, Agent xử ly xong trả kết quả vào topic response. Gateway Consumer nhận kết quả và giải phóng `Future` cho Frontend.

2.  **Luồng Dashboard (Đồng bộ qua REST)**:
    - Khi người dùng mở Dashboard, Gateway gọi trực tiếp Query Service qua HTTP. Điều này giúp giảm độ trễ (latency) và tận dụng khả năng xử lý song song (Parallel execution) của FastAPI.

---

## 4. Hạ tầng (Infrastructure)

- **Kafka**: Đóng vai trò xương sống cho việc điều phối Agent. Sử dụng chế độ KRaft (không cần Zookeeper).
- **Supabase**: Cơ sở dữ liệu PostgreSQL chính, kết nối qua Connection Pooler để tối ưu hiệu năng.
- **Docker Network**: Các service nội bộ giao tiếp trong mạng cô lập, chỉ Gateway và Frontend mở port ra bên ngoài.
