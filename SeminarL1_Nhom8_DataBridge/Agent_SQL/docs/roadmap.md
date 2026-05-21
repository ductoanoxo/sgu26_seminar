# Lộ trình Phát triển và Tính năng Mở rộng (Agent SQL Roadmap)

## 1. Mục tiêu chiến lược
Nâng cấp hệ thống Agent SQL từ một công cụ chuyển đổi ngôn ngữ tự nhiên thành một **Nền tảng Phân tích Dữ liệu Thông minh (Agentic Data Intelligence Platform)**: an toàn tuyệt đối, trải nghiệm người dùng tối ưu và khả năng cung cấp thông tin chuyên sâu (insights) thay vì chỉ trả về dữ liệu thô.

---

## 2. Các Tính năng Trọng tâm (Core Features)

### 2.1) Tương tác trực tiếp với SQL (SQL Editor & Playground)
*   **Mô tả:** Cho phép người dùng chuyên gia chỉnh sửa trực tiếp câu lệnh SQL mà AI đã tạo, thực thi lại và so sánh kết quả.
*   **Luồng xử lý (Flow):**
    1. AI tạo SQL -> Hiển thị trong Editor có Highlight.
    2. Người dùng sửa SQL -> Hệ thống Validate (SELECT-only) -> Thực thi.
    3. Lưu lịch sử cả bản gốc (AI) và bản chỉnh sửa (Manual).
*   **Yêu cầu:** Vẫn áp dụng nghiêm ngặt các quy tắc bảo mật (Timeout, Row Limit) cho SQL thủ công.
*   **Phạm vi triển khai (ưu tiên P1):**
    1. Editor có highlight, format SQL cơ bản, copy SQL.
    2. Chạy lại SQL thủ công, hiển thị lỗi rõ ràng nhưng không lộ thông tin nhạy cảm.
    3. So sánh nhanh kết quả (row count, thời gian chạy, khác biệt hàng/cột nếu có).
*   **Backend đề xuất:**
    1. API Gateway: thêm endpoint `POST /query/manual` nhận SQL đã chỉnh sửa.
    2. Query Service: tái sử dụng `validate_sql`, chặn multi-statement, chỉ SELECT/CTE.
    3. Lưu lịch sử: lưu `sql_original`, `sql_manual`, `source=ai|manual`, `duration_ms`, `row_count`.
*   **Frontend đề xuất:**
    1. SQL editor component có cảnh báo read-only DB.
    2. Nút Chạy lại và So sánh kết quả.
    3. Hiển thị giới hạn áp dụng (Timeout, Row Limit).
*   **Tiêu chí hoàn thành (DoD):**
    1. SQL thủ công bị chặn nếu không phải SELECT/CTE.
    2. Thực thi trong giới hạn thời gian và số dòng.
    3. Lưu lịch sử cả SQL gốc và SQL chỉnh sửa.
    4. UI hiển thị lỗi thân thiện, không lộ stack trace.
*   **Kiểm thử:**
    1. Unit tests cho validate_sql với các case injection, multi-statement.
    2. Integration tests cho endpoint manual query.
    3. UI test cho editor, chạy lại, và so sánh kết quả.

### 2.2) Dashboard & Widget Tương tác
*   **Mô tả:** Lưu các truy vấn phổ biến thành các biểu đồ (Charts) trên Dashboard cá nhân.
*   **Tính năng:**
    1. Kéo thả widget, thay đổi kiểu biểu đồ (Bar, Line, Pie).
    2. Bộ lọc (Filter) động: Lọc theo thời gian, vùng miền mà không cần viết lại SQL.
    3. Làm mới dữ liệu (Refresh) định kỳ hoặc thủ công.
    4. Tự động tạo dashboard/widget sau mỗi truy vấn thành công (auto-save).
*   **Phạm vi triển khai (ưu tiên P2):**
    1. Dashboard cơ bản với bảng và 1-2 loại biểu đồ.
    2. Lưu cấu hình widget (chart type, mapping trục, format số).
    3. Refresh thủ công trước, sau đó mới đến refresh định kỳ.
    4. Auto-save sau mỗi query, có thể chỉnh sửa lại widget khi cần.
*   **Backend đề xuất:**
    1. API lưu dashboard: `POST /dashboard`, `GET /dashboard/{id}`, `PUT /dashboard/{id}`.
    2. Lưu cấu hình widget: `widgets[]` gồm `sql_source`, `chart_type`, `fields`, `filters`.
    3. Cache kết quả theo `dashboard_id` hoặc `query_fingerprint`.
*   **Frontend đề xuất:**
    1. Trang Dashboard dạng grid, kéo thả widget.
    2. Widget editor để chọn trường dữ liệu và kiểu biểu đồ.
    3. Nút Làm mới và trạng thái tải dữ liệu cho từng widget.
*   **Tiêu chí hoàn thành (DoD):**
    1. Lưu và mở lại dashboard không mất cấu hình.
    2. Widget có thể làm mới dữ liệu theo SQL gốc.
    3. Người dùng thao tác lọc/sắp xếp cơ bản mà không cần viết SQL.
    4. Mỗi truy vấn thành công tự tạo widget và hiển thị ngay trên dashboard.
*   **Kiểm thử:**
    1. Integration tests cho lưu/mở dashboard.
    2. UI tests cho kéo thả, đổi chart, refresh.
    3. Kiểm thử tải nhẹ với 5-10 widget/dashboard.

---

## 3. Tính năng AI Nâng cao (Advanced AI Capabilities)

### 3.1) AI-Powered Data Insights & Narrative (Kể chuyện bằng dữ liệu)
*   **Mô tả:** Thay vì chỉ hiển thị bảng số liệu khô khan, Agent sẽ phân tích kết quả trả về để đưa ra các nhận xét quan trọng (Key Takeaways).
*   **Ví dụ:** Nếu người dùng hỏi về doanh thu, Agent không chỉ hiện bảng mà còn nhận xét: *"Doanh thu tháng này tăng 15%, chủ yếu nhờ vào sự tăng trưởng vượt bậc ở nhóm sản phẩm X."*
*   **Kỹ thuật:** Sau khi có kết quả từ Query Service, gửi một bản tóm tắt dữ liệu (summary stats) quay lại LLM để tạo đoạn mô tả bằng ngôn ngữ tự nhiên.

### 3.2) Multi-turn Conversation & Iterative Refinement (Hội thoại đa bước)
*   **Mô tả:** Cho phép người dùng đặt câu hỏi tiếp nối dựa trên kết quả vừa nhận được mà không cần nhắc lại bối cảnh.
*   **Ví dụ:** 
    *   User: *"Liệt kê 10 khách hàng mua nhiều nhất."*
    *   User: *"Lọc ra những người ở Hà Nội trong danh sách đó."*
    *   User: *"Gửi email cảm ơn cho họ."* (Nếu tích hợp thêm công cụ gửi mail).
*   **Kỹ thuật:** Lưu trữ Conversation Context (bao gồm các câu hỏi trước và SQL đã tạo) vào bộ nhớ (Memory) của Agent để xây dựng các câu truy vấn phức tạp dần bằng CTE.

### 3.3) Semantic Layer & Knowledge Graph (Lớp ngữ nghĩa doanh nghiệp)
*   **Mô tả:** Xây dựng một từ điển thuật ngữ (Glossary) để AI hiểu các khái niệm đặc thù của doanh nghiệp mà DB Schema không thể hiện rõ.
*   **Ví dụ:** Định nghĩa *"Khách hàng tiềm năng"* là khách hàng có trên 3 đơn hàng thành công và tổng chi tiêu > 5 triệu. Khi người dùng hỏi về "khách hàng tiềm năng", AI sẽ tự áp dụng logic này vào SQL.
*   **Kỹ thuật:** Sử dụng Vector Database (như pgvector có sẵn trong Supabase) để lưu trữ tài liệu về Business Logic và thực hiện RAG trước khi tạo SQL.

### 3.4) SQL Performance Self-Optimization (Tự tối ưu hiệu năng)
*   **Mô tả:** Hệ thống tự động phân tích câu lệnh SQL nào chạy chậm và đề xuất cách tối ưu (như thêm Index) hoặc tự động viết lại câu lệnh hiệu quả hơn.
*   **Kỹ thuật:** Sử dụng lệnh `EXPLAIN ANALYZE` trong Postgres. Agent sẽ đọc kết quả phân tích này và đưa ra gợi ý tối ưu hóa cho người dùng hoặc Admin.

### 3.5) Proactive Alerting & Monitoring (Cảnh báo chủ động qua ngôn ngữ tự nhiên)
*   **Mô tả:** Cho phép người dùng thiết lập các cảnh báo bằng câu hỏi tự nhiên.
*   **Ví dụ:** *"Hãy báo cho tôi qua Slack nếu số lượng đơn hàng bị hủy trong ngày vượt quá 10."*
*   **Kỹ thuật:** Tích hợp Supabase Cron hoặc một Worker chạy định kỳ các câu lệnh SQL đã lưu, nếu kết quả thỏa mãn điều kiện sẽ kích hoạt Webhook gửi thông báo.

### 3.6) Federated Querying (Truy vấn đa nguồn dữ liệu)
*   **Mô tả:** Agent có thể kết hợp dữ liệu từ Supabase với các file Excel/CSV người dùng upload lên, hoặc dữ liệu từ các API bên ngoài (Google Sheets, Salesforce).
*   **Kỹ thuật:** Sử dụng DuckDB (một engine OLAP cực nhanh) chạy dưới dạng một worker service để thực hiện join dữ liệu giữa các nguồn khác nhau ngay tại lớp trung gian.

---

## 4. Hạ tầng và Bảo mật (Infra & Security)

### 4.1) Quản trị Dữ liệu & RLS (Supabase Hardening)
*   **Mô tả:** Chuẩn hóa Row Level Security (RLS) để đảm bảo người dùng chỉ thấy dữ liệu họ được phép, ngay cả khi AI tạo ra câu lệnh SQL rộng hơn.
*   **Audit:** Log chi tiết mọi câu lệnh SQL, thời gian thực thi và chi phí Token LLM.

### 4.2) Hiệu năng & Cache
*   **Mô tả:** Cache kết quả theo vân tay câu lệnh (Query Fingerprint). Thêm Async Job Queue cho các truy vấn dữ liệu lớn.
*   **Monitoring:** Triển khai OpenTelemetry để theo dõi vết (tracing) từ Gateway đến NL2SQL và Query Service.

---

## 5. Phân kỳ Triển khai (Implementation Phases)

| Giai đoạn | Trọng tâm | Tính năng chính |
| :--- | :--- | :--- |
| **P1** | **Interactive** | SQL Editor, Chạy lại SQL, Validate nghiêm ngặt. |
| **P2** | **Visual** | Dashboard cơ bản, Export CSV/Excel, Caching kết quả. |
| **P3** | **Agentic** | Hội thoại đa bước, AI Insights, Lớp ngữ nghĩa (Semantic). |
| **P4** | **Enterprise** | Federated Querying, Tự tối ưu hiệu năng, Cảnh báo chủ động. |

---

## 6. Rủi ro và Lưu ý
*   **Chi phí LLM:** Cần cơ chế giới hạn Token và Cache hiệu quả để tránh bùng nổ chi phí khi Dashboard refresh liên tục.
*   **An toàn SQL:** Luôn duy trì nguyên tắc "Chỉ đọc" (Read-only) và chặn mọi từ khóa DDL/DML.
*   **Tải hệ thống:** Giới hạn tần suất refresh dashboard và thiết lập Circuit Breaker cho các truy vấn nặng.
