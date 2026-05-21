# BÁO CÁO THỰC HÀNH LAB 3
## Chương 3: Hướng dẫn sử dụng GitHub Copilot với PyCharm, VS Code và Jupyter Notebook

**Họ và tên:** Trương Phú Kiệt  
**MSSV:** 3122411109  
**Môn học:** Seminar  

---

## 1. Giới thiệu tổng quan

GitHub Copilot là một công cụ lập trình AI được xây dựng dựa trên mô hình ngôn ngữ lớn (LLM), được thiết kế đặc biệt cho các tác vụ hoàn thành mã nguồn, phân tích mã và hỗ trợ lập trình thông qua giao diện chat. Nhờ sự kết hợp giữa kiến thức được học từ lượng lớn mã nguồn mở trên GitHub và ngữ cảnh mã hiện tại của người dùng, Copilot có khả năng đưa ra các gợi ý mã nguồn phù hợp và chính xác.

Sau khi đã xây dựng chương trình hoàn thành mã đơn giản bằng OpenAI API (Lab 2.3), chúng ta có thể hiểu rõ hơn về cách Copilot hoạt động, bao gồm cả các bước tiền xử lý và hậu xử lý bổ sung mà công cụ này thực hiện so với một lời gọi API đơn thuần.

---

## 2. Kiến trúc và Cách thức hoạt động của GitHub Copilot

### 2.1 Luồng xử lý gợi ý mã (Code Completion Flow)

Để tạo ra các gợi ý mã nguồn có ý nghĩa, Copilot xử lý đầu vào và đầu ra của LLM qua nhiều bước:

- **Thu thập ngữ cảnh (Context gathering):** Copilot tổng hợp thông tin từ các dòng mã xung quanh con trỏ, chữ ký hàm, các tệp đang mở, lịch sử chỉnh sửa gần đây và thông tin Git.
- **Xây dựng prompt:** Toàn bộ thông tin được tổ chức thành *system prompts* và *user prompts* rồi gửi đến LLM.
- **Hậu xử lý (Post-processing):** Đầu ra từ LLM được xác thực để đảm bảo mã có thể biên dịch thành công trước khi hiển thị cho người dùng.

*thêm ảnh Figure 3.1 (Sơ đồ luồng xử lý gợi ý của Copilot) ở đây*

> **Lưu ý quan trọng:** Nhiều lập trình viên lầm tưởng rằng Copilot gửi toàn bộ repository lên LLM. Thực tế, chỉ các đoạn mã liên quan mới được gửi đi, nhằm tiết kiệm chi phí token đầu vào và đảm bảo tốc độ phản hồi.

### 2.2 Ba chế độ tương tác

GitHub Copilot cung cấp ba chế độ tương tác chính:

| Chế độ | Mô tả | Trường hợp sử dụng |
|--------|-------|-------------------|
| **Chat** | Cửa sổ hỏi đáp dạng ChatGPT hoặc inline chat | Hỏi câu hỏi liên quan đến mã, giải thích khái niệm |
| **Completion** | Tự động gợi ý mã (ghost text) khi đang gõ | Triển khai tính năng mới |
| **Analysis** | Sửa lỗi, giải thích, tạo test bằng slash commands | Làm việc với mã hiện có |

---

## 3. Tài khoản, Chi phí và Chính sách

### 3.1 Điều kiện sử dụng miễn phí

Có ba trường hợp được sử dụng GitHub Copilot miễn phí:
- **Tài khoản miễn phí có giới hạn**: tối đa 2.000 lượt hoàn thành mã và 50 yêu cầu chat mỗi tháng
- **Sinh viên và giảng viên** có email đại học hợp lệ (đăng ký qua GitHub Education Pack)
- **Người bảo trì dự án mã nguồn mở** phổ biến

### 3.2 Bảng giá

| Gói | Giá |
|-----|-----|
| Individual | 10 USD/tháng hoặc 100 USD/năm |
| Business | 19 USD/người/tháng |
| Enterprise | 39 USD/người/tháng |

### 3.3 Chính sách bản quyền mã nguồn

Vì mô hình Copilot được huấn luyện trên mã nguồn mở và công khai, một số gợi ý có thể trùng với mã được bảo hộ bản quyền. GitHub cung cấp tùy chọn **"Suggestions matching public code"** để người dùng lựa chọn loại trừ các gợi ý trùng lặp.

*thêm ảnh Figure 3.2 (Cài đặt quyền riêng tư và bản quyền trong Copilot) ở đây*

---

## 4. Cài đặt GitHub Copilot

### 4.1 Kích hoạt tài khoản

Truy cập [github.com](https://www.github.com), nhấp vào biểu tượng hồ sơ và chọn **Your Copilot**.

*thêm ảnh Figure 3.3 (Truy cập Copilot trong tài khoản GitHub) ở đây*

Sau khi hoàn tất, trang cài đặt Copilot tại `https://github.com/settings/copilot` sẽ hiển thị cấp độ truy cập và các chính sách.

*thêm ảnh Figure 3.4 (Tiêu đề trang cài đặt GitHub Copilot) ở đây*

### 4.2 Cài đặt trên PyCharm

Vào **PyCharm | Settings | Plugins**, tìm kiếm **GitHub Copilot** trong Marketplace, cài đặt và khởi động lại IDE. Sau khi khởi động lại, đăng nhập vào tài khoản GitHub.

Để kiểm tra trạng thái, nhìn vào biểu tượng Copilot ở góc dưới của IDE:

*thêm ảnh Figure 3.5 (GitHub Copilot Plugin trong PyCharm) ở đây*

*thêm ảnh Figure 3.6 (Kiểm tra trạng thái plugin Copilot trong PyCharm) ở đây*

### 4.3 Cài đặt trên VS Code

Vào **Code | Extensions**, tìm **GitHub Copilot** và cài đặt. Extension **GitHub Copilot Chat** sẽ được cài đặt tự động kèm theo.

*thêm ảnh Figure 3.7 (Extension GitHub Copilot và Copilot Chat trong VS Code) ở đây*

Sau xác thực, nhấp vào biểu tượng GitHub Copilot ở góc dưới phải:

*thêm ảnh Figure 3.8 (Biểu tượng GitHub Copilot ở góc dưới phải VS Code) ở đây*

*thêm ảnh Figure 3.9 (Xác nhận trạng thái extension Copilot trong VS Code) ở đây*

> **Lưu ý:** Copilot được tích hợp sâu hơn với VS Code. Các tính năng mới như hỗ trợ Jupyter Notebook thường xuất hiện trên VS Code trước PyCharm.

---

## 5. Sử dụng Copilot Chat

Copilot Chat hỗ trợ các câu hỏi liên quan đến mã, chủ đề ngoài, lệnh terminal và cả VS Code IDE.

- **Mở trong VS Code:** `Ctrl + Alt + I` (hoặc `Cmd + Control + I` trên Mac)
- **Mở trong PyCharm:** `Ctrl + Shift + C` hoặc chọn tab **GitHub Copilot Chat** trong menu bên trái

*thêm ảnh Figure 3.10 (Cửa sổ chat GitHub Copilot trong VS Code) ở đây*

*thêm ảnh Figure 3.11 (Cửa sổ chat GitHub Copilot trong PyCharm) ở đây*

Khi nhập prompt `What can you do?`, Copilot sẽ liệt kê các khả năng như: viết và debug mã, giải thích code, tạo unit test, hỗ trợ Git, giải thích terminal...

*thêm ảnh Figure 3.12 (Lựa chọn mô hình LLM trong cửa sổ chat Copilot) ở đây*

---

## 6. Lab 3.1 – Tính Trung bình nhân bằng Chat và Completion

### 6.1 Mục tiêu

Sử dụng chế độ Chat để tìm hiểu về **trung bình nhân (geometric mean)**, sau đó dùng chế độ Completion để triển khai hàm tính toán.

### 6.2 Công thức toán học

**Trung bình cộng (Arithmetic Mean):**
$$\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$$

**Trung bình nhân (Geometric Mean):**
$$G = \left(\prod_{i=1}^{n} x_i\right)^{\frac{1}{n}}$$

Ví dụ: Trung bình nhân của 5 và 20:
$$G = (5 \times 20)^{1/2} = \sqrt{100} = 10$$

### 6.3 Hướng dẫn thực hiện

**Phần 1 – Chat:** Mở cửa sổ Copilot Chat và nhập prompt:
```
Explain the geometric mean.
```

**Phần 2 – Completion:** Gõ chữ ký hàm để Copilot tự hoàn thiện thân hàm:
```python
def get_geometric_mean_of_two_numbers(
    a: float,
    b: float,
) -> float:
```

**Phần 3 – Print:** Gõ biến và lệnh `print` để Copilot tự gợi ý lời gọi hàm:
```python
num1: float = 5.0
num2: float = 20.0
print
```

### 6.4 Code thực hiện (`lab31.py`)

```python
def get_geometric_mean_of_two_numbers(
    a: float,
    b: float,
) -> float:
    """
    Get the geometric mean of two floating-point numbers
    """
    return (a * b) ** 0.5

num1: float = 5.0
num2: float = 20.0
print(f"The geometric mean of {num1} and {num2} is: {get_geometric_mean_of_two_numbers(num1, num2)}")
```

### 6.5 Kết quả

*thêm ảnh lab_31_part1.png (Copilot Chat giải thích geometric mean) ở đây*

*thêm ảnh lab_31_output.png (Kết quả chạy Lab 3.1) ở đây*

```
The geometric mean of 5.0 and 20.0 is: 10.0
```

### 6.6 Phân tích

- Chữ ký hàm đầy đủ (tên hàm, tham số, type hints, kiểu trả về) là một prompt hiệu quả để Copilot tự sinh ra thân hàm chính xác.
- Copilot Chat có thể trả về công thức LaTeX thô và bị cắt cụt do giới hạn `max_tokens`, song vẫn đủ ngữ nghĩa để hiểu khái niệm.
- Lệnh `print` là cue hiệu quả để Copilot gợi ý lời gọi hàm với đúng tham số.

---

## 7. Lab 3.2 – Phím tắt Completion cho tính Trung bình nhân

### 7.1 Mục tiêu

Thực hành các phím tắt của GitHub Copilot khi sử dụng chế độ **Completion** để triển khai hàm tính trung bình nhân cho một dãy số thực.

### 7.2 Bảng phím tắt quan trọng

| Thao tác | PyCharm | VS Code |
|----------|---------|---------|
| Chấp nhận toàn bộ gợi ý | `Tab` | `Tab` |
| Hoàn tác | `Ctrl + Z` | `Ctrl + Z` |
| Chấp nhận từng dòng | `Ctrl + Alt + →` | Trỏ chuột → `...` → Accept Line |
| Chấp nhận từng từ | `Ctrl + →` | `Ctrl + →` |
| Ẩn gợi ý | `Esc` | `Esc` |
| Kích hoạt lại gợi ý | `Alt + \` | `Alt + \` |
| Gợi ý tiếp theo | `Alt + ]` | `Alt + ]` |
| Gợi ý trước | `Alt + [` | `Alt + [` |
| Mở danh sách gợi ý | `Alt + Enter` / Copilot: Open Completion | `Ctrl + Enter` |

### 7.3 Code thực hiện (`lab32.py`)

```python
def get_geometric_mean(*nums: float) -> float:
    """
    Get the geometric mean of a list of floating-point numbers
    """
    product = 1.0
    for num in nums:
        product *= num
    return product ** (1 / len(nums))
```

### 7.4 Kết quả thực hành

*thêm ảnh lab_32_recommend_Code.png (Copilot gợi ý mã tự động trong Lab 3.2) ở đây*

*thêm ảnh lab_32_shortcuts.png (Thực hành phím tắt Copilot trong Lab 3.2) ở đây*

Ví dụ minh họa danh sách gợi ý mã trong PyCharm:

*thêm ảnh Figure 3.13 (Ví dụ về Copilot code completion trong VS Code) ở đây*

*thêm ảnh Figure 3.14 (Copilot inline menu trong PyCharm) ở đây*

*thêm ảnh Figure 3.15 (Bảng gợi ý mã Copilot trong PyCharm) ở đây*

*thêm ảnh Figure 3.16 (Bảng gợi ý mã Copilot trong VS Code) ở đây*

### 7.5 Phân tích

- Việc nắm vững phím tắt giúp tăng đáng kể tốc độ làm việc với Copilot.
- Tính năng **Completions Pane** (danh sách tối đa 10 gợi ý khác nhau) cho phép lựa chọn phương án tối ưu nhất.
- Cùng một prompt có thể sinh ra nhiều kết quả khác nhau do tính ngẫu nhiên trong LLM, do đó việc so sánh nhiều gợi ý là hữu ích.

---

## 8. Lab 3.3 – Phân tích mã với Copilot (VS Code Jupyter Notebook)

### 8.1 Mục tiêu

Sử dụng chế độ **Analysis** với các lệnh `/fix` và `/explain` để:
1. Sửa lỗi trong hàm tính trung bình nhân của ba số
2. Giải thích một hàm tính trung bình nhân tổng quát

### 8.2 Mã khởi đầu

```python
from functools import reduce

# Hàm BỊ LỖI: dùng căn bậc hai thay vì căn bậc ba
def get_geometric_mean_for_three_numbers(a, b, c):
    return (a * b * c) ** (1/2)  # SAI: phải là (1/3)

# Hàm đúng cho dãy số bất kỳ
def get_geometric_mean(*nums: float) -> float:
    """Get the geometric mean of a sequence of numbers"""
    if not len(nums):
        raise ValueError("Cannot calculate the geometric mean of an empty sequence")
    product = reduce(lambda a, b: a * b, nums)
    if product < 0 and len(nums) % 2 == 0:
        raise ValueError("Cannot calculate the geometric mean")
    return pow(product, 1 / len(nums))
```

### 8.3 Công cụ phân tích mã

#### Truy cập qua menu chuột phải:

*thêm ảnh Figure 3.17 (Phân tích mã Copilot trong PyCharm) ở đây*

*thêm ảnh Figure 3.18 (Phân tích mã Copilot trong VS Code) ở đây*

#### Inline Chat (Copilot trong dòng):
- **VS Code:** `Ctrl + I` (hoặc `Cmd + I` trên Mac)
- **PyCharm:** `Ctrl + Shift + I`

*thêm ảnh Figure 3.19 (Copilot editor inline chat trong VS Code) ở đây*

*thêm ảnh Figure 3.20 (Copilot inline chat trong PyCharm) ở đây*

#### Cửa sổ Edits (VS Code):

*thêm ảnh Figure 3.21 (Truy cập cửa sổ Edits của Copilot) ở đây*

*thêm ảnh Figure 3.22 (Làm việc với #selection trong cửa sổ Edits) ở đây*

*thêm ảnh Figure 3.23 (Thêm input validation bằng cửa sổ Edits) ở đây*

### 8.4 Ứng dụng lệnh `/fix`

Bôi đen hàm `get_geometric_mean_for_three_numbers`, mở Inline Chat và nhập `/fix`. Copilot đề xuất sửa từ `**(1/2)` thành `**(1/3)`:

*thêm ảnh lab_33_fix.png (Kết quả dùng /fix để sửa lỗi trong Lab 3.3) ở đây*

*thêm ảnh Figure 3.24 (Gợi ý sửa lỗi của Copilot trong VS Code) ở đây*

*thêm ảnh Figure 3.25 (Gợi ý sửa lỗi của Copilot trong PyCharm) ở đây*

*thêm ảnh Figure 3.26 (Nút Preview để chấp nhận thay đổi trong PyCharm) ở đây*

*thêm ảnh Figure 3.27 (Chấp nhận gợi ý sửa lỗi Copilot trong PyCharm) ở đây*

**Kết quả sau khi sửa:**
```python
def get_geometric_mean_for_three_numbers(a, b, c):
    return (a * b * c) ** (1/3)  # Đúng
```

### 8.5 Ứng dụng lệnh `/explain`

Di chuyển cursor vào hàm `get_geometric_mean`, mở Inline Chat và nhập `/explain`. Copilot phân tích hàm thành 4 bước:

1. **Kiểm tra mảng rỗng:** `if not len(nums)` → raise `ValueError`
2. **Tính tích:** dùng `reduce(lambda a, b: a * b, nums)`
3. **Kiểm tra điều kiện số thực:** nếu tích âm và số lượng phần tử chẵn → raise `ValueError`
4. **Trả về căn bậc n:** `pow(product, 1 / len(nums))`

*thêm ảnh lab_33_explain.png (Kết quả dùng /explain trong Lab 3.3) ở đây*

### 8.6 Code hoàn chỉnh (`lab33.py`)

```python
from functools import reduce

def get_geometric_mean_for_three_numbers(a, b, c):
    """
    Calculate the geometric mean of three numbers (cube root of a*b*c).
    """
    return (a * b * c) ** (1/3)

def get_geometric_mean(*nums: float) -> float:
    """
    Get the geometric mean of a sequence of numbers
    """
    if not len(nums):
        raise ValueError("Cannot calculate the geometric mean of an empty sequence")
    product = reduce(lambda a, b: a * b, nums)
    if product < 0 and len(nums) % 2 == 0:
        raise ValueError("Cannot calculate the geometric mean")
    return pow(product, 1 / len(nums))
```

### 8.7 Phân tích

- Lệnh `/fix` giúp phát hiện và sửa lỗi logic nhanh chóng mà không cần đọc lại toàn bộ mã.
- Lệnh `/explain` tách hàm thành các bước rõ ràng, hữu ích cho việc review và bảo trì code.
- Nếu `/explain` giải thích không đầy đủ, đây là dấu hiệu cho thấy mã cần được **tái cấu trúc (refactor)** để dễ đọc hơn.
- **Cửa sổ Edits** là tính năng mạnh mẽ cho phép làm việc trên nhiều tệp cùng lúc với giao diện so sánh (diff) trực quan.

---

## 9. Tổng kết

### 9.1 So sánh ba chế độ tương tác

| Tiêu chí | Chat | Completion | Analysis |
|----------|------|-----------|----------|
| **Mục đích chính** | Hỏi đáp, giải thích khái niệm | Sinh mã mới tự động | Phân tích, sửa mã hiện có |
| **Cách kích hoạt** | `Ctrl+Alt+I` / `Ctrl+Shift+C` | Tự động khi gõ | Chuột phải / `Ctrl+I` / `Ctrl+Shift+I` |
| **Lệnh hữu ích** | Prompt tự nhiên | Chữ ký hàm, type hints | `/fix`, `/explain`, `/test` |
| **Thực hành trong lab** | Lab 3.1 | Lab 3.1, 3.2 | Lab 3.3 |

### 9.2 Kinh nghiệm rút ra

1. **Chữ ký hàm chi tiết** (tên, tham số, type hints, return type) là prompt hiệu quả nhất cho Completion.
2. **Nắm vững phím tắt** (đặc biệt `Tab`, `Ctrl+Z`, `Alt+]`, `Ctrl+Enter`) giúp tăng tốc độ làm việc đáng kể.
3. **`/fix`** rất hiệu quả với lỗi logic đơn giản, không cần phải debug thủ công.
4. **`/explain`** không chỉ giải thích mã mà còn gián tiếp chỉ ra những đoạn cần refactor.
5. **VS Code tích hợp sâu hơn PyCharm**: hỗ trợ Jupyter Notebook, cửa sổ Edits, và nhận tính năng mới sớm hơn.

### 9.3 Câu hỏi ôn tập

**Q1: Copilot có phải dịch vụ trả phí không?**  
Copilot chủ yếu là dịch vụ trả phí, nhưng có ngoại lệ: tài khoản miễn phí có giới hạn (2.000 completions/tháng), sinh viên/giảng viên, và người bảo trì dự án mã nguồn mở lớn được dùng miễn phí.

**Q2: Ba chế độ tương tác của GitHub Copilot là gì?**  
**Chat** (hỏi đáp qua cửa sổ hoặc inline), **Completion** (tự động gợi ý khi gõ), và **Analysis** (phân tích mã hiện có qua `/fix`, `/explain`, `/test`).

---

## 10. Tài liệu tham khảo

- Hila Paz Herszfang & Peter V. Henstock. *Supercharged Coding with GenAI*. Packt Publishing, 2025. Chapter 3, pp. 45–75.
- GitHub Copilot Documentation: https://docs.github.com/en/copilot/quickstart
- Copilot Subscription Plans: https://docs.github.com/en/copilot/about-github-copilot/subscription-plans-for-github-copilot
- Copilot Setup in IDE: https://docs.github.com/en/copilot/setting-up-github-copilot/setting-up-github-copilot-for-yourself
- Copilot Best Practices: https://docs.github.com/en/copilot/using-github-copilot/best-practices-for-using-github-copilot
