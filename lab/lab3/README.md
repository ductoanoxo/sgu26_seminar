Dưới đây là bản tóm tắt đi sâu vào từng chi tiết, giải thích rõ các cơ chế, phím tắt và ví dụ thực hành được đề cập trong **Chương 3: A Guide to GitHub Copilot with PyCharm, VS Code, and Jupyter Notebook**:

**1. Kiến trúc và Cách thức hoạt động của GitHub Copilot**
*   **Luồng xử lý (Flowchart):** Khác với việc chỉ dùng chữ ký hàm đơn giản, Copilot thu thập ngữ cảnh rộng lớn hơn nhiều. Khi bạn viết mã, Copilot sẽ thu thập: (1) Mã nguồn xung quanh con trỏ chuột, (2) Các tệp mở gần đây, (3) Lịch sử và thông tin Git.
*   **Xử lý Lời nhắc (Prompt):** Tất cả thông tin trên được tổ hợp thành "system prompts" (hướng dẫn hệ thống) và "user prompts" (lời nhắc người dùng), sau đó gửi đến LLM.
*   **Hậu kỳ (Post-processing):** Đầu ra từ LLM không được hiển thị ngay mà phải qua bước xử lý hậu kỳ để đảm bảo mã đề xuất có thể biên dịch thành công. Mọi người thường lầm tưởng Copilot gửi toàn bộ repository cho LLM, nhưng thực tế nó chỉ gửi các đoạn mã liên quan để tiết kiệm chi phí và giữ tốc độ phản hồi nhanh.

**2. Chính sách, Quyền riêng tư và Chi phí**
*   **Chi phí cụ thể:** 
    *   Cá nhân (Individual): 10 USD/tháng hoặc 100 USD/năm.
    *   Doanh nghiệp (Business/Enterprise): 19 USD/người/tháng hoặc 39 USD/người/tháng.
    *   Miễn phí: Dành cho sinh viên, giảng viên và những người bảo trì dự án mã nguồn mở phổ biến.
*   **Quyền riêng tư:** Bạn có quyền bật/tắt tính năng **"Suggestions matching public code"** (cho phép gợi ý mã trùng khớp với mã công khai trên GitHub) để tránh rủi ro bản quyền. Bạn cũng có thể từ chối cho phép GitHub sử dụng dữ liệu của bạn để huấn luyện mô hình.

**3. Cài đặt chi tiết trên IDE**
*   **Mức độ tích hợp:** Copilot được tích hợp sâu hơn trên VS Code. Các tính năng mới (như hỗ trợ Jupyter Notebook hoặc cập nhật LLM mới) thường có mặt trên VS Code trước PyCharm.
*   **Cách cài đặt:**
    *   *PyCharm:* Vào `Settings | Plugins | Marketplace`, tìm "GitHub Copilot", cài đặt, khởi động lại IDE và đăng nhập GitHub. Trạng thái hoạt động hiển thị chữ "Ready" ở góc dưới.
    *   *VS Code:* Vào phần `Extensions`, tìm "GitHub Copilot" (nó sẽ tự động cài thêm tiện ích Copilot Chat), đăng nhập và cấp quyền.

**4. Ba chế độ tương tác chuyên sâu**
*   **Chat:** Giống ChatGPT, dùng để hỏi đáp ngữ cảnh. Bạn có thể mở cửa sổ Chat riêng hoặc Chat ngay trong dòng mã (Inline Chat). Khi hỏi "What can you do?", Copilot sẽ liệt kê các khả năng như: viết mã, giải thích mã, hỗ trợ Git, giải thích terminal.
*   **Completion (Hoàn thành mã):** Chế độ tự động gợi ý mã mờ (ghost text) khi bạn đang gõ, dùng để viết tính năng mới.
*   **Analysis (Phân tích mã):** Làm việc với mã đã có sẵn bằng các lệnh (slash commands) như `/explain` (giải thích), `/fix` (sửa lỗi), `/test` (tạo test).

**5. Phân tích chi tiết các bài Lab**

*   **Lab 3.1 - Tính Trung bình nhân (Chat & Completion):**
    *   *Mục tiêu:* Tính trung bình nhân của 2 số (căn bậc hai của tích 2 số).
    *   *Thực hành:* Bạn dùng khung Chat để hỏi "Explain the geometric mean" (Copilot có thể trả về công thức dạng thô LaTeX bị cắt cụt). Sau đó, bạn chỉ cần gõ chữ ký hàm: `def get_geometric_mean_of_two_numbers(a: float, b: float) -> float:`, Copilot sẽ tự động viết thân hàm: `return pow(a * b, 1 / 2)`. Tiếp tục gõ biến `num1`, `num2` và lệnh `print`, Copilot sẽ tự gọi đúng hàm vừa tạo.

*   **Lab 3.2 - Phím tắt hoàn thành mã (Keyboard Shortcuts):**
    *   *Mục tiêu:* Tính trung bình nhân cho một mảng số thực `*nums`. Để lập trình nhanh với Copilot, bạn bắt buộc phải thuộc các phím tắt.
    *   *Chấp nhận toàn bộ (Accept full):* Nhấn `Tab`.
    *   *Hoàn tác (Undo):* `Ctrl + Z` (hoặc `Cmd + Z`).
    *   *Chấp nhận từng dòng (Accept line):* PyCharm dùng `Ctrl + Alt + Mũi tên phải`. VS Code phải dùng chuột trỏ vào dấu `...` và chọn "Accept Line".
    *   *Chấp nhận từng từ (Accept word):* `Ctrl + Mũi tên phải`.
    *   *Chuyển các gợi ý (Next/Previous):* `Alt + ]` và `Alt + [`.
    *   *Mở danh sách gợi ý (Completions Pane):* Liệt kê tối đa 10 phương án mã khác nhau. PyCharm nhấn `Alt + Enter`, VS Code nhấn `Ctrl + Enter`.

*   **Lab 3.3 - Phân tích mã, sửa lỗi và cửa sổ Edits:**
    *   *Cửa sổ Edits (VS Code):* Đây là tính năng mạnh mẽ cho phép làm việc trên nhiều tệp cùng lúc. Bạn có thể bôi đen một đoạn mã, gọi biến `#selection` và yêu cầu "thêm xác thực kiểu dữ liệu cho đầu vào float". Copilot sẽ hiển thị giao diện so sánh (diff) trực quan để bạn duyệt (Accept) hoặc hủy (Discard).
    *   *Sửa lỗi (`/fix`):* Giả sử hàm tính trung bình nhân của 3 số (`a, b, c`) đang bị viết sai thành tính căn bậc hai `**(1/2)`. Bạn bôi đen hàm, mở Inline chat (PyCharm: `Ctrl + Shift + I`, VS Code: `Ctrl + I`) và gõ `/fix`. Copilot sẽ đề xuất sửa thành căn bậc ba `**(1/3)`.
    *   *Giải thích (`/explain`):* Khi yêu cầu giải thích một hàm tính toán phức tạp, Copilot sẽ tách đoạn mã thành 4 bước (kiểm tra mảng rỗng, tính tích, kiểm tra điều kiện số thực, trả về căn bậc n). Tuy nhiên, LLM thỉnh thoảng sẽ bỏ sót hoặc giải thích không trọn vẹn ý nghĩa logic của thuật toán, báo hiệu cho chúng ta biết rằng đoạn mã đó cần được tái cấu trúc (refactor) cho dễ hiểu hơn.