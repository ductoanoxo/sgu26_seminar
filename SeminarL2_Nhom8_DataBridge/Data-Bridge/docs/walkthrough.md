# Tổng kết cập nhật Đối tượng người dùng & User Story

Tôi đã chỉnh sửa tài liệu User Story, tinh gọn từ 4 đối tượng phân tán xuống còn **2 nhóm người dùng cốt lõi** thực sự cần thiết nhất cho hệ thống.

## Các thay đổi chính trong [user_story.md](file:///home/traductoan/Seminar_Final/docs/user_story.md)

### 1. Gói gọn Đối tượng người dùng (Personas)
- **Người dùng cuối (End-User)**: Gộp chung Nghiệp vụ, Phân tích dữ liệu và Product Manager lại. Nhóm này chỉ quan tâm đến đầu ra: Gõ câu hỏi tự nhiên -> Nhận lại dữ liệu và biểu đồ nhanh chóng.
- **Quản trị viên Hệ thống (Admin)**: Gộp chung DBA và Data Engineer. Nhóm này lo liệu nền tảng: Cung cấp kết nối an toàn và đảm bảo Database không bị "sập" do truy vấn sai.

### 2. Tái cấu trúc User Stories
Các câu chuyện người dùng đã được cô đọng lại thành 5 mục tiêu sát thực tế:

**Dành cho Người dùng cuối:**
- **US1**: Truy vấn tự nhiên (Nhận kết quả bảng).
- **US2**: Hiểu & Trực quan hóa (Xem giải thích SQL và vẽ biểu đồ).
- **US3**: Lịch sử & Chia sẻ (Xem lại câu hỏi cũ và share kết quả).

**Dành cho Quản trị viên:**
- **US4**: Bảo vệ Database gốc (Chặn đứng các lệnh DDL/DML như INSERT, DROP).
- **US5**: Kiểm soát tài nguyên (Giới hạn timeout và ép thêm LIMIT số dòng).

Sự thay đổi này giúp dự án tập trung đúng vào cốt lõi: Làm hài lòng người cần xem dữ liệu (End-User) và làm an tâm người giữ dữ liệu (Admin).
