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

## Đối tượng người dùng (Personas)
1) Người dùng nghiệp vụ
- Không biết SQL, cần xem số liệu nhanh để ra quyết định.

2) Nhà phân tích dữ liệu
- Biết SQL cơ bản, cần tạo báo cáo nhanh từ nhiều bảng.

3) Kỹ sư dữ liệu/DBA
- Quan tâm bảo mật, phân quyền, và chất lượng truy vấn.

4) Trưởng nhóm/Sản phẩm
- Cần theo dõi tổng hợp và chia sẻ kết quả trong nhóm.

## Câu chuyện người dùng
### 1. Truy vấn nhanh bằng ngôn ngữ tự nhiên
- Là người dùng nghiệp vụ, tôi muốn nhập câu hỏi bằng ngôn ngữ tự nhiên để hệ thống tự tạo SQL và trả về kết quả, để tôi có thể ra quyết định nhanh.
- Tiêu chí chấp nhận:
  - Hệ thống chỉ tạo SQL SELECT/CTE.
  - Kết quả trả về trong giới hạn thời gian và số dòng.

### 2. Xem trước SQL và giải thích
- Là nhà phân tích dữ liệu, tôi muốn xem SQL được tạo và giải thích ý nghĩa, để tôi tin tưởng và có thể điều chỉnh câu hỏi.
- Tiêu chí chấp nhận:
  - Hiển thị SQL rõ ràng.
  - Có tóm tắt giải thích bằng ngôn ngữ tự nhiên.

### 3. Kiểm tra schema trước khi tạo SQL
- Là nhà phân tích dữ liệu, tôi muốn hệ thống kiểm tra schema và chỉ dùng bảng/cột tồn tại, để truy vấn không bị lỗi và giảm ảo giác (hallucination).
- Tiêu chí chấp nhận:
  - SQL chỉ sử dụng bảng/cột có trong schema.

### 4. Bảo vệ hệ thống và giới hạn truy vấn
- Là DBA, tôi muốn giới hạn truy vấn và chặn SQL nguy hiểm, để hệ thống an toàn và ổn định.
- Tiêu chí chấp nhận:
  - Từ chối các lệnh không phải SELECT/CTE.
  - Giới hạn thời gian thực thi và số dòng trả về.

### 5. Lưu lịch sử và tái sử dụng truy vấn
- Là trưởng nhóm/sản phẩm, tôi muốn lưu lịch sử và tái sử dụng truy vấn, để nhóm có thể theo dõi và chia sẻ kết quả.
- Tiêu chí chấp nhận:
  - Lưu lịch sử truy vấn và kết quả tổng quan.
  - Cho phép sao chép/chia sẻ liên kết kết quả.

### 6. Báo cáo và biểu đồ
- Là người dùng nghiệp vụ, tôi muốn xem biểu đồ từ kết quả truy vấn, để tôi hiểu xu hướng nhanh.
- Tiêu chí chấp nhận:
  - Hệ thống hỗ trợ chuyển kết quả sang biểu đồ cơ bản.

## Phạm vi không bao gồm (Out of scope)
- Tự động ghi/ghi đè lên DB (INSERT/UPDATE/DELETE).
- Quản lý phân quyền người dùng chi tiết (nếu chưa có Auth/RLS đầy đủ).

## Giá trị mang lại
- Giảm thời gian từ câu hỏi đến kết quả.
- Giảm lỗi viết SQL và giảm rủi ro bảo mật.
- Nâng cao khả năng tự phục vụ dữ liệu cho nhóm không chuyên.
