Dưới đây là phần tóm tắt chi tiết và giải thích đầy đủ cho **Chương 5: Thực tiễn tốt nhất khi thiết kế Prompt với OpenAI API và GitHub Copilot** (Best Practices for Prompting with OpenAI API and GitHub Copilot) dựa trên các tài liệu bạn đã cung cấp.

Chương này tập trung vào việc áp dụng khuôn khổ **"5 chữ S"** (Structured - Có cấu trúc, Surrounding context - Bối cảnh xung quanh, Single-task - Đơn nhiệm, Specific - Cụ thể, và Short - Ngắn gọn) vào hai công cụ AI phổ biến là OpenAI API và GitHub Copilot để đạt được kết quả lập trình chính xác và đáng tin cậy.

---

### 1. Khai thác thuộc tính từ các đối tượng Python cho OpenAI API
Khi tự động hóa các tác vụ lập trình bằng OpenAI API (ví dụ: viết docstring, gỡ lỗi, tạo unit test), chúng ta cần cung cấp thông tin chi tiết về code cho mô hình. 
*   **Sử dụng package `inspect`:** Python có thư viện tích hợp sẵn là `inspect`. Bạn có thể dùng hàm `inspect.getsource(tên_hàm)` để trích xuất toàn bộ mã nguồn của một hàm hoặc lớp dưới dạng chuỗi văn bản (string). Định dạng này rất dễ để các mô hình ngôn ngữ lớn (LLMs) hiểu.
*   **Sử dụng thuộc tính "Dunder" (Double underscore):** Bạn có thể lấy siêu dữ liệu (metadata) của đối tượng thông qua các thuộc tính đặc biệt như `obj.__name__` (lấy tên đối tượng), `obj.__class__.__name__` (lấy tên lớp), hoặc `obj.__doc__` (lấy docstring hiện tại).

### 2. Thiết kế Prompt chính xác cho OpenAI API
Việc tạo prompt cho OpenAI API yêu cầu sự phân tách rõ ràng giữa hướng dẫn và dữ liệu để có thể tái sử dụng theo quy mô lớn.

*   **Prompt có cấu trúc (Structured prompts):** Sử dụng hệ thống bao gồm `system prompt` (để định nghĩa ngữ cảnh và nhiệm vụ) và `user prompt` (để chứa dữ liệu cụ thể và tín hiệu yêu cầu hoàn thành).
*   **System Prompts (Bối cảnh và Đơn nhiệm):** Xác định bối cảnh xung quanh (`SURROUND`) và một nhiệm vụ duy nhất (`SINGLE_TASK`). 
    *   *Ví dụ:* `SURROUND` = "Bạn sẽ được cung cấp một hàm Python nằm trong thẻ {{{ FUNCTION }}}." và `SINGLE_TASK` = "Nhiệm vụ của bạn là tạo docstring chuẩn Google cho nó.".
*   **User Prompts (Chỉ dẫn cụ thể):** Đóng gói mã nguồn (lấy từ `inspect`) và kết thúc bằng một "tín hiệu dẫn nhập" (lead-in cue) để nhắc AI bắt đầu trả lời. 
    *   *Ví dụ:* `FUNCTION: {{{ {mã_nguồn} }}} \n GOOGLE STYLE DOCSTRING:`.

*Thực hành (Lab 5.1):* Tác giả minh họa việc đưa mã nguồn của hàm `__call__` trong mẫu thiết kế Singleton vào hệ thống cấu trúc prompt trên, gọi OpenAI API (`gpt-4o-mini`), và mô hình đã tự động trả về một docstring chuẩn Google cực kỳ chính xác mà không cần con người can thiệp.

### 3. Thiết kế Prompt chính xác cho GitHub Copilot
Mặc dù GitHub Copilot tự động xử lý phần lớn cấu trúc và bối cảnh (dựa vào file đang mở, vị trí con trỏ, lịch sử Git...), chúng ta vẫn cần áp dụng "5 chữ S" để định hướng nó tốt hơn.

*   **Cấu trúc bằng Tín hiệu dẫn nhập (Structuring with a lead-in cue):** 
    *   Thay vì viết các dòng bình luận dài dòng kể lể yêu cầu (VD: `# Implement a Singleton meta-class...`), hãy bắt đầu viết code thực tế. Việc gõ `class Singleton:` là một tín hiệu dẫn nhập hoàn hảo để Copilot tự động điền phần còn lại của kiến trúc đó.
*   **Bối cảnh thông qua Imports và Hashtags (Surrounding with imports and hashtags):**
    *   Copilot quét các file đang mở và các dòng `import`. Nếu bạn import một thư viện cụ thể (VD: `from dataclasses import dataclass`), Copilot sẽ hiểu bối cảnh và ưu tiên sử dụng các decorator của thư viện đó khi gợi ý code.
    *   Trong giao diện Copilot Chat, sử dụng các tag như `@workspace`, `@terminal` hoặc `#selection` để khoanh vùng chính xác bối cảnh bạn muốn AI phân tích.
*   **Thu hẹp mục tiêu đơn nhiệm (Further narrowing the single task):**
    *   Khi sử dụng các lệnh chat như `/fix`, nếu không có chỉ dẫn, Copilot có thể đoán sai ý định và thêm những phần code không cần thiết (VD: tự dưng thêm hàm `__post_init__`).
    *   Hãy thu hẹp tác vụ bằng cách đưa ra lệnh cụ thể, ví dụ: `/fix extract hard-coded values to global constants` (Sửa lỗi bằng cách trích xuất giá trị cứng thành hằng số toàn cục).
*   **Chỉ dẫn cụ thể bằng Code sạch (Type hints, Docstrings, Descriptive names, Unit tests):**
    *   Viết code rõ ràng chính là cách "prompt" tốt nhất cho Copilot. Việc đặt tên biến có ý nghĩa, sử dụng Type Hints (khai báo kiểu dữ liệu như `float`, `int`), và viết Unit Tests sẽ giúp Copilot dự đoán chính xác ý đồ của bạn và đề xuất code chất lượng cao.
*   **Prompt ngắn gọn, không chứa bình luận thừa (Short prompts without comment fluff):**
    *   Tránh viết những bình luận "nhảm" (fluff) chỉ nhằm mục đích gợi ý cho AI nhưng sau đó bạn lại phải xóa đi vì chúng làm bẩn code (VD: `# initialize a product variable to 1`). 
    *   Thay vào đó, hãy sử dụng tên biến và type hints (VD: `product: float = `) làm tín hiệu dẫn nhập. Cách này vừa sạch sẽ, vừa tạo kết quả dự đoán tốt hơn cho Copilot.

*Thực hành (Lab 5.2):* Tác giả minh họa việc gỡ lỗi một lớp Singleton bị sai. Bằng cách viết một Unit Test có tên mô tả rõ ràng (`test_singleton_should_return_same_instance`), chạy test để lấy lỗi, sau đó dùng lệnh `@terminal /explain` để Copilot giải thích nguyên nhân lỗi, và cuối cùng dùng lệnh `/fix cls instantiation` để Copilot tập trung sửa đúng dòng bị sai.

### Tóm tắt tổng thể
Chương này khẳng định rằng dù sử dụng API tự động (OpenAI) hay trợ lý lập trình trực tiếp (GitHub Copilot), sự kết hợp giữa **phân tách nhiệm vụ (system/user prompts)**, **định hướng ngữ cảnh (imports, `#selection`)**, và **viết code sạch để làm tín hiệu (lead-in cues, type hints)** là chìa khóa để khai thác tối đa sức mạnh của GenAI mà không làm rác mã nguồn.