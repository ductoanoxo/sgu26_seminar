"""
Lab 15.4: Gemini Integration - Sinh Decorator tự động

Mục tiêu:
- Sử dụng Google Gemini API để sinh decorator code tự động
- So sánh Gemini với OpenAI
- Tạo demo mode khi quota hết

Gemini Benefits:
✅ Hoàn toàn miễn phí
✅ 100 requests/phút
✅ Không cần thẻ tín dụng
✅ Multi-modal (text, image, audio)
"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

# Cờ demo mode
DEMO_MODE = os.getenv("LAB15_DEMO_MODE", "0") == "1"
QUOTA_MARKER = Path(".lab15_quota_exhausted")

# ===== DEMO FALLBACK OUTPUTS =====
DEMO_DECORATOR_CACHE = """from functools import wraps
from typing import Callable, Any, Dict

def cache_decorator(func: Callable) -> Callable:
    '''Caches function results to avoid redundant computations.'''
    cache: Dict = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Create hashable key from args and kwargs
        key = (args, tuple(sorted(kwargs.items())))
        
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        
        return cache[key]
    
    return wrapper
"""

DEMO_DECORATOR_RETRY = """from functools import wraps
from typing import Callable, Any
import time

def retry_decorator(max_attempts: int = 3, delay: float = 1.0) -> Callable:
    '''Retries function call on failure with exponential backoff.'''
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))
            
        return wrapper
    return decorator
"""


def get_demo_fallback(decorator_type: str) -> str:
    """Trả về decorator demo khi không gọi API"""
    if decorator_type == "cache":
        return DEMO_DECORATOR_CACHE
    elif decorator_type == "retry":
        return DEMO_DECORATOR_RETRY
    return "# Demo decorator (không gọi API)"


try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    print("⚠️  google-generativeai chưa cài. Chạy: pip install google-generativeai")
    genai = None
    GEMINI_AVAILABLE = False


# ===== GEMINI INTEGRATION =====
def setup_gemini(api_key: Optional[str] = None) -> Optional[object]:
    """
    Thiết lập Gemini client
    
    Args:
        api_key: API key (nếu không, đọc từ .env)
    
    Returns:
        Gemini model hoặc None nếu không khả dụng
    """
    if not GEMINI_AVAILABLE:
        return None
    
    load_dotenv()
    key = api_key or os.getenv("GEMINI_API_KEY")
    
    if not key:
        print("⚠️  GEMINI_API_KEY không tìm thấy")
        return None
    
    genai.configure(api_key=key)
    return genai.GenerativeModel("gemini-pro")


def generate_decorator_with_gemini(
    decorator_name: str,
    description: str,
    model: Optional[object] = None
) -> str:
    """
    Dùng Gemini sinh decorator code
    
    Args:
        decorator_name: Tên decorator
        description: Mô tả chức năng
        model: Gemini model (nếu None, sử dụng demo)
    
    Returns:
        Mã Python của decorator
    """
    if DEMO_MODE or QUOTA_MARKER.exists():
        print(f"🎬 DEMO MODE: Trả về {decorator_name} mẫu")
        return get_demo_fallback(decorator_name.lower())
    
    if not model:
        print("❌ Gemini model không khả dụng. Sử dụng demo mode.")
        return get_demo_fallback(decorator_name.lower())
    
    prompt = f"""Create a Python decorator named '{decorator_name}' that {description}

Requirements:
1. Use functools.wraps
2. Add type hints
3. Include comprehensive docstring
4. Handle edge cases
5. Return complete, working code

Provide ONLY Python code, no markdown syntax, no explanations."""

    try:
        print(f"⏳ Gọi Gemini API để sinh {decorator_name}...")
        response = model.generate_content(prompt)
        code = response.text
        
        # Ghi log
        with open("lab154_gemini_log.txt", "a", encoding='utf-8') as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Generated {decorator_name}\n")
        
        return code
    
    except Exception as e:
        if "quota" in str(e).lower() or "429" in str(e):
            QUOTA_MARKER.write_text("exhausted\n")
            print(f"⚠️  Quota hết. Chuyển sang demo mode.")
        else:
            print(f"❌ Lỗi: {e}")
        
        return get_demo_fallback(decorator_name.lower())


# ===== MAIN DEMO =====
def run_lab():
    """Chạy Lab 15.4"""
    print("\n" + "=" * 70)
    print("🧪 LAB 15.4: GEMINI DECORATOR GENERATOR")
    print("=" * 70)
    
    # Setup Gemini
    model = setup_gemini()
    
    # Sinh decorators
    decorators_to_generate = [
        ("cache_decorator", "caches function results to avoid redundant computations"),
        ("retry_decorator", "retries function execution on failure up to 3 times"),
        ("rate_limit_decorator", "limits function call frequency to max 10 per second"),
    ]
    
    print(f"\n⚙️ Mode: {'DEMO' if DEMO_MODE else 'API'}")
    print(f"📊 Gemini API Available: {GEMINI_AVAILABLE}")
    
    results = {}
    for decorator_name, description in decorators_to_generate:
        print(f"\n{'='*70}")
        print(f"📝 Sinh: {decorator_name}")
        print(f"   Mô tả: {description}")
        print(f"{'='*70}")
        
        code = generate_decorator_with_gemini(decorator_name, description, model)
        results[decorator_name] = code
        
        # Hiển thị trước 300 ký tự
        preview = code[:300].replace("\n", "\n   ")
        print(f"\n📄 Kết quả (preview):\n   {preview}...")
        
        # Lưu vào file
        output_file = f"lab154_{decorator_name}.py"
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(code)
        print(f"\n💾 Lưu vào: {output_file}")
    
    print(f"\n{'='*70}")
    print("✅ Tất cả decorators đã sinh xong!")
    print(f"{'='*70}")
    
    # Tóm tắt
    print("\n📊 THỐNG KỀ:")
    print(f"   - Decorators sinh: {len(results)}")
    print(f"   - Mode: {'DEMO' if DEMO_MODE else 'API'}")
    print(f"   - Files tạo: {len([f for f in Path('.').glob('lab154_*.py')])}")
    
    print("\n💡 Gợi ý:")
    print("   1. Kiểm tra các file lab154_*.py")
    print("   2. Thử import và dùng các decorator")
    print("   3. Chạy lại với LAB15_DEMO_MODE=0 để dùng Gemini")
    
    print("\n" + "=" * 70)
    print("🎉 LAB 15.4 HOÀN THÀNH! 🎉")
    print("=" * 70)


if __name__ == "__main__":
    run_lab()
