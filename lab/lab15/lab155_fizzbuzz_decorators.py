"""
Lab 15.5: FizzBuzz với Multiple Decorators

Mục tiêu:
- Áp dụng nhiều decorators trên cùng một hàm
- Hiểu thứ tự thực thi decorators (bottom-up)
- Tạo decorator reusable và composable

Thứ tự Decorator:
@decorator_1      <- Layer 3 (ngoài cùng - thực thi cuối)
@decorator_2      <- Layer 2
@decorator_3      <- Layer 1 (trong cùng - thực thi đầu)
def func():
    ...

Khi gọi func():
Thực thi: decorator_1.__enter__ → decorator_2.__enter__ → 
          decorator_3.__enter__ → func() → decorator_3.__exit__ → 
          decorator_2.__exit__ → decorator_1.__exit__
"""

import logging
import time
from functools import wraps
from typing import Callable, Any

# ===== SETUP LOGGING =====
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-8s | %(message)s"
)
logger = logging.getLogger(__name__)


# ===== COUNTER GLOBAL =====
FIZZBUZZ_CALL_COUNT = 0


# ===== DECORATOR 1: Logging =====
def log_function_args(func: Callable) -> Callable:
    """Log arguments khi hàm được gọi"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"📞 Calling {func.__name__}(args={args}, kwargs={kwargs})")
        result = func(*args, **kwargs)
        logger.info(f"✅ {func.__name__} completed successfully")
        return result
    return wrapper


# ===== DECORATOR 2: Counter =====
def increment_counter(func: Callable) -> Callable:
    """Tăng counter mỗi lần gọi hàm"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        global FIZZBUZZ_CALL_COUNT
        FIZZBUZZ_CALL_COUNT += 1
        logger.info(f"📊 Call #{FIZZBUZZ_CALL_COUNT}")
        return func(*args, **kwargs)
    return wrapper


# ===== DECORATOR 3: Validation (Parameterized) =====
def validate_args_types_and_limits(min_limit: int, max_limit: int) -> Callable:
    """
    Decorator validate type và range của arguments
    
    Args:
        min_limit: Giá trị tối thiểu
        max_limit: Giá trị tối đa
    
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(limit: int):
            # Type check
            if not isinstance(limit, int):
                logger.error(f"❌ TypeError: limit must be int, got {type(limit).__name__}")
                raise TypeError(f"Argument 'limit' must be int, got {type(limit).__name__}")
            
            # Range check
            if not (min_limit <= limit <= max_limit):
                logger.error(f"❌ ValueError: limit must be {min_limit}-{max_limit}, got {limit}")
                raise ValueError(
                    f"Argument 'limit' must be between {min_limit} and {max_limit}, got {limit}"
                )
            
            logger.info(f"✓ Validation passed: {min_limit} <= {limit} <= {max_limit}")
            return func(limit)
        
        return wrapper
    
    return decorator


# ===== DECORATOR 4: Timing (Bonus) =====
def timer_decorator(func: Callable) -> Callable:
    """Đo thời gian thực thi"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(f"⏱️  Execution time: {elapsed:.4f}s")
        return result
    return wrapper


# ===== HÀM FIZZBUZZ VỚI MULTIPLE DECORATORS =====
@timer_decorator              # Layer 4 (execute last)
@log_function_args            # Layer 3
@increment_counter            # Layer 2
@validate_args_types_and_limits(0, 100)  # Layer 1 (execute first)
def print_fizzbuzz(limit: int) -> None:
    """
    In ra FizzBuzz từ 1 đến limit
    
    - 3 倍 số: "Fizz"
    - 5 倍 số: "Buzz"
    - 15 倍 số: "FizzBuzz"
    - Khác: In số
    
    Args:
        limit: Giới hạn trên (0-100)
    """
    logger.info(f"🔵 Starting FizzBuzz from 1 to {limit}")
    
    for i in range(1, limit + 1):
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)


# ===== DEMO & TEST =====
def demonstrate_decorator_order():
    """Minh họa thứ tự thực thi decorators"""
    print("\n" + "=" * 70)
    print("📋 THỨ TỰ THỰC TỰ DECORATOR")
    print("=" * 70)
    print("""
Decorator Stack (ngàn ngoài ra trong):
    @timer_decorator         (Layer 4 - in ngoài cùng)
    @log_function_args       (Layer 3)
    @increment_counter       (Layer 2)
    @validate_args           (Layer 1 - gọi trong cùng)
    def print_fizzbuzz():
        ...

Thứ tự THỰC thi khi gọi print_fizzbuzz(5):
    1. timer_decorator.wrapper() bắt đầu ⏱️
    2. log_function_args.wrapper() bắt đầu 📞
    3. increment_counter.wrapper() bắt đầu 📊
    4. validate_args.wrapper() kiểm tra ✓
    5. print_fizzbuzz(5) thực thi chính ⚙️
    6. increment_counter.wrapper() kết thúc 📊
    7. log_function_args.wrapper() kết thúc 📞
    8. timer_decorator.wrapper() kết thúc ⏱️
""")


def run_tests():
    """Chạy các bài kiểm thử"""
    print("\n" + "=" * 70)
    print("🧪 LAB 15.5: MULTIPLE DECORATORS")
    print("=" * 70)
    
    demonstrate_decorator_order()
    
    # Test 1: Normal case
    print("\n" + "=" * 70)
    print("✅ TEST 1: print_fizzbuzz(5) - Normal")
    print("=" * 70)
    print_fizzbuzz(5)
    
    # Test 2: Type error
    print("\n" + "=" * 70)
    print("❌ TEST 2: print_fizzbuzz('5') - Type Error")
    print("=" * 70)
    try:
        print_fizzbuzz("5")
    except TypeError as e:
        logger.error(f"✓ Caught: {e}")
    
    # Test 3: Range error
    print("\n" + "=" * 70)
    print("❌ TEST 3: print_fizzbuzz(150) - Range Error")
    print("=" * 70)
    try:
        print_fizzbuzz(150)
    except ValueError as e:
        logger.error(f"✓ Caught: {e}")
    
    # Test 4: Larger range
    print("\n" + "=" * 70)
    print("✅ TEST 4: print_fizzbuzz(15) - Larger Range")
    print("=" * 70)
    print_fizzbuzz(15)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 THỐNG KỀ")
    print("=" * 70)
    print(f"Tổng số lần gọi hàm: {FIZZBUZZ_CALL_COUNT}")
    print(f"Successful calls: {FIZZBUZZ_CALL_COUNT - 2}")  # Trừ 2 lần lỗi
    print(f"Failed calls: 2")
    
    print("\n" + "=" * 70)
    print("🎉 LAB 15.5 HOÀN THÀNH! 🎉")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
