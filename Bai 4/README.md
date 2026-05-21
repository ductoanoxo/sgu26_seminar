# 🚀 Supercharged Coding with GenAI: Comprehensive Seminar Project

Dự án này là một kho lưu trữ kiến thức và thực hành chuyên sâu về việc tích hợp trí tuệ nhân tạo tạo sinh (Generative AI) vào quy trình phát triển phần mềm hiện đại. Dựa trên giáo trình "Supercharged Coding with Gen-AI", dự án cung cấp lộ trình từ việc hiểu cơ bản về API đến việc làm chủ các kỹ thuật Prompt Engineering nâng cao.

---

## 📋 Mục lục
1. [Giới thiệu tổng quan](#giới-thiệu-tổng-quan)
2. [Cấu trúc chi tiết dự án](#cấu-trúc-chi tiết-dự-án)
3. [Phân tích chuyên sâu các Module Lab](#phân-tích-chuyên-sâu-các-module-lab)
4. [Kỹ thuật Prompt Engineering (5S Framework)](#kỹ-thuật-prompt-engineering-5s-framework)
5. [GitHub Copilot & IDE Integration](#github-copilot--ide-integration)
6. [Mã nguồn tham khảo từ sách](#mã-nguồn-tham-khảo-từ-sách)
7. [Hướng dẫn cài đặt và Bảo mật](#hướng-dẫn-cài-đặt-và-bảo-mật)
8. [Kết quả và Hình ảnh thực tế](#kết-quả-và-hình-ảnh-thực-tế)

---

## 🌟 Giới thiệu tổng quan
Dự án tập trung vào ba trụ cột chính của lập trình với AI:
*   **API Mastery:** Hiểu và tương tác trực tiếp với các mô hình của OpenAI qua Python SDK.
*   **Prompt Engineering:** Kỹ thuật thiết kế lời nhắc có cấu trúc để đạt được độ chính xác 100%.
*   **AI Pair Programming:** Tối ưu hóa hiệu suất làm việc với GitHub Copilot trong các môi trường IDE chuyên nghiệp.

---

## 📂 Cấu trúc chi tiết dự án

### 🛠️ Phần 1: Lab_3122411109_TruongPhuKiet (Thực hành)
Phần này chứa các bài thực hành được cá nhân hóa, minh họa cho từng chương của giáo trình.

| Module | Tên Lab | File chính | Mục tiêu kỹ thuật |
| :--- | :--- | :--- | :--- |
| **Lab 2** | OpenAI API Fundamentals | `lab21.py`, `lab22_multiple.py`, `lab23.py` | Kết nối API, quản lý Token, tinh chỉnh `temperature`, `n`, `max_tokens`. |
| **Lab 3** | GitHub Copilot Workflow | `lab31.py`, `lab32.py`, `lab33.py` | Làm chủ phím tắt, Inline Chat, giải thích và sửa lỗi mã nguồn tự động. |
| **Lab 4** | Prompting Best Practices | `lab41.txt`, `lab42.py` | Áp dụng quy tắc 5S vào ChatGPT để giải quyết các bài toán logic phức tạp. |
| **Lab 5** | Advanced Prompting | `lab51.py`, `lab52.py` | Sử dụng thư viện `inspect` để tự động hóa việc viết Docstrings và Unit Tests. |

### 📖 Phần 2: Supercharged-Coding-with-Gen-AI (Tài liệu gốc)
Mã nguồn bổ trợ cho các chương nâng cao trong sách:
*   **ch7 - Docker & Pandas:** Cách dùng AI để giải thích cấu trúc Dockerfile và debug dữ liệu Pandas.
*   **ch10 - Performance:** Refactoring mã nguồn để tối ưu hóa thời gian chạy và bộ nhớ.
*   **ch13 - Unit Testing:** Tự động tạo dữ liệu kiểm thử (Data-driven testing) với Pytest.
*   **ch14 - Complexity:** Phân tích độ phức tạp thuật toán (Big O) bằng AI.

---

## 🧠 Phân tích chuyên sâu các Module Lab

### 🔹 Lab 2: Làm chủ OpenAI API
*   **`lab21.py`**: Khởi tạo `OpenAI Client`, thực hiện truy vấn cơ bản và **phân tích Token usage**. Việc hiểu Input/Output tokens giúp tối ưu hóa chi phí.
*   **`lab22_multiple.py`**: Thử nghiệm tham số `n=3` (tạo 3 kết quả khác nhau) và `temperature=2` (mức độ sáng tạo cao nhất). Kết quả cho thấy sự biến đổi mạnh mẽ của AI trong việc giải thích thuật toán.
*   **`lab23.py`**: Kỹ thuật **Code Completion qua Chat API**. Sử dụng `System Prompt` để ép buộc AI chỉ trả về code, kết hợp với "Lead-in cue" (`# Complete this code`) trong `User Prompt`.

### 🔹 Lab 5: Tự động hóa với `inspect` và `dunder`
*   **`lab51.py`**: Trình bày một workflow cực kỳ mạnh mẽ:
    1. Dùng `inspect.getsource(method)` để lấy mã nguồn của một hàm Python bất kỳ.
    2. Đóng gói mã nguồn vào một Structured Prompt.
    3. AI tự động sinh ra **Google-style Docstring** dựa trên logic thực tế của code.
*   **`lab52.py`**: Quy trình gỡ lỗi Singleton Pattern:
    - Sử dụng Unit Test để phát hiện lỗi.
    - Dùng lệnh `/fix` của Copilot để tập trung sửa đúng logic khởi tạo instance.

---

## 🎯 Kỹ thuật Prompt Engineering (5S Framework)
Dự án áp dụng triệt để quy tắc **5S** để nâng cao chất lượng đầu ra:
1.  **Structured:** Phân tách rõ ràng `CONTEXT`, `TASK`, `DATA` và `COMPLETION`.
2.  **Surrounding information:** Cung cấp thông tin bối cảnh (Ví dụ: "Bạn là một chuyên gia bảo mật...").
3.  **Single task per prompt:** Không gộp chung việc "giải thích" và "sửa lỗi" trong cùng một lần hỏi.
4.  **Specific instructions:** Sử dụng các chỉ dẫn định lượng (Ví dụ: "Trả về tối đa 5 dòng code", "Chỉ sử dụng thư viện chuẩn").
5.  **Short prompts:** Loại bỏ các từ ngữ thừa, tập trung vào từ khóa hành động.

---

## ⌨️ GitHub Copilot & IDE Integration
Hướng dẫn tối ưu hóa năng suất trên PyCharm và VS Code:
*   **Phím tắt vàng:**
    - `Tab`: Chấp nhận toàn bộ gợi ý.
    - `Alt + ]` / `Alt + [`: Duyệt qua các phương án code khác nhau.
    - `Ctrl + I` (VS Code) / `Ctrl + Shift + I` (PyCharm): Mở Inline Chat.
*   **Slash Commands:**
    - `/explain`: Phân tích logic code phức tạp thành ngôn ngữ tự nhiên.
    - `/fix`: Đề xuất phương án sửa lỗi cho đoạn mã được bôi đen.
    - `/tests`: Tự động viết mã kiểm thử cho hàm hiện tại.

---

## ⚙️ Hướng dẫn cài đặt và Bảo mật

### 1. Yêu cầu hệ thống
*   Python 3.10 trở lên.
*   Tài khoản OpenAI (đã nạp tối thiểu $5 để đạt Tier 1).
*   GitHub Copilot subscription.

### 2. Cài đặt thư viện
```bash
pip install openai python-dotenv pandas pytest inspect
```

### 3. Quản lý bí mật (Security First)
**Tuyệt đối không hardcode API Key.** 
1. Tạo file `.env` trong thư mục gốc.
2. Thêm dòng sau: `OPENAI_API_KEY=your_secret_key_here`.
3. Sử dụng thư viện `dotenv` để load:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   api_key = os.getenv("OPENAI_API_KEY")
   ```

---

## 🖼️ Kết quả và Hình ảnh thực tế
Các kết quả chạy chương trình và giao diện tương tác được lưu trữ tại các thư mục `image/` trong mỗi bài Lab:
*   [Kết quả Lab 2 (Pricing & Usage)](./Lab_3122411109_TruongPhuKiet/lab2/image/)
*   [Gợi ý Code Lab 3](./Lab_3122411109_TruongPhuKiet/lab3/image/lab_32_recommend_Code.png)
*   [Phân tích lỗi Lab 5](./Lab_3122411109_TruongPhuKiet/lab5/image/lab_52_final_output.png)

---
*Bản báo cáo này được tổng hợp và trình bày bởi: **Trương Phú Kiệt - 3122411109***
*Ngày cập nhật: 11/03/2026*
