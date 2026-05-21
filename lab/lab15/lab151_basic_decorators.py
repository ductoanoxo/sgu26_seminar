"""
Lab 15.1: Decorator Logging - Cơ bản

Mục tiêu:
- Hiểu khái niệm Decorator trong Python
- Tạo decorator để ghi lại thông tin hàm khi được gọi
- Sử dụng functools.wraps để giữ metadata hàm gốc

Decorator là gì?
- Một hàm bao bọc hàm khác để mở rộng chức năng
- Không sửa đổi mã gốc của hàm được bao bọc
- Được áp dụng bằng cú pháp @decorator
"""

import logging
from functools import wraps
from typing import Any, Callable

# ===== CẤU HÌNH LOGGING =====
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ===== PHIÊN BẢN 1: DECORATOR ĐƠN GIẢN (không dùng wraps) =====
def log_function_calls_v1(func):
    """
    Phiên bản đơn giản. Lưu ý: Mất thông tin metadata hàm gốc!
    """
    def wrapper(*args, **kwargs):
        logger.info(f"📞 Calling {func.__name__}")
        logger.info(f"   Args: {args}")
        logger.info(f"   Kwargs: {kwargs}")
        
        result = func(*args, **kwargs)
        
        logger.info(f"✅ {func.__name__} returned: {result}")
        return result
    
    return wrapper


# ===== PHIÊN BẢN 2: DECORATOR ĐÚNG CÁCH (dùng wraps) =====
def log_function_calls(func: Callable) -> Callable:
    """
    Decorator logging chính thức. Sử dụng functools.wraps để giữ metadata.
    
    Args:
        func: Hàm muốn bao bọc
    
    Returns:
        Hàm wrapper với chức năng logging thêm
    """
    @wraps(func)  # 🔑 Quan trọng! Giữ __name__, __doc__, __annotations__
    def wrapper(*args, **kwargs):
        logger.info(f"📞 Calling {func.__name__}")
        logger.info(f"   Args: {args}")
        logger.info(f"   Kwargs: {kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.info(f"✅ {func.__name__} returned: {result}")
            return result
        except Exception as e:
            logger.error(f"❌ {func.__name__} raised {type(e).__name__}: {e}")
            raise
    
    return wrapper


# ===== CÁC HÀM THỬ NGHIỆM =====

@log_function_calls
def add(a: int, b: int) -> int:
    """Cộng hai số."""
    return a + b


@log_function_calls
def greet(name: str, greeting: str = "Hello") -> str:
    """Chào hỏi ai đó."""
    return f"{greeting}, {name}!"


@log_function_calls
def divide(a: float, b: float) -> float:
    """Chia hai số (có thể lỗi nếu b=0)."""
    if b == 0:
        raise ValueError("Không thể chia cho 0!")
    return a / b


# ===== SO SÁNH: Có wraps vs Không wraps =====
def compare_wraps():
    """So sánh tác dụng của functools.wraps"""
    print("\n" + "=" * 70)
    print("🔍 SO SÁNH: Decorator với/không wraps")
    print("=" * 70)
    
    @log_function_calls_v1
    def func_without_wraps():
        """Đây là docstring gốc"""
        pass
    
    @log_function_calls
    def func_with_wraps():
        """Đây là docstring gốc"""
        pass
    
    print("\n❌ Decorator V1 (không dùng @wraps):")
    print(f"   func_without_wraps.__name__ = {func_without_wraps.__name__}")  # 'wrapper' ❌ SAI!
    print(f"   func_without_wraps.__doc__ = {func_without_wraps.__doc__}")    # None ❌ SAI!
    
    print("\n✅ Decorator V2 (dùng @wraps):")
    print(f"   func_with_wraps.__name__ = {func_with_wraps.__name__}")        # 'func_with_wraps' ✅ ĐÚNG!
    print(f"   func_with_wraps.__doc__ = {func_with_wraps.__doc__}")          # 'Đây là ...' ✅ ĐÚNG!
    
    print("\n💡 Kết luận: Luôn dùng @wraps để giữ metadata hàm gốc!")
    print("=" * 70)


# ===== KIỂM THỬ =====
def run_tests():
    """Chạy các bài kiểm thử"""
    print("\n" + "=" * 70)
    print("🧪 LAB 15.1: DECORATOR LOGGING")
    print("=" * 70)
    
    # Test 1: Hàm thông thường
    print("\n✅ Test 1: add(2, 3)")
    result = add(2, 3)
    assert result == 5, "add(2, 3) phải bằng 5"
    
    # Test 2: Hàm với kwargs
    print("\n✅ Test 2: greet('Alice', greeting='Hi')")
    result = greet("Alice", greeting="Hi")
    assert result == "Hi, Alice!", "greet phải trả 'Hi, Alice!'"
    
    # Test 3: Hàm có lỗi
    print("\n✅ Test 3: divide(10, 0) - Sẽ lỗi nhưng được logging")
    try:
        divide(10, 0)
    except ValueError as e:
        logger.info(f"✓ Lỗi được catch: {e}")
    
    # So sánh wraps
    compare_wraps()
    
    print("\n" + "=" * 70)
    print("🎉 LAB 15.1 HOÀN THÀNH! 🎉")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
