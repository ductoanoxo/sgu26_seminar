"""
Lab 15.6: Gemini Decorator Analysis

Mục tiêu:
- Dùng Gemini API để phân tích và cải thiện decorator code
- Tạo interactive Q&A session với Gemini
- Demo chế độ fallback khi hết quota

Capabilities:
1. Giải thích decorator code
2. Tìm ra potential issues
3. Gợi ý cải thiện
4. Tạo test cases
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

# ===== DEMO FALLBACK RESPONSES =====
DEMO_EXPLANATION = """
This cache decorator implements a simple memoization pattern:

1. **Cache Dictionary**: Maintains a dictionary to store previous results
2. **Key Generation**: Uses (args, kwargs) as the cache key
3. **Hit/Miss Logic**: Checks if result is cached, if yes returns it, else computes
4. **functools.wraps**: Preserves the original function metadata

Potential Issues:
- Memory leak for infinite argument combinations
- Not thread-safe for concurrent calls
- Cache never expires
- No size limit on cache dictionary
"""

DEMO_ISSUES = """
Critical Issues:
1. **Memory Leak**: Cache grows indefinitely with unique arguments
2. **Thread Safety**: Not safe for concurrent access
3. **No Expiration**: Cached values never expire

Recommendations:
1. Add maxsize parameter with LRU eviction
2. Use threading.Lock for thread safety
3. Add TTL (time-to-live) for cache entries
4. Add cache hit/miss statistics
"""

DEMO_IMPROVEMENT = """
from functools import wraps, lru_cache
from typing import Callable, Any
import threading

@lru_cache(maxsize=128)
def improved_cache(func: Callable) -> Callable:
    '''Thread-safe caching with LRU eviction'''
    cache = {}
    lock = threading.Lock()
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        
        with lock:
            if key in cache:
                return cache[key]
            
            result = func(*args, **kwargs)
            cache[key] = result
            return result
    
    return wrapper
"""

DEMO_TESTS = """
def test_cache_decorator():
    '''Comprehensive tests for cache decorator'''
    
    call_count = 0
    
    @cache_decorator
    def expensive_function(x):
        nonlocal call_count
        call_count += 1
        return x ** 2
    
    # Test 1: First call should compute
    result1 = expensive_function(5)
    assert result1 == 25
    assert call_count == 1
    
    # Test 2: Second call should use cache
    result2 = expensive_function(5)
    assert result2 == 25
    assert call_count == 1  # Not incremented
    
    # Test 3: Different argument should compute
    result3 = expensive_function(10)
    assert result3 == 100
    assert call_count == 2
    
    print("✅ All tests passed!")
"""


try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️  google-generativeai not installed")


# ===== GEMINI ANALYSIS FUNCTIONS =====
def setup_gemini(api_key: Optional[str] = None):
    """Thiết lập Gemini client"""
    if not GEMINI_AVAILABLE:
        return None
    
    load_dotenv()
    key = api_key or os.getenv("GEMINI_API_KEY")
    
    if not key:
        print("⚠️  GEMINI_API_KEY not found")
        return None
    
    genai.configure(api_key=key)
    return genai.GenerativeModel("gemini-pro")


def explain_decorator(code: str, model=None) -> str:
    """Gemini giải thích decorator code"""
    if not model:
        print("🎬 DEMO MODE")
        return DEMO_EXPLANATION
    
    prompt = f"""Analyze and explain this Python decorator in detail:

```python
{code}
```

Provide:
1. What it does
2. How it works (step by step)
3. Key components
4. Use cases
"""
    
    try:
        print("⏳ Gọi Gemini để giải thích...")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return DEMO_EXPLANATION


def find_issues(code: str, model=None) -> str:
    """Gemini tìm potential issues"""
    if not model:
        print("🎬 DEMO MODE")
        return DEMO_ISSUES
    
    prompt = f"""Identify potential issues, bugs, and performance problems in this decorator:

```python
{code}
```

Provide:
1. Critical issues
2. Performance concerns
3. Security risks
4. Best practice violations
"""
    
    try:
        print("⏳ Gọi Gemini để tìm issues...")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return DEMO_ISSUES


def suggest_improvement(code: str, model=None) -> str:
    """Gemini gợi ý cải thiện"""
    if not model:
        print("🎬 DEMO MODE")
        return DEMO_IMPROVEMENT
    
    prompt = f"""Improve this decorator code addressing identified issues:

```python
{code}
```

Provide:
1. Improved version with comments
2. Added features (thread safety, limits, etc.)
3. Explanation of changes
4. Performance gains
"""
    
    try:
        print("⏳ Gọi Gemini để gợi ý cải thiện...")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return DEMO_IMPROVEMENT


def generate_tests(code: str, model=None) -> str:
    """Gemini tạo test cases"""
    if not model:
        print("🎬 DEMO MODE")
        return DEMO_TESTS
    
    prompt = f"""Generate comprehensive test cases for this decorator:

```python
{code}
```

Provide:
1. Unit tests
2. Edge case tests
3. Performance tests
4. Error handling tests
"""
    
    try:
        print("⏳ Gọi Gemini để tạo tests...")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return DEMO_TESTS


# ===== DECORATOR MẪU ĐỂ PHÂN TÍCH =====
SAMPLE_DECORATOR = """from functools import wraps
from typing import Callable, Any, Dict

def cache_decorator(func: Callable) -> Callable:
    '''Simple caching decorator'''
    cache: Dict = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        key = (args, tuple(kwargs.items()))
        
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        
        return cache[key]
    
    return wrapper
"""


# ===== MAIN LAB =====
def run_lab():
    """Chạy Lab 15.6"""
    print("\n" + "=" * 70)
    print("🧪 LAB 15.6: GEMINI DECORATOR ANALYSIS")
    print("=" * 70)
    
    model = setup_gemini()
    
    print(f"\n⚙️ Mode: {'API' if model else 'DEMO'}")
    print(f"📊 Gemini Available: {GEMINI_AVAILABLE}")
    
    print("\n" + "=" * 70)
    print("📝 SAMPLE DECORATOR TO ANALYZE:")
    print("=" * 70)
    print(SAMPLE_DECORATOR)
    
    # Step 1: Giải thích
    print("\n" + "=" * 70)
    print("1️⃣ STEP 1: EXPLANATION")
    print("=" * 70)
    explanation = explain_decorator(SAMPLE_DECORATOR, model)
    print(explanation)
    
    with open("lab156_explanation.txt", "w", encoding='utf-8') as f:
        f.write(explanation)
    print("\n💾 Saved to: lab156_explanation.txt")
    
    # Step 2: Tìm issues
    print("\n" + "=" * 70)
    print("2️⃣ STEP 2: IDENTIFY ISSUES")
    print("=" * 70)
    issues = find_issues(SAMPLE_DECORATOR, model)
    print(issues)
    
    with open("lab156_issues.txt", "w", encoding='utf-8') as f:
        f.write(issues)
    print("\n💾 Saved to: lab156_issues.txt")
    
    # Step 3: Gợi ý cải thiện
    print("\n" + "=" * 70)
    print("3️⃣ STEP 3: IMPROVEMENTS")
    print("=" * 70)
    improvement = suggest_improvement(SAMPLE_DECORATOR, model)
    print(improvement)
    
    with open("lab156_improved.py", "w", encoding='utf-8') as f:
        f.write(improvement)
    print("\n💾 Saved to: lab156_improved.py")
    
    # Step 4: Tạo tests
    print("\n" + "=" * 70)
    print("4️⃣ STEP 4: GENERATE TESTS")
    print("=" * 70)
    tests = generate_tests(SAMPLE_DECORATOR, model)
    print(tests)
    
    with open("lab156_tests.py", "w", encoding='utf-8') as f:
        f.write(tests)
    print("\n💾 Saved to: lab156_tests.py")
    
    print("\n" + "=" * 70)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 70)
    print("\nFiles created:")
    print("  - lab156_explanation.txt")
    print("  - lab156_issues.txt")
    print("  - lab156_improved.py")
    print("  - lab156_tests.py")
    
    print("\n" + "=" * 70)
    print("🎉 LAB 15.6 HOÀN THÀNH! 🎉")
    print("=" * 70)


if __name__ == "__main__":
    run_lab()
