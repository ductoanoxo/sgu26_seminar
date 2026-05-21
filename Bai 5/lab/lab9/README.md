# 📚 CHƯƠNG 9: CHIẾN LƯỢC NHẮC (PROMPTING STRATEGIES)

Dưới đây là bản diễn giải chi tiết, chuyên sâu và được trình bày trực quan về **Chương 9: Chiến lược nhắc (Prompting Strategies)** từ cuốn sách "Supercharged Coding with GenAI". 

Chương này tập trung vào **ba chiến lược prompting chính** giúp nâng cao hiệu suất của mô hình AI trong việc giải quyết các bài toán lập trình phức tạp.

---

## 🌟 TỔNG QUAN VỀ CHIẾN LƯỢC NHẮC

Khi sử dụng GenAI để giải quyết các bài toán lập trình, cách chúng ta **"nhắc" (prompt) mô hình** sẽ quyết định chất lượng kết quả. Có Ba chiến lược chính:

| 🎯 Chiến Lược | 📝 Mô Tả | ✅ Ưu Điểm | ⚠️ Hạn Chế |
|---|---|---|---|
| **Baseline** | Gửi một prompt đơn lẻ, trực tiếp | Nhanh, đơn giản | Dễ thiếu chi tiết, cơ hội tối ưu hóa `ít` |
| **Chain of Thought (CoT)** | Yêu cầu mô hình suy nghĩ từng bước trước khi đưa ra kết quả | Giải quyết bài toán phức tạp tốt hơn | Thời gian xử lý lâu hơn, chi phí API cao hơn |
| **Chaining** | Gửi nhiều prompt liên tiếp, mỗi lần tinh chỉnh kết quả trước đó | Có thể tái sử dụng kết quả, dễ kiểm soát từng bước | Yêu cầu quản lý lịch sử conversational, phức tạp hơn |

---

## 🔬 PHẦN 1: BÀI TOÁN VÀ NGỮ CẢNH

### Bài Toán: Tính Lợi Suất Trung Bình Đầu Tư (Average Investment Return)

Chúng ta sẽ sử dụng **bài toán tính lợi suất trung bình** từ các năm đầu tư khác nhau. Đây là một bài toán thực tế trong lĩnh vực tài chính:

**Công thức toán học:**
- **Lợi suất hàng năm (Annual Returns):** $r_1, r_2, ..., r_n$
- **Lợi suất Brutto (Gross Returns):** $G_i = 1 + r_i$
- **Trung bình hình học (Geometric Mean):** $\overline{G} = \sqrt[n]{G_1 \times G_2 \times ... \times G_n}$
- **Lợi suất Netto trung bình (Net Average Return):** $\overline{r} = \overline{G} - 1$

**Ví dụ cụ thể:**
```
Nếu bạn đầu tư vào chứng chỉ:
- Năm 1: lãi suất +10% (net_returns = 0.10)
- Năm 2: lãi suất +20% (net_returns = 0.20)
- Năm 3: lãi suất -5% (net_returns = -0.05)

Thì lợi suất trung bình = (1.10 × 1.20 × 0.95)^(1/3) - 1 = 0.0746 ≈ 7.46%
```

### Mã nguồn cần hoàn thiện:

```python
from typing import Dict
import numpy as np

# Hàm chính cần hoàn thiện
def get_average_return(
        net_returns: Dict[str, float],
) -> float:
    gross_returns: np.ndarray = get_gross_returns(net_returns)
    gross_average: float = get_geometric_mean(gross_returns)
    net_average: float = get_net_average(gross_average)
    return net_average

# Các hàm phụ cần tạo
def get_gross_returns(net_returns: Dict[str, float]) -> np.ndarray:
    # ❓ Cần hoàn thiện

def get_geometric_mean(gross_returns: np.ndarray) -> float:
    # ❓ Cần hoàn thiện

def get_net_average(gross_average: float) -> float:
    # ❓ Cần hoàn thiện
```

---

## 🎯 PHẦN 2: CHIẾN LƯỢC BASELINE (Cơ Sở)

### Khái niệm

**Baseline Strategy** là phương pháp gửi một prompt **đơn lẻ**, **trực tiếp** đến mô hình OpenAI mà không có bất kỳ xử lý hay tinh chỉnh nào. Đây là cách đơn giản nhất nhưng cũng ít hiệu quả nhất.

**Luồng thực thi:**
```
Prompt đơn lẻ → OpenAI API → Kết quả
```

### Cấu trúc Prompt cho Baseline

Prompt cơ sở nên có:
- **SURROUND:** Bối cảnh - mô tả bạn sẽ được cấp cái gì
- **SINGLE_TASK:** Nhiệm vụ duy nhất - xác định chính xác cần làm gì

```python
SURROUND = "You are provided with a Python function signature enclosed with {{{ FUNCTION }}}."
SINGLE_TASK = "Your task is to implement the function."

SRC_CODE = """def get_geometric_mean(
    net_returns: Dict[str, float],
) -> float:"""
```

### Lab 9.1: Baseline Strategy với OpenAI API

**Mục tiêu:** Sử dụng Baseline Strategy để hoàn thiện hàm `get_geometric_mean()`.

**Hướng dẫn:**
1. Tạo file `lab91_baseline.py`
2. Sử dụng OpenAI API để gửi prompt baseline
3. Trích xuất mã từ phản hồi của mô hình
4. Kiểm tra kết quả

**Mã mẫu:**
```python
import inspect
from openai import OpenAI
from openai.types.chat import ChatCompletion

SURROUND = "You are provided with a Python function signature enclosed with {{{ FUNCTION }}}."
SINGLE_TASK = "Your task is to implement the function."

SRC_CODE = """def get_geometric_mean(
    net_returns: Dict[str, float],
) -> float:"""

def get_user_prompt(src: str) -> str:
    return f""" 
    FUNCTION: {{{{{{ {src} }}}}}} 

    CODE: 
    """

if __name__ == '__main__':
    client: OpenAI = OpenAI()
    system_prompt = f"{SURROUND} {SINGLE_TASK}"
    user_prompt = get_user_prompt(SRC_CODE)
    
    completion: ChatCompletion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    output = completion.choices[0].message.content
    print("=== BASELINE RESULT ===")
    print(output)
```

**Kết quả mong đợi:**
```python
def get_geometric_mean(net_returns: Dict[str, float]) -> float:
    product: float = 1
    for key in net_returns:
        product *= net_returns[key]
    geometric_mean: float = product ** (1 / len(net_returns))
    return geometric_mean
```

### Lab 9.2: Baseline với GitHub Copilot

**Mục tiêu:** Sử dụng GitHub Copilot trong VS Code để hoàn thiện hàm.

**Hướng dẫn:**
1. Mở VS Code
2. Tạo file `lab92_copilot_baseline.py`
3. Gõ chữ ký hàm:
   ```python
   def get_geometric_mean(net_returns: Dict[str, float]) -> float:
   ```
4. Copilot sẽ tự động gợi ý phần thân hàm (nhấn `Tab` để chấp nhận)
5. So sánh kết quả với OpenAI API

**Nhận xét:**
- Copilot gợi ý xử lý dựa trên ngữ cảnh file hiện tại
- OpenAI API yêu cầu prompt cấu trúc rõ ràng hơn
- Cách tiếp cận nào nhanh hơn?

---

## 🧠 PHẦN 3: CHIẾN LƯỢC CHAIN OF THOUGHT (CoT)

### Khái niệm

**Chain of Thought (CoT)** là phương pháp **yêu cầu mô hình suy nghĩ từng bước trước khi đưa ra kết quả cuối cùng**. Thay vì nhảy thẳng đến câu trả lời, mô hình sẽ:

1. **Phân tích vấn đề**
2. **Liệt kê các bước giải quyết**
3. **Thực hiện từng bước**
4. **Đưa ra kết luận**

**Luồng thực thi:**
```
Prompt yêu cầu "hãy suy nghĩ từng bước"
    ↓
Mô hình trả lời: "Step 1: ..., Step 2: ..., Step 3: ..."
    ↓
Mô hình đưa ra kết quả
```

### Lợi ích của CoT

- ✅ **Độ chính xác cao hơn** cho các bài toán phức tạp
- ✅ **Dễ kiểm chứng** logic vì có thể thấy từng bước tư duy
- ✅ **Giảm "hallucinations"** (mô hình bịa ra kết quả)
- ⚠️ **Chi phí cao hơn** vì phải gửi và nhận thêm dữ liệu (tokens)
- ⚠️ **Thời gian lâu hơn** do phải suy nghĩ nhiều bước

### Lab 9.3: Chain of Thought Strategy

**Mục tiêu:** Sử dụng CoT để hoàn thiện toàn bộ hàm `get_average_return()` và các hàm phụ.

**Hướng dẫn:**
1. Tạo file `lab93_cot.py`
2. Sử dụng Prompt yêu cầu "suy nghĩ từng bước"
3. Phân tích đầu vào từng bước

**Mã mẫu:**
```python
import inspect
from openai import OpenAI
from openai.types.chat import ChatCompletion

SURROUND = """You are provided with a Python function enclosed with {{{ FUNCTION }}} 
that calls functions that should be completed."""

SINGLE_TASK = """Your task is to implement the missing functions.
Think step by step:
1. Understand what each function should do
2. Determine the mathematical operations needed
3. Write clean, well-documented code"""

SOURCE_CODE = """
def get_average_return(net_returns: Dict[str, float]) -> float:
    gross_returns: np.ndarray = get_gross_returns(net_returns)
    gross_average: float = get_geometric_mean(gross_returns)
    net_average: float = get_net_average(gross_average)
    return net_average
"""

def get_user_prompt(src: str) -> str:
    return f"""
    FUNCTION: {{{{{{ {src} }}}}}}
    
    Please think step by step and implement all missing functions.
    CODE:
    """

if __name__ == '__main__':
    client: OpenAI = OpenAI()
    system_prompt = f"{SURROUND} {SINGLE_TASK}"
    user_prompt = get_user_prompt(SOURCE_CODE)
    
    completion: ChatCompletion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    output = completion.choices[0].message.content
    print("=== CHAIN OF THOUGHT RESULT ===")
    print(output)
```

**Phân tích đầu ra:**
- Có bao nhiêu bước suy nghĩ?
- Mô hình có giải thích logic của nó không?
- Kết quả có chính xác hơn Baseline không?

---

## 🔗 PHẦN 4: CHIẾN LƯỢC CHAINING (Xâu chuỗi)

### Khái niệm

**Chaining Strategy** là phương pháp **gửi nhiều prompt liên tiếp trong một cuộc hội thoại (conversation)**. Thay vì gửi một prompt lớn, bạn:

1. **Gửi Prompt 1** → Nhận kết quả
2. **Thêm kết quả vào lịch sử hội thoại**
3. **Gửi Prompt 2** → Nhận kết quả tinh chỉnh
4. **Lặp lại** cho đến khi hài lòng

**Luồng thực thi:**
```
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "Prompt 1"},
    {"role": "assistant", "content": "Result 1"},
    {"role": "user", "content": "Prompt 2"},
    {"role": "assistant", "content": "Result 2"},
    ...
]
```

### Lợi ích của Chaining

- ✅ **Kiểm soát chi tiết** - có thể điều chỉnh từng bước
- ✅ **Tái sử dụng kết quả** - nhận thêm tinh chỉnh từ kết quả trước
- ✅ **Tương tác được** - có thể trao đổi thêm với mô hình
- ⚠️ **Phức tạp hơn** - phải quản lý lịch sử conversation
- ⚠️ **Chi phí cao hơn** - phải gửi toàn bộ lịch sử trong mỗi request

### Lab 9.4: Naive Chaining Strategy

**Mục tiêu:** Sử dụng một chuỗi các prompt để tinh chỉnh kết quả theo từng bước.

**Hướng dẫn:**
1. Tạo file `lab94_naive_chaining.py`
2. Gửi 3 prompt liên tiếp:
   - Prompt 1: "Hoàn thiện hàm `get_average_return()`"
   - Prompt 2: "Thêm type hints cho tất cả biến"
   - Prompt 3: "Thêm Google Style docstring"
3. Lưu lịch sử hội thoại

**Mã mẫu:**
```python
import inspect
from openai import OpenAI
from openai.types.chat import ChatCompletion

SURROUND = """You are provided with a Python function enclosed with {{{ FUNCTION }}} 
that calls functions that should be completed."""
SINGLE_TASK = "Your task is to implement the missing functions."

SOURCE_CODE = """
def get_average_return(net_returns: Dict[str, float]) -> float:
    gross_returns: np.ndarray = get_gross_returns(net_returns)
    gross_average: float = get_geometric_mean(gross_returns)
    net_average: float = get_net_average(gross_average)
    return net_average
"""

def get_user_prompt(src: str) -> str:
    return f"""
    FUNCTION: {{{{{{ {src} }}}}}}
    
    CODE:
    """

if __name__ == '__main__':
    client: OpenAI = OpenAI()
    system_prompt = f"{SURROUND} {SINGLE_TASK}"

    # Khởi tạo lịch sử hội thoại
    messages = [{"role": "system", "content": system_prompt}]

    # Chuỗi các prompt
    prompt_1 = get_user_prompt(SOURCE_CODE)
    prompt_2 = "Add type hints to all variables."
    prompt_3 = "Include Google Style docstring."

    # Gửi từng prompt lần lượt
    for i, prompt in enumerate([prompt_1, prompt_2, prompt_3], 1):
        messages.append({"role": "user", "content": prompt})
        
        completion: ChatCompletion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        
        output: str = completion.choices[0].message.content
        messages.append({"role": "assistant", "content": output})
        
        print(f"\n=== STEP {i} OUTPUT ===")
        print(output)

    print("\n=== FINAL RESULT ===")
    print(output)
```

**Phân tích:**
- So sánh kích thước của mỗi kết quả (tokens)
- Kết quả có tốt hơn Baseline không?
- Chi phí API có cao hơn không?

### Lab 9.5: Selective Chaining Strategy

**Mục tiêu:** Sử dụng Chaining nhưng **chọn lọc** - chỉ gửi prompt cần thiết.

**Hướng dẫn:**
1. Tạo file `lab95_selective_chaining.py`
2. Thay vì gửi 3 prompt riêng, hợp nhất một số prompt:
   - Prompt 1: "Hoàn thiện các hàm + thêm type hints"
   - Prompt 2: "Thêm Google Style docstring"
3. So sánh chi phí và chất lượng kết quả

**Nhận xét:**
- Giản lược số lượng round-trip API giảm chi phí
- Hiệu suất vẫn tốt không?

---

## 📊 PHẦN 5: SO SÁNH CHIẾN LƯỢC (COMPARATIVE ANALYSIS)

### Bảng so sánh hiệu suất

| Tiêu chí | Baseline | CoT | Chaining |
|---|---|---|---|
| 🚀 **Tốc độ** | ⭐⭐⭐ | ⭐ | ⭐⭐ |
| 💰 **Chi phí** | ⭐⭐⭐ | ⭐ | ⭐⭐ |
| 🎯 **Độ chính xác** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 🔍 **Khả năng giải thích** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 📝 **Dễ quản lý** | ⭐⭐⭐ | ⭐⭐ | ⭐ |

### Khi nào dùng cái gì?

**🎯 Baseline khi:**
- ✅ Bài toán đơn giản, rõ ràng
- ✅ Cần phải nhanh và rẻ
- ✅ Không cần giải thích chi tiết

**🧠 Chain of Thought khi:**
- ✅ Bài toán phức tạp, có nhiều bước
- ✅ Cần độ chính xác cao
- ✅ Muốn thấy logic suy nghĩ của AI

**🔗 Chaining khi:**
- ✅ Cần tinh chỉnh từng bước
- ✅ Muốn kiểm soát quá trình chi tiết
- ✅ Có thể dung nạp chi phí cao hơn

---

## 🔬 PHẦN 6: LAB THỰC HÀNH - TỔNG HỢP

### Lab 9.6: So sánh đầu ra ba chiến lược

**Mục tiêu:** Chạy cả ba chiến lược trên cùng bài toán và so sánh.

**Hướng dẫn:**
1. Tạo file `lab96_comparison.py`
2. Chạy ba chiến lược Baseline, CoT, Chaining
3. Ghi lại:
   - Thời gian thực thi
   - Số lượng token sử dụng
   - Chất lượng kết quả
   - Chi phí ước tính

**Mã mẫu:**
```python
import time
from openai import OpenAI
from openai.types.chat import ChatCompletion

def strategy_baseline(client: OpenAI) -> tuple[str, int]:
    """Chiến lược Baseline"""
    start_time = time.time()
    
    system_prompt = "You are provided with a Python function signature. Implement it."
    user_prompt = """
    FUNCTION: {{{ def get_geometric_mean(net_returns: Dict[str, float]) -> float: }}}
    CODE:
    """
    
    completion: ChatCompletion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    
    elapsed = time.time() - start_time
    tokens = completion.usage.total_tokens
    output = completion.choices[0].message.content
    
    return output, tokens, elapsed

def strategy_cot(client: OpenAI) -> tuple[str, int]:
    """Chiến lược Chain of Thought"""
    start_time = time.time()
    
    system_prompt = """You are provided with a Python function signature. 
    Implement it. Think step by step:
    1. Understand the problem
    2. Plan the solution
    3. Write the code"""
    user_prompt = "FUNCTION: {{{ def get_geometric_mean(...) }}} CODE:"
    
    completion: ChatCompletion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    
    elapsed = time.time() - start_time
    tokens = completion.usage.total_tokens
    output = completion.choices[0].message.content
    
    return output, tokens, elapsed

# Gọi các hàm và ghi lại kết quả
if __name__ == '__main__':
    client = OpenAI()
    
    print("=" * 60)
    print("CHIẾU SO SÁNH BA CHIẾN LƯỢC PROMPTING")
    print("=" * 60)
    
    # Baseline
    result_b, tokens_b, time_b = strategy_baseline(client)
    print(f"\n🎯 BASELINE:")
    print(f"   Tokens: {tokens_b}")
    print(f"   Time: {time_b:.2f}s")
    
    # CoT
    result_c, tokens_c, time_c = strategy_cot(client)
    print(f"\n🧠 CHAIN OF THOUGHT:")
    print(f"   Tokens: {tokens_c}")
    print(f"   Time: {time_c:.2f}s")
```

**Câu hỏi phân tích:**
1. Chiến lược nào nhanh nhất? Tại sao?
2. Chiến lược nào sử dụng tokens nhiều nhất?
3. Chất lượng kết quả có khác biệt không?
4. Nếu chạy 100 lần, chi phí sẽ là bao nhiêu?

---

## 🎓 PHẦN 7: KIẾN THỨC VÀ LẼ THẮNG TỔ CHỨC

### Các khái niệm chính

📌 **Prompting** - Cách đặt câu hỏi cho AI  
📌 **Token** - Đơn vị tính giá API (1 token ≈ 4 ký tự)  
📌 **System Message** - Hướng dẫn hệ thống (vai trò, hành vi)  
📌 **User Message** - Lệnh của người dùng  
📌 **Assistant Message** - Phản hồi từ AI  
📌 **Conversational History** - Lịch sử hội thoại (dùng trong Chaining)  

### Công thức chi phí API

```
Chi phí (USD) = (Input tokens × Giá input) + (Output tokens × Giá output)
```

**Ví dụ gpt-4o-mini:**
- Input: $0.00015 / 1K tokens
- Output: $0.0006 / 1K tokens

Nếu sử dụng 1000 input tokens + 500 output tokens:
```
Chi phí = (1000 × 0.00015) + (500 × 0.0006) = 0.15 + 0.3 = $0.45
```

### Best Practices

✅ **Luôn kiểm tra API Key** - Lưu trong `.env`, không hardcode  
✅ **Monitore token usage** - Dùng `completion.usage.total_tokens`  
✅ **Thiết kế prompt cẩn thận** - Tuân thủ 5S (Structured, Surrounding, Single-task, Specific, Short)  
✅ **Kiểm chứng kết quả** - Chạy unit test, không tin tuyệt đối  
✅ **Lựa chọn mô hình phù hợp** - gpt-4o-mini cho bài toán đơn giản, gpt-4o cho bài toán phức tạp  

---

## 📝 TÓM TẮT

### Các bài Lab bắt buộc

| Lab | Tiêu đề | Độ khó |
|---|---|---|
| **9.1** | Baseline Strategy với OpenAI API | ⭐ |
| **9.2** | Baseline Strategy với GitHub Copilot | ⭐ |
| **9.3** | Chain of Thought Strategy | ⭐⭐ |
| **9.4** | Naive Chaining Strategy | ⭐⭐ |
| **9.5** | Selective Chaining Strategy | ⭐⭐ |
| **9.6** | Tổng hợp So sánh Ba Chiến lược | ⭐⭐⭐ |

### Những điều bạn sẽ học được

1. ✨ Hiểu rõ 3 chiến lược prompting chính
2. ✨ Biết khi nào dùng chiến lược nào
3. ✨ Tối ưu hóa chi phí API thông qua lựa chọn chiến lược
4. ✨ Tăng độ chính xác của AI thông qua prompt tốt hơn
5. ✨ Quản lý lịch sử hội thoại (conversational history) cho Chaining
6. ✨ Đo lường hiệu suất và so sánh các phương pháp

---

## 🔗 THAM KHẢO

📚 **Nguồn tài liệu:**
- Supercharged Coding with GenAI - Chapter 9
- OpenAI API Documentation: https://platform.openai.com/docs/
- GitHub Copilot in VS Code: https://docs.github.com/en/copilot

💡 **Gợi ý thêm:**
- Thử nghiệm với các mô hình khác nhau (gpt-4, gpt-4o, o3-mini)
- Tìm hiểu thêm về "Prompt Engineering" (kỹ thuật tối ưu hóa prompt)
- Khám phá các công cụ hỗ trợ prompt builder (LangChain, LLamaIndex)

---

**🎯 Hãy bắt đầu từ Lab 9.1 và lần lượt hoàn thành các bài tập. Chúc bạn thành công! 🚀**
