"""
Lab 15.3: Validation Decorator - Kiểm tra dữ liệu

Mục tiêu:
- Tạo decorator để kiểm tra loại dữ liệu (type validation)
- Kiểm tra giá trị (value validation)
- Tạo decorator factory cho tái sử dụng

Validation Patterns:
1. Type checking - Kiểm tra kiểu dữ liệu
2. Range checking - Kiểm tra công thức
3. Custom validation - Kiểm tra tùy chỉnh
"""

import functools
from typing import Callable, Any, Tuple, Type, Dict, List


# ===== DECORATOR 1: TYPE VALIDATION =====
def validate_types(*expected_types: Type):
    """
    Decorator kiểm tra loại dữ liệu của arguments.
    
    Args:
        *expected_types: Loại dữ liệu kỳ vọng (theo thứ tự args)
    
    Ví dụ:
        @validate_types(int, int)
        def add(a, b): pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Kiểm tra số lượng arguments
            if len(args) < len(expected_types):
                raise TypeError(
                    f"{func.__name__} expects at least {len(expected_types)} args, "
                    f"got {len(args)}"
                )
            
            # Kiểm tra loại từng arg
            for i, (arg, expected_type) in enumerate(zip(args, expected_types)):
                if not isinstance(arg, expected_type):
                    raise TypeError(
                        f"Argument {i} ({arg!r}) must be {expected_type.__name__}, "
                        f"got {type(arg).__name__}"
                    )
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


# ===== DECORATOR 2: RANGE VALIDATION =====
def validate_range(arg_ranges: Dict[int, Tuple[float, float]]):
    """
    Decorator kiểm tra giá trị nằm trong phạm vi.
    
    Args:
        arg_ranges: Dict {arg_index: (min, max)}
    
    Ví dụ:
        @validate_range({0: (0, 100), 1: (0, 100)})
        def set_brightness(brightness, contrast): pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for arg_idx, (min_val, max_val) in arg_ranges.items():
                if arg_idx < len(args):
                    arg_value = args[arg_idx]
                    if not (min_val <= arg_value <= max_val):
                        raise ValueError(
                            f"Argument {arg_idx} must be between {min_val}-{max_val}, "
                            f"got {arg_value}"
                        )
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


# ===== DECORATOR 3: CUSTOM VALIDATION =====
def validate_custom(**validators: Dict[str, Callable]):
    """
    Decorator với custom validation logic.
    
    Args:
        **validators: {arg_name: validation_function}
        
    Ví dụ:
        def is_even(n): return n % 2 == 0
        
        @validate_custom(number=is_even)
        def process_even(number): pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Gộp kwargs vào
            all_kwargs = {**kwargs}
            
            # Kiểm tra từng validator
            for arg_name, validator in validators.items():
                if arg_name in all_kwargs:
                    value = all_kwargs[arg_name]
                    if not validator(value):
                        raise ValueError(
                            f"Validation failed for '{arg_name}={value}': "
                            f"{validator.__name__} returned False"
                        )
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


# ===== HÀM TEST =====

@validate_types(int, int)
def add(a: int, b: int) -> int:
    """Cộng hai số nguyên"""
    return a + b


@validate_types(float, float)
def divide(a: float, b: float) -> float:
    """Chia hai số thực"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


@validate_range({0: (0, 100), 1: (0, 100)})
def set_brightness(brightness: int, contrast: int) -> str:
    """Đặt độ sáng và độ tương phản (0-100)"""
    return f"Brightness={brightness}, Contrast={contrast}"


def is_even(n: int) -> bool:
    """Kiểm tra số chẵn"""
    return n % 2 == 0

def is_positive(n: int) -> bool:
    """Kiểm tra số dương"""
    return n > 0

@validate_custom(number=is_even, multiplier=is_positive)
def multiply_even(number: int, multiplier: int) -> int:
    """Nhân một số chẵn với một số dương"""
    return number * multiplier


# ===== DEMONSTRATION =====
def run_tests():
    print("\n" + "=" * 70)
    print("🧪 LAB 15.3: VALIDATION DECORATOR")
    print("=" * 70)
    
    # Test 1: Type validation - PASS
    print("\n✅ Test 1: Type Validation (PASS)")
    result1 = add(2, 3)
    print(f"   add(2, 3) = {result1}")
    
    # Test 2: Type validation - FAIL
    print("\n❌ Test 2: Type Validation (FAIL)")
    try:
        result2 = add("2", 3)
    except TypeError as e:
        print(f"   ✓ Caught error: {e}")
    
    # Test 3: Range validation - PASS
    print("\n✅ Test 3: Range Validation (PASS)")
    result3 = set_brightness(50, 75)
    print(f"   set_brightness(50, 75) = '{result3}'")
    
    # Test 4: Range validation - FAIL
    print("\n❌ Test 4: Range Validation (FAIL)")
    try:
        result4 = set_brightness(150, 50)
    except ValueError as e:
        print(f"   ✓ Caught error: {e}")
    
    # Test 5: Custom validation - PASS
    print("\n✅ Test 5: Custom Validation (PASS)")
    result5 = multiply_even(4, 5)
    print(f"   multiply_even(4, 5) = {result5}")
    
    # Test 6: Custom validation - FAIL (odd number)
    print("\n❌ Test 6: Custom Validation (FAIL - odd number)")
    try:
        result6 = multiply_even(3, 5)
    except ValueError as e:
        print(f"   ✓ Caught error: {e}")
    
    # Test 7: Custom validation - FAIL (negative multiplier)
    print("\n❌ Test 7: Custom Validation (FAIL - negative multiplier)")
    try:
        result7 = multiply_even(4, -5)
    except ValueError as e:
        print(f"   ✓ Caught error: {e}")
    
    print("\n" + "=" * 70)
    print("🎉 LAB 15.3 HOÀN THÀNH! 🎉")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
