# 📚 CHƯƠNG 15: DECORATORS & GEMINI API

Dưới đây là bản hướng dẫn chi tiết, chuyên sâu và được trình bày trực quan về **Chương 15: Decorators & Fine-tuning** từ cuốn sách "Supercharged Coding with GenAI", được điều chỉnh để sử dụng **Google Gemini API** thay vì OpenAI.

Chương này tập trung vào **hai kỹ thuật nâng cao:**
1. 🎨 **Decorators** - Trang trí hàm/lớp Python
2. 🚀 **Gemini API** - Sử dụng mô hình AI của Google

---

## 🌟 TỔNG QUAN DECORATORS

### Decorator là gì?

**Decorator** (trang trí) là một hàm cao cấp (higher-order function) trong Python cho phép bạn:
- ✅ **Bao bọc** một hàm khác
- ✅ **Mở rộng chức năng** mà không sửa mã gốc
- ✅ **Tái sử dụng logic** cho nhiều hàm

**Típ dụ cơ bản:**
```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Trước khi gọi hàm")
        result = func(*args, **kwargs)
        print("Sau khi gọi hàm")
        return result
    return wrapper

@my_decorator
def say_hello(name):
    print(f"Hello {name}")

say_hello("Alice")  # In ra: "Trước khi gọi hàm" → "Hello Alice" → "Sau khi gọi hàm"
```

### 💡 Tại sao dùng Decorators?

| Lợi ích | Ví dụ |
|---------|-------|
| 📊 **Logging** | Ghi lại who, when, what |
| ⏱️ **Timing** | Đo hiệu suất hàm |
| ✅ **Validation** | Kiểm tra arguments trước gọi |
| 🔐 **Authorization** | Kiểm tra quyền trước thực thi |
| 💾 **Caching** | Lưu kết quả để tái sử dụng |

---

## 🎯 PHẦN 1: GEMINI API - GIỚI THIỆU

### Gemini là mô hình AI gì?

**Gemini** là mô hình AI đa phương tiện của Google:
- 🔤 Xử lý **Text** (tạo code, viết văn bản)
- 🖼️ Xử lý **Image** (phân tích ảnh)
- 🎵 Xử lý **Audio** (xử lý âm thanh)

**So sánh Gemini vs OpenAI:**

| Tiêu chí | Gemini (Google) | GPT-4o (OpenAI) |
|---------|-----------------|-----------------|
| 💰 Giá | Miễn phí (100 calls/min) | $0.15 per 1M tokens |
| 🚀 Tốc độ | Nhanh | Chuẩn |
| 📝 Context Window | 1M tokens | 128K tokens |
| 🎨 Khả năng | Tốt | Rất tốt |
| 🔧 Dễ dùng | Rất dễ | Dễ |

### Lợi thế của Gemini:
✅ **Hoàn toàn miễn phí** - Không cần nạp tiền  
✅ **API key dễ lấy** - Không cần card tín dụng  
✅ **Quota cao** - 100 requests/phút  
✅ **Multi-modal** - Hỗ trợ text, image, audio  

---

## 🔑 PHẦN 2: THIẾT LẬP GEMINI API

### Bước 1: Lấy API Key

1. Truy cập: https://aistudio.google.com/app/apikey
2. Click **"Create API Key in new project"**
3. Chọn **"Google AI Studio"** hoặc **"Existing project"**
4. Copy API key (dạng: `AIza...`)

### Bước 2: Thiết lập Environment

File `.env` đã được tạo sẵn:
```
GEMINI_API_KEY=AIzaSyCTYxrHmmPoA_h_OUvtZyr4zajmpGpmr7o
```

### Bước 3: Cài đặt Package

```bash
pip install google-generativeai python-dotenv
```

---

## 🎨 PHẦN 3: DECORATOR BASICS - LAB 15.1

### Bài tập 1: Decorator Logging

**Mục tiêu:** Viết decorator để ghi lại thông tin hàm khi được gọi

**Lab 15.1: log_function_decorator.py**

```python
import logging
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_function_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        logger.info(f"Result: {result}")
        return result
    return wrapper

@log_function_calls
def add(a, b):
    return a + b

# Test
add(2, 3)  # In ra: Calling add with args=(2, 3), kwargs={}, Result: 5
```

---

## ⏱️ PHẦN 4: DECORATOR TIMING - LAB 15.2

### Bài tập 2: Decorator đo hiệu suất

**Mục tiêu:** Tạo decorator để đo thời gian thực thi hàm

**Lab 15.2: timing_decorator.py**

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "Done"

slow_function()  # In ra: slow_function took 1.0001 seconds
```

---

## ✅ PHẦN 5: VALIDATION DECORATOR - LAB 15.3

### Bài tập 3: Decorator validation

**Mục tiêu:** Tạo decorator để kiểm tra loại dữ liệu và giá trị hợp lệ

**Lab 15.3: validation_decorator.py**

```python
from functools import wraps

def validate_types(arg_types):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg, expected_type in zip(args, arg_types):
                if not isinstance(arg, expected_type):
                    raise TypeError(f"Expected {expected_type}, got {type(arg)}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types([int, int])
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

divide(10, 2)    # ✅ OK: 5.0
divide("10", 2)  # ❌ Error: Expected <class 'int'>, got <class 'str'>
```

---

## 🚀 PHẦN 6: GEMINI INTEGRATION - LAB 15.4

### Bài tập 4: Sử dụng Gemini API để sinh decorator

**Mục tiêu:** Dùng Gemini API để tự động tạo code decorators

**Lab 15.4: gemini_decorator_generator.py**

```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

def generate_decorator_with_gemini(decorator_name: str, description: str):
    """Sử dụng Gemini tạo decorator code"""
    
    prompt = f"""
    Create a Python decorator named '{decorator_name}' that {description}
    
    Requirements:
    1. Use functools.wraps
    2. Add type hints
    3. Include docstring
    4. Return callable
    
    Only provide Python code, no explanation.
    """
    
    response = model.generate_content(prompt)
    return response.text

# Ví dụ: Gemini tạo cache decorator
code = generate_decorator_with_gemini(
    "cache_decorator",
    "caches function results to avoid redundant computations"
)

print(code)
```

**Kết quả mong đợi:**
```python
from functools import wraps

def cache_decorator(func):
    """Caches the return value of a function"""
    cache = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    return wrapper
```

---

## 🎪 PHẦN 7: MULTIPLE DECORATORS - LAB 15.5

### Bài tập 5: FizzBuzz với nhiều decorators

**Mục tiêu:** Áp dụng vài decorators trên cùng một hàm

**Lab 15.5: fizzbuzz_decorators.py**

```python
import logging
import time
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FIZZBUZZ_COUNTER = 0

def log_function_args(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"{func.__name__} called with args={args}")
        return func(*args, **kwargs)
    return wrapper

def increment_counter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global FIZZBUZZ_COUNTER
        FIZZBUZZ_COUNTER += 1
        logger.info(f"Call #{FIZZBUZZ_COUNTER}")
        return func(*args, **kwargs)
    return wrapper

def validate_args_types_and_limits(min_val: int, max_val: int):
    def decorator(func):
        @wraps(func)
        def wrapper(limit: int):
            if not isinstance(limit, int):
                raise TypeError(f"limit must be int, got {type(limit)}")
            if not (min_val <= limit <= max_val):
                raise ValueError(f"limit must be {min_val}-{max_val}, got {limit}")
            return func(limit)
        return wrapper
    return decorator

# Áp dụng 3 decorators
@log_function_args
@increment_counter
@validate_args_types_and_limits(0, 100)
def print_fizzbuzz(limit: int) -> None:
    for i in range(1, limit + 1):
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)

# Test
print_fizzbuzz(15)
print_fizzbuzz(20)

print(f"Tổng gọi hàm: {FIZZBUZZ_COUNTER}")
```

**Thứ tự decorator:**
```
@log_function_args       ← Layer 3 (ngoài cùng)
@increment_counter       ← Layer 2
@validate_args           ← Layer 1 (trong cùng)
def print_fizzbuzz(limit):
    ...

Khi gọi: print_fizzbuzz(15)
Thứ tự thực thi: Layer 3 → Layer 2 → Layer 1 → hàm gốc
```

---

## 🤖 PHẦN 8: GEMINI CHAIN - LAB 15.6

### Bài tập 6: Sử dụng Gemini để phân tích decorators

**Mục tiêu:** Dùng Gemini để giải thích và cải thiện decorator code

**Lab 15.6: gemini_decorator_analysis.py**

```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

def analyze_decorator_with_gemini(code: str, question: str):
    """Dùng Gemini phân tích decorator code"""
    
    prompt = f"""
    Analyze this Python decorator code:
    
    ```python
    {code}
    ```
    
    Question: {question}
    
    Provide a clear, concise explanation.
    """
    
    response = model.generate_content(prompt)
    return response.text

# Ví dụ
decorator_code = """
def cache_decorator(func):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper
"""

explanation = analyze_decorator_with_gemini(
    decorator_code,
    "What are potential issues with this caching decorator?"
)

print(explanation)
```

---

## 📊 PHẦN 9: SO SÁNH - LAB 15.7

### Bài tập 7: So sánh cách triển khai

**Mục tiêu:** So sánh: hand-written vs Gemini-generated decorators

**Lab 15.7: comparison.py**

```python
import time
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def time_execution(label: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            print(f"{label}: {elapsed:.6f}s")
            return result
        return wrapper
    return decorator

# Cách 1: Hand-written
@time_execution("Hand-written")
def my_function_manual():
    return sum(range(1000000))

# Cách 2: Gemini-generated
prompt = "Create a memoization decorator for expensive functions in one line"
# ... (call Gemini)

# So sánh
print("=== COMPARISON ===")
my_function_manual()
```

---

## 📋 TÓM TẮT CÁC BÀI LAB

| Lab | Tiêu đề | API | Độ khó |
|-----|---------|-----|---------|
| **15.1** | Decorator Logging | ❌ | ⭐ |
| **15.2** | Timing Decorator | ❌ | ⭐ |
| **15.3** | Validation Decorator | ❌ | ⭐ |
| **15.4** | Gemini Decorator Generator | ✅ Gemini | ⭐⭐ |
| **15.5** | FizzBuzz Multiple Decorators | ❌ | ⭐⭐ |
| **15.6** | Gemini Analysis | ✅ Gemini | ⭐⭐ |
| **15.7** | Comparison | ✅ Gemini | ⭐⭐⭐ |

---

## 🎓 KIẾN THỨC CHÍNH

### Khái niệm cơ bản
- 🎨 **Decorator** = hàm bao bọc hàm khác
- 🔗 **functools.wraps** = giữ nguyên metadata hàm gốc
- 📚 **Higher-order function** = hàm nhận/trả hàm
- 🚀 **Gemini API** = AI của Google, miễn phí

### Best Practices
✅ Luôn dùng `@wraps` để giữ `__name__`, `__doc__`  
✅ Tránh side effects không mong muốn  
✅ Viết docstring cho decorator  
✅ Test decorator với args/kwargs khác nhau  

### Common Patterns
```python
# 1. Simple decorator
@decorator
def func(): pass

# 2. Decorator with arguments
@decorator(arg1, arg2)
def func(): pass

# 3. Multiple decorators (execution order: bottom-up)
@decorator_1
@decorator_2
@decorator_3
def func(): pass
# Thực thi: decorator_3 → decorator_2 → decorator_1 → func
```

---

## 💡 GEMINI API - TIPS

### Lợi thế
✅ Hoàn toàn miễn phí  
✅ Không cần card tín dụng  
✅ 100 requests/phút (đủ cho học tập)  
✅ Multi-modal (text, image, audio)  

### Hạn chế
⚠️ Quota không cao cho production  
⚠️ Response có thể chậm hơn OpenAI  
⚠️ Documentation ít hơn OpenAI  

---

## 📚 THAM KHẢO

📖 **Python Decorators:**
- https://docs.python.org/3/glossary.html#term-decorator
- https://docs.python.org/3/library/functools.html

🤖 **Google Gemini:**
- https://ai.google.dev/
- https://ai.google.dev/tutorials/python_quickstart

📊 **So sánh AI Models:**
- https://ai.google.dev/models/  
- https://platform.openai.com/docs/models

---

**🎯 Hãy bắt đầu từ Lab 15.1 và lần lượt hoàn thành các bài tập. Chúc bạn thành công! 🚀**
