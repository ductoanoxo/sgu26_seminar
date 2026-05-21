# User Story và Bối cảnh Dự án Agent SQL

## Bối cảnh
Doanh nghiệp/nhóm phân tích muốn khai thác dữ liệu nhưng không có kỹ năng truy vấn (SQL/NoSQL) hoặc không muốn viết code thủ công. Hệ thống cần hỗ trợ kết nối đa dạng nguồn dữ liệu (SQL và NoSQL) thông qua hai hình thức:
1. Import file trực tiếp.
2. Kết nối bằng Connection String.
Hệ thống sẽ chuyển đổi ngôn ngữ tự nhiên sang các câu truy vấn an toàn, thực thi và hiển thị kết quả nhanh trên giao diện web.

Các yêu cầu chính:
- Chỉ cho phép truy vấn đọc (SELECT/CTE), không DDL/DML.
- Bảo mật kết nối DB, giới hạn thời gian và số dòng trả về.
- Giao diện đơn giản, hỗ trợ hiểu về schema và kết quả.
- Mở rộng được cho các đơn vị/nhóm khác nhau.

## Đối tượng người dùng cốt lõi (Personas)

Để tối ưu hóa trải nghiệm, hệ thống tập trung phục vụ 2 nhóm người dùng thực sự cần thiết nhất:

1) **Người dùng cuối (End-User: Business, PM, Data Analyst)**
- **Đặc điểm:** Không rành SQL hoặc muốn tiết kiệm thời gian viết code.
- **Mục tiêu:** Đặt câu hỏi bằng ngôn ngữ tự nhiên, xem SQL được giải thích rõ ràng, nhận dữ liệu/biểu đồ nhanh chóng và chia sẻ cho team.

2) **Quản trị viên Hệ thống (Admin: DBA, Data Engineer)**
- **Đặc điểm:** Người thiết lập hệ thống và bảo vệ dữ liệu.
- **Mục tiêu:** Cung cấp nguồn dữ liệu an toàn, kiểm soát chặt chẽ các truy vấn (chặn DML/DDL, chống quá tải) để không ảnh hưởng đến Database gốc.

## Câu chuyện người dùng (User Stories)

### 1. Dành cho Người dùng cuối

- **US1 - Truy vấn tự nhiên:** Là người dùng cuối, tôi muốn nhập câu hỏi bằng ngôn ngữ tự nhiên để nhận lại kết quả dạng bảng, giúp tôi ra quyết định nhanh mà không cần nhờ IT.
  - *Tiêu chí:* Hệ thống nhận diện chuẩn xác bảng/cột từ schema để sinh truy vấn.

- **US2 - Hiểu & Trực quan hóa:** Là người dùng cuối, tôi muốn xem lời giải thích câu lệnh SQL bằng tiếng Việt và chuyển đổi dữ liệu sang dạng biểu đồ để dễ dàng kiểm chứng và báo cáo.
  - *Tiêu chí:* Có box giải thích SQL rõ ràng, hỗ trợ vẽ biểu đồ cơ bản (Line, Bar, Pie).

- **US3 - Lịch sử & Chia sẻ:** Là người dùng cuối, tôi muốn xem lại các câu hỏi cũ trong lịch sử và chia sẻ kết quả cho đồng nghiệp.
  - *Tiêu chí:* Lưu lại bộ nhớ ngữ cảnh hội thoại, có tính năng copy kết quả/chia sẻ.

### 2. Dành cho Quản trị viên

- **US4 - Bảo vệ Database gốc:** Là quản trị viên, tôi muốn hệ thống tự động chặn mọi câu lệnh thay đổi dữ liệu (INSERT/UPDATE/DELETE/DROP) và chỉ cho phép lệnh đọc (SELECT/CTE) an toàn.
  - *Tiêu chí:* Cơ chế chặn (filter) hoạt động ở tầng logic trước khi chạm tới Database.

- **US5 - Kiểm soát tài nguyên:** Là quản trị viên, tôi muốn hệ thống giới hạn thời gian thực thi (timeout) và số lượng dòng trả về (limit) để chống treo server hoặc lộ quá nhiều dữ liệu.
  - *Tiêu chí:* Tự động ép thêm `LIMIT` vào SQL và áp dụng timeout cho mọi request.

## Phạm vi không bao gồm (Out of scope)
- Tự động ghi/ghi đè lên DB (INSERT/UPDATE/DELETE).
- Quản lý phân quyền người dùng chi tiết (nếu chưa có Auth/RLS đầy đủ).

## Giá trị mang lại
- Giảm thời gian từ câu hỏi đến kết quả.
- Giảm lỗi viết SQL và giảm rủi ro bảo mật.
- Nâng cao khả năng tự phục vụ dữ liệu cho nhóm không chuyên.

## III. Phân bổ Nghiệp vụ Toàn Hệ thống (Full-stack) và AI Agent phụ trách

Dưới đây là bảng phân bổ các nhóm nghiệp vụ chính trong toàn bộ hệ thống (Frontend, Backend, Database, DevOps, QA) và AI Agent tương ứng chịu trách nhiệm thiết kế, xử lý hoặc hỗ trợ:

| Nhóm Nghiệp vụ | Chi tiết User Story / Yêu cầu Hệ thống | AI Agent phụ trách chính |
| :--- | :--- | :--- |
| **1. Kết nối & Trích xuất Metadata** | Là người dùng, tôi muốn kết nối Database hoặc tải file lên để hệ thống tự động trích xuất cấu trúc (schema) chuẩn xác. | **SQL Agent**: Phân tích schema, hiểu ngữ cảnh dữ liệu và thiết lập metadata. |
| **2. Chuyển đổi NL2SQL (Core Engine)** | Là người dùng nghiệp vụ, tôi muốn nhập câu hỏi tự nhiên để nhận lại dữ liệu chính xác mà không cần biết code SQL. | **SQL Agent**: Nhận diện ý định (intent), ánh xạ schema và sinh mã SQL an toàn (Chỉ SELECT/CTE). |
| **3. Giải thích & Tối ưu SQL** | Là nhà phân tích dữ liệu, tôi muốn xem câu lệnh SQL được tạo ra kèm theo lời giải thích chi tiết bằng tiếng Việt để dễ dàng kiểm chứng. | **SQL Agent**: Dịch ngược SQL sang ngôn ngữ tự nhiên, gợi ý cách tối ưu truy vấn. |
| **4. Kiểm soát An toàn Truy vấn** | Hệ thống (Backend/DBA) cần tự động chặn các lệnh DDL/DML, giới hạn tài nguyên (timeout, limit rows) để bảo vệ DB. | **SQL Agent**: Lọc và validate SQL trước khi thực thi. **DevOps Agent**: Theo dõi tải database. |
| **5. Trực quan hóa Dữ liệu (Frontend)**| Là người dùng, tôi muốn xem kết quả dưới dạng bảng hoặc biểu đồ động để phân tích xu hướng nhanh chóng. | **SQL Agent**: Gợi ý loại biểu đồ phù hợp. **QA Agent**: Kiểm thử hiển thị UI/UX. |
| **6. Lịch sử & Chia sẻ Truy vấn** | Là trưởng nhóm, tôi muốn lưu lại các truy vấn hay dùng và chia sẻ kết quả cho thành viên khác trong team. | **SQL Agent**: Quản lý lịch sử hội thoại và bộ nhớ ngữ cảnh (Context memory). |
| **7. Triển khai & Quản lý Hạ tầng** | (Nội bộ) Hệ thống cần được đóng gói (Docker), tự động build và deploy (CI/CD pipeline) trơn tru lên server. | **DevOps Agent**: Viết Dockerfile, cấu hình Jenkins pipeline, quản lý môi trường và cloud. |
| **8. Giám sát Hiệu năng (Observability)**| (Nội bộ) Cần theo dõi uptime, thời gian phản hồi API và nhận cảnh báo (Telegram) khi hệ thống gặp sự cố. | **DevOps Agent**: Cấu hình Grafana/Prometheus/Alloy, thiết lập cảnh báo ChatOps. |
| **9. Kiểm thử Toàn diện (QA Automation)**| (Nội bộ) Mọi tính năng từ API backend đến luồng thao tác UI frontend đều phải được test tự động trước khi release. | **QA Agent**: Sinh test case, chạy API Integration Test, Load Test (k6), và Playwright (UI). |
