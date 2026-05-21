# Cập nhật User Story và Phân bổ AI Agent

Kế hoạch này nhằm bổ sung chi tiết các chức năng giao diện (Frontend) và xác định rõ AI Agent nào sẽ chịu trách nhiệm chính trong việc xử lý, kiểm thử hoặc triển khai tính năng đó.

## Mục tiêu
1.  Chi tiết hóa các tính năng trên Frontend.
2.  Gắn User Story cho từng tính năng.
3.  Xác định AI Agent phụ trách (SQL Agent, QA Agent, DevOps Agent).

## Đề xuất thay đổi

### [MODIFY] [user_story.md](file:///home/traductoan/Seminar_Final/docs/user_story.md)
Bổ sung mục **"III. Chức năng Frontend và AI Agent phụ trách"** vào sau phần User Story hiện tại.

#### Nội dung bổ sung dự kiến:

| Chức năng Frontend | User Story | AI Agent phụ trách |
| :--- | :--- | :--- |
| **Kết nối Dữ liệu (Connect Modal)** | Là người dùng, tôi muốn nhập Connection String hoặc tải file CSV/JSON để Agent có thể học cấu trúc dữ liệu. | **SQL Agent**: Đọc và phân tích schema/metadata từ nguồn dữ liệu. |
| **Khung nhập Truy vấn (Query Input)** | Là người dùng nghiệp vụ, tôi muốn nhập câu hỏi tự nhiên để nhận lại kết quả mà không cần viết SQL. | **SQL Agent**: Chuyển đổi NL sang SQL (Core LLM Logic). |
| **Xem trước & Giải thích SQL** | Là người dùng, tôi muốn xem câu lệnh SQL và giải thích của nó để kiểm tra độ chính xác của Agent. | **SQL Agent**: Tạo giải thích và tối ưu hóa câu lệnh. |
| **Hiển thị Bảng & Biểu đồ** | Là người dùng, tôi muốn xem kết quả dạng bảng và biểu đồ tự động để dễ dàng phân tích xu hướng. | **SQL Agent**: Xử lý dữ liệu đầu ra; **QA Agent**: Kiểm thử hiển thị UI/UX. |
| **Lịch sử & Thư viện Truy vấn** | Là người dùng, tôi muốn xem lại các câu hỏi cũ và kết quả để tiết kiệm thời gian. | **SQL Agent**: Quản lý ngữ cảnh và lưu trữ truy vấn. |
| **Giám sát & Bảo mật (Admin View)** | Là DBA, tôi muốn theo dõi các truy vấn đang chạy và chặn các lệnh nguy hiểm. | **DevOps Agent**: Giám sát hiệu năng; **SQL Agent**: Thực thi chính sách bảo mật SQL. |
| **Kiểm thử Giao diện Tự động** | (Nội bộ) Hệ thống cần tự động kiểm tra xem các nút bấm và luồng nhập liệu có hoạt động tốt không. | **QA Agent**: Thực thi kịch bản test (Playwright/E2E). |

## Kế hoạch thực hiện
1.  Đọc lại toàn bộ file `user_story.md`.
2.  Chèn bảng phân bổ AI Agent vào cuối file.
3.  Cập nhật thêm các tiêu chí chấp nhận (Acceptance Criteria) liên quan đến Agent.

## Xác minh
-   Kiểm tra xem các chức năng đã bao phủ hết quy trình của dự án chưa.
-   Đảm bảo tên các AI Agent thống nhất với hệ thống hiện tại.
