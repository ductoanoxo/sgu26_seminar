"""
Lab 15.2: Timing Decorator - Đo hiệu suất

Mục tiêu:
- Tạo decorator để đo thời gian thực thi hàm
- So sánh hiệu suất giữa các cách triển khai
- Hiểu decorator với arguments (parameterized decorator)

Parameterized Decorator Pattern:
@timer(unit='ms')
def func(): pass

# Thực chất là:
timer_instance = timer(unit='ms')
@timer_instance
def func(): pass
"""

import time
import functools
from typing import Callable, Any
from pathlib import Path

# ===== DECORATOR TIMING - PHIÊN BẢN ĐƠNG GIẢN =====
def timer_simple(func: Callable) -> Callable:
    """
    Decorator đơn giản: đo thời gian thực thi hàm
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        elapsed = end_time - start_time
        print(f"⏱️  {func.__name__} took {elapsed:.6f} seconds")
        
        return result
    
    return wrapper


# ===== DECORATOR TIMING - PHIÊN BẢN NÂNG CAO (CÓ ARGUMENTS) =====
def timer_advanced(unit: str = 'seconds', display: bool = True):
    """
    Decorator timing nâng cao: có thể tùy chỉnh đơn vị và hiển thị.
    
    Args:
        unit: Đơn vị thời gian ('seconds', 'ms', 'us')
        display: Có hiển thị kết quả không
    
    Returns:
        Hàm decorator
    
    Ví dụ:
        @timer_advanced(unit='ms')
        def my_func(): pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            
            elapsed = end - start
            
            # Chuyển đổi đơn vị
            if unit == 'ms':
                elapsed = elapsed * 1000
                unit_str = 'ms'
            elif unit == 'us':
                elapsed = elapsed * 1_000_000
                unit_str = 'µs'
            else:
                unit_str = 's'
            
            if display:
                print(f"⏱️  {func.__name__} took {elapsed:.4f} {unit_str}")
            
            return result
        
        return wrapper
    
    return decorator


# ===== DECORATOR TIMING - PHIÊN BẢN LOG VÀO FILE =====
def timer_with_log(log_file: str = "timings.log"):
    """
    Decorator timing với ghi vào file.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            
            elapsed = end - start
            log_line = f"{func.__name__}: {elapsed:.6f}s\n"
            
            # Ghi vào file
            with open(log_file, 'a') as f:
                f.write(log_line)
            
            print(f"⏱️  {func.__name__} took {elapsed:.6f}s (logged to {log_file})")
            return result
        
        return wrapper
    
    return decorator


# ===== HÀM TEST =====

@timer_simple
def fibonacci_slow(n: int) -> int:
    """Fibonacci sử dụng đệ quy (chậm)"""
    if n <= 1:
        return n
    return fibonacci_slow(n-1) + fibonacci_slow(n-2)


@timer_advanced(unit='ms', display=True)
def fibonacci_fast(n: int) -> int:
    """Fibonacci sử dụng lập trình động (nhanh)"""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


@timer_advanced(unit='us')
def quick_operation() -> int:
    """Phép toán nhanh (microseconds)"""
    return sum(range(1000))


@timer_with_log()
def slow_operation():
    """Phép toán chậm (ghi log)"""
    time.sleep(0.1)
    return "Done"


# ===== SO SÁNH HIỆU SUẤT =====
def performance_comparison():
    """So sánh hiệu suất: Slow vs Fast"""
    print("\n" + "=" * 70)
    print("📊 SO SÁNH HIỆU SUẤT: Fibonacci Slow vs Fast")
    print("=" * 70)
    
    n = 30
    
    print(f"\n▶️ Fibonacci Slow (n={n}):")
    result_slow = fibonacci_slow(n)
    
    print(f"\n▶️ Fibonacci Fast (n={n}):")
    result_fast = fibonacci_fast(n)
    
    print(f"\n✅ Cả hai cho kết quả: {result_slow} = {result_fast}")
    print("💡 Nhưng Fast nhanh hơn rất nhiều lần!")
    print("=" * 70)


# ===== LAB 15.2 CHÍNH =====
def run_lab():
    print("\n" + "=" * 70)
    print("🧪 LAB 15.2: TIMING DECORATOR")
    print("=" * 70)
    
    print("\n✅ Test 1: Timer Simple")
    fibonacci_slow(20)
    
    print("\n✅ Test 2: Timer Advanced (milliseconds)")
    fibonacci_fast(30)
    
    print("\n✅ Test 3: Timer Advanced (microseconds)")
    result = quick_operation()
    
    print("\n✅ Test 4: Timer with Log File")
    slow_operation()
    slow_operation()
    slow_operation()
    
    # Hiển thị file log
    log_file = Path("timings.log")
    if log_file.exists():
        print(f"\n📄 Nội dung {log_file}:")
        print(log_file.read_text())
        log_file.unlink()  # Xóa file sau test
    
    performance_comparison()
    
    print("\n" + "=" * 70)
    print("🎉 LAB 15.2 HOÀN THÀNH! 🎉")
    print("=" * 70)


if __name__ == "__main__":
    run_lab()
