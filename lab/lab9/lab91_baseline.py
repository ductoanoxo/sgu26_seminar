"""
Lab 9.1: Baseline Strategy với OpenAI API

Mục tiêu:
- Sử dụng Baseline Strategy để hoàn thiện hàm get_geometric_mean()
- Gửi một prompt đơn lẻ, trực tiếp đến OpenAI API
- Trích xuất và kiểm tra kết quả

Baseline Strategy:
- Gửi đúng 1 prompt
- Không có tinh chỉnh hay bước thêm
- Nhanh nhất nhưng ít hiệu quả nhất
"""

from typing import Dict
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion


# ===== CẤU HÌNH PROMPT =====
SURROUND = "You are provided with a Python function signature enclosed with {{{ FUNCTION }}}."
SINGLE_TASK = "Your task is to implement the function."

SRC_CODE = """def get_geometric_mean(
    net_returns: Dict[str, float],
) -> float:"""

QUOTA_MARKER_FILE = Path(".lab91_quota_exhausted")


def get_demo_fallback_output() -> str:
    """Kết quả mẫu khi chạy demo fallback, không gọi OpenAI."""
    return """def get_geometric_mean(
    net_returns: Dict[str, float],
) -> float:
    product: float = 1.0
    for key in net_returns:
        product *= net_returns[key]
    geometric_mean: float = product ** (1 / len(net_returns))
    return geometric_mean
"""


def should_use_demo_fallback() -> tuple[bool, str]:
    """Quyết định có chạy fallback hay không."""
    force_demo = os.getenv("LAB9_DEMO_MODE", "0") == "1"
    if force_demo:
        return True, "LAB9_DEMO_MODE=1"

    if QUOTA_MARKER_FILE.exists():
        return True, "quota marker"

    return False, ""


def get_user_prompt(src: str) -> str:
    """Tạo user prompt từ mã nguồn"""
    return f""" 
    FUNCTION: {{{{{{ {src} }}}}}} 

    CODE: 
    """


def run_baseline_strategy():
    """Chạy Baseline Strategy"""
    load_dotenv()

    use_fallback, reason = should_use_demo_fallback()
    if use_fallback:
        output = get_demo_fallback_output()
        tokens_used = 0

        print("=" * 70)
        print("🎯 BASELINE STRATEGY - DEMO FALLBACK")
        print("=" * 70)
        print(f"\nℹ️ Lý do fallback: {reason}")
        print("ℹ️ Chế độ này không gọi OpenAI API.")
        print(f"\n📝 Kết quả demo:")
        print(output)

        with open("lab91_baseline_result.txt", "w", encoding="utf-8") as f:
            f.write("=== BASELINE STRATEGY DEMO FALLBACK ===\n\n")
            f.write(f"Source Code:\n{SRC_CODE}\n\n")
            f.write(f"Reason: {reason}\n")
            f.write("No OpenAI API call was made.\n\n")
            f.write(f"Result:\n{output}\n\n")
            f.write(f"Tokens Used: {tokens_used}\n")

        print(f"\n💾 Kết quả đã lưu vào: lab91_baseline_result.txt")
        print("=" * 70)
        return output, tokens_used
    
    # Khởi tạo OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("❌ Thiếu OPENAI_API_KEY trong biến môi trường!")
    
    client: OpenAI = OpenAI(api_key=api_key)
    
    # Giải thích cấu trúc prompt
    print("=" * 70)
    print("🎯 BASELINE STRATEGY - CẤU TRÚC PROMPT")
    print("=" * 70)
    print(f"\n📋 SURROUND: {SURROUND}")
    print(f"\n📋 SINGLE_TASK: {SINGLE_TASK}")
    print(f"\n📋 SOURCE CODE:\n{SRC_CODE}")
    print("\n" + "=" * 70)
    
    # Tạo prompts
    system_prompt = f"{SURROUND} {SINGLE_TASK}"
    user_prompt = get_user_prompt(SRC_CODE)
    
    # Gửi request tới OpenAI API
    print("\n⏳ Gửi request tới OpenAI API (gpt-4o-mini)...")
    
    try:
        completion: ChatCompletion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
    except Exception as exc:
        error_message = str(exc)
        if "insufficient_quota" in error_message or "Error code: 429" in error_message:
            QUOTA_MARKER_FILE.write_text("insufficient_quota\n", encoding="utf-8")

            output = get_demo_fallback_output()
            tokens_used = 0

            print("\n⚠️ OpenAI API đã hết quota, chuyển sang DEMO FALLBACK.")
            print("ℹ️ Các lần chạy sau sẽ tự động không gọi OpenAI cho đến khi xóa file marker.")

            with open("lab91_baseline_result.txt", "w", encoding="utf-8") as f:
                f.write("=== BASELINE STRATEGY DEMO FALLBACK (QUOTA) ===\n\n")
                f.write(f"Source Code:\n{SRC_CODE}\n\n")
                f.write("Reason: insufficient_quota\n")
                f.write("No OpenAI API call was made in fallback output generation.\n\n")
                f.write(f"Result:\n{output}\n\n")
                f.write(f"Tokens Used: {tokens_used}\n")

            print(f"\n📝 Kết quả demo:")
            print(output)
            print(f"\n💾 Kết quả đã lưu vào: lab91_baseline_result.txt")
            print("=" * 70)
            return output, tokens_used

        raise
    
    # Trích xuất kết quả
    output = completion.choices[0].message.content
    tokens_used = completion.usage.total_tokens

    if QUOTA_MARKER_FILE.exists():
        QUOTA_MARKER_FILE.unlink()
    
    # In kết quả
    print("\n" + "=" * 70)
    print("✅ BASELINE STRATEGY - KẾT QUẢ")
    print("=" * 70)
    print(f"\n📊 Thông tin API:")
    print(f"   - Model: {completion.model}")
    print(f"   - Input tokens: {completion.usage.prompt_tokens}")
    print(f"   - Output tokens: {completion.usage.completion_tokens}")
    print(f"   - Total tokens: {tokens_used}")
    
    print(f"\n📝 Kết quả:")
    print(output)
    
    # Lưu kết quả vào file
    with open("lab91_baseline_result.txt", "w", encoding="utf-8") as f:
        f.write("=== BASELINE STRATEGY RESULT ===\n\n")
        f.write(f"Source Code:\n{SRC_CODE}\n\n")
        f.write(f"Result:\n{output}\n\n")
        f.write(f"Tokens Used: {tokens_used}\n")
    
    print(f"\n💾 Kết quả đã lưu vào: lab91_baseline_result.txt")
    print("=" * 70)
    
    return output, tokens_used


# ===== PHÂN TÍCH KẾT QUẢ =====
def analyze_result(result: str) -> None:
    """Phân tích kết quả từ OpenAI"""
    print("\n" + "=" * 70)
    print("🔍 PHÂN TÍCH KẾT QUẢ")
    print("=" * 70)
    
    # Kiểm tra xem kết quả có chứa code không
    if "def" in result or "return" in result:
        print("✅ Kết quả chứa mã Python")
    else:
        print("⚠️  Kết quả có thể không chứa mã Python")
    
    # Kiểm tra xem có sử dụng numpy không
    if "np." in result or "numpy" in result:
        print("✅ Kết quả sử dụng numpy")
    else:
        print("⚠️  Kết quả không sử dụng numpy (có thể đơn giản hơn)")
    
    # Kiểm tra xem có sử dụng vòng lặp không
    if "for" in result or "while" in result:
        print("✅ Kết quả sử dụng vòng lặp")
    else:
        print("⚠️  Kết quả không sử dụng vòng lặp (có thể dùng hàm sẵn)")
    
    print("=" * 70)


if __name__ == "__main__":
    try:
        result, tokens = run_baseline_strategy()
        analyze_result(result)
        
        print("\n" + "🎉 " * 20)
        print("✨ Lab 9.1 hoàn thành thành công! ✨")
        print("🎉 " * 20)
        
    except ValueError as e:
        print(f"❌ Lỗi: {e}")
    except Exception as e:
        print(f"❌ Lỗi API: {e}")
