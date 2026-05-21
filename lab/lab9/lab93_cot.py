"""
Lab 9.3: Chain of Thought (CoT) Strategy

Mục tiêu:
- Sử dụng CoT để hoàn thiện toàn bộ hàm get_average_return() 
- Yêu cầu mô hình suy nghĩ từng bước trước khi đưa ra kết quả
- So sánh với Baseline (Lab 9.1) về độ chính xác

Chain of Thought Strategy:
- Thêm từ khóa "think step by step"
- Mô hình sẽ giải thích từng bước tư duy trước khi code
- Tốn nhiều tokens hơn nhưng độ chính xác cao hơn
"""

import os
import time
from openai import OpenAI
from openai.types.chat import ChatCompletion


# ===== MÃ NGUỒN CẦN HOÀN THIỆN =====
SOURCE_CODE = """
from typing import Dict
import numpy as np

def get_average_return(
        net_returns: Dict[str, float],
) -> float:
    \"\"\"Tính lợi suất trung bình theo công thức hình học.\"\"\"
    gross_returns: np.ndarray = get_gross_returns(net_returns)
    gross_average: float = get_geometric_mean(gross_returns)
    net_average: float = get_net_average(gross_average)
    return net_average
"""

# ===== CẤU HÌNH PROMPT CoT =====
SURROUND = """You are provided with a Python function enclosed with {{{ FUNCTION }}} 
that calls functions that should be completed."""

SINGLE_TASK = """Your task is to implement the missing functions.
Think step by step:
1. Analyze the input parameter and understand what it represents
2. Identify what each function should do based on its name and parameters
3. Determine the mathematical operations needed for each function
4. Write clean, well-documented code with type hints
5. Ensure all functions work together correctly"""


def get_user_prompt(src: str) -> str:
    """Tạo user prompt từ mã nguồn"""
    return f"""
    FUNCTION: {{{{{{ {src} }}}}}}
    
    Please think step by step and implement all missing functions:
    - get_gross_returns()
    - get_geometric_mean()
    - get_net_average()
    
    Ensure the functions work correctly with the main function get_average_return().
    
    IMPLEMENTATION:
    """


def run_cot_strategy():
    """Chạy Chain of Thought Strategy"""
    
    # Khởi tạo OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("❌ Thiếu OPENAI_API_KEY trong biến môi trường!")
    
    client: OpenAI = OpenAI(api_key=api_key)
    
    # Giải thích cấu trúc prompt
    print("=" * 80)
    print("🧠 CHAIN OF THOUGHT STRATEGY - CẤU TRÚC PROMPT")
    print("=" * 80)
    print(f"\n📋 SURROUND:\n{SURROUND}")
    print(f"\n📋 SINGLE_TASK:\n{SINGLE_TASK}")
    print(f"\n📋 SOURCE CODE:\n{SOURCE_CODE}")
    print("\n" + "=" * 80)
    print("💡 Nhận xét: Prompt CoT yêu cầu 5 bước tư duy rõ ràng")
    print("=" * 80)
    
    # Tạo prompts
    system_prompt = f"{SURROUND} {SINGLE_TASK}"
    user_prompt = get_user_prompt(SOURCE_CODE)
    
    # Gửi request tới OpenAI API
    print("\n⏳ Gửi request tới OpenAI API (gpt-4o-mini) với CoT...")
    start_time = time.time()
    
    completion: ChatCompletion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    
    elapsed_time = time.time() - start_time
    
    # Trích xuất kết quả
    output = completion.choices[0].message.content
    tokens_input = completion.usage.prompt_tokens
    tokens_output = completion.usage.completion_tokens
    tokens_total = completion.usage.total_tokens
    
    # In kết quả
    print("\n" + "=" * 80)
    print("✅ CHAIN OF THOUGHT STRATEGY - KẾT QUẢ")
    print("=" * 80)
    
    print(f"\n📊 Thông tin API:")
    print(f"   - Model: {completion.model}")
    print(f"   - Input tokens: {tokens_input}")
    print(f"   - Output tokens: {tokens_output}")
    print(f"   - Total tokens: {tokens_total}")
    print(f"   - Thời gian: {elapsed_time:.2f} giây")
    
    print(f"\n📝 Kết quả (suy nghĩ từng bước):")
    print("-" * 80)
    print(output)
    print("-" * 80)
    
    # Lưu kết quả vào file
    with open("lab93_cot_result.txt", "w", encoding="utf-8") as f:
        f.write("=== CHAIN OF THOUGHT STRATEGY RESULT ===\n\n")
        f.write(f"Source Code:\n{SOURCE_CODE}\n\n")
        f.write(f"System Prompt:\n{system_prompt}\n\n")
        f.write(f"User Prompt:\n{user_prompt}\n\n")
        f.write(f"Result:\n{output}\n\n")
        f.write(f"Statistics:\n")
        f.write(f"- Input tokens: {tokens_input}\n")
        f.write(f"- Output tokens: {tokens_output}\n")
        f.write(f"- Total tokens: {tokens_total}\n")
        f.write(f"- Time: {elapsed_time:.2f}s\n")
    
    print(f"\n💾 Kết quả đã lưu vào: lab93_cot_result.txt")
    print("=" * 80)
    
    return output, tokens_total, elapsed_time


# ===== PHÂN TÍCH KẾT QUẢ =====
def analyze_cot_result(result: str, tokens: int, elapsed: float) -> None:
    """Phân tích kết quả từ CoT"""
    print("\n" + "=" * 80)
    print("🔍 PHÂN TÍCH KẾT QUẢ CoT")
    print("=" * 80)
    
    analysis = {
        "Chứa suy nghĩ từng bước": ("Step 1" in result or "Thinking" in result or "analysis" in result.lower()),
        "Chứa mã Python": ("def" in result or "return" in result),
        "Sử dụng numpy": ("np." in result or "numpy" in result),
        "Có docstring": ('"""' in result or "'''" in result),
        "Có type hints": ("->" in result and "float" in result),
    }
    
    print("\n✅ Kiểm tra kết quả:")
    for criterion, passed in analysis.items():
        status = "✅" if passed else "⚠️"
        print(f"   {status} {criterion}: {'Có' if passed else 'Không'}")
    
    print(f"\n📊 So sánh với Baseline (Lab 9.1):")
    print(f"   - Tokens Base: ~150-200 ➜ Tokens CoT: {tokens}")
    print(f"   - Tokens tăng: {tokens - 175:.0f} (+{(tokens/175 - 1)*100:.0f}%)")
    print(f"   - Thời gian: {elapsed:.2f}s")
    print(f"\n💡 Nhận xét:")
    print(f"   - CoT sử dụng nhiều tokens hơn do phải giải thích suy nghĩ")
    print(f"   - Chi phí API tăng lên nhưng độ chính xác thường cao hơn")
    print(f"   - Thích hợp cho bài toán phức tạp hoặc yêu cầu cao")
    print("=" * 80)


# ===== SO SÁNH BASELINE vs CoT =====
def comparison_guidance():
    """Hướng dẫn so sánh Baseline vs CoT"""
    print("\n" + "=" * 80)
    print("📋 HƯỚNG DẪN SO SÁNH BASELINE vs CoT")
    print("=" * 80)
    print("""
Sau khi hoàn thành Lab 9.1 (Baseline) và Lab 9.3 (CoT), hãy so sánh:

1️⃣ CHẤT LƯỢNG KÓ:
   - Kết quả Baseline có lỗi logic không?
   - Kết quả CoT có hoàn thiện hơn không?
   - Cả hai có tạo hàm khác nhau không?

2️⃣ TOKENS & CHI PHÍ:
   - Baseline sử dụng bao nhiêu tokens?
   - CoT sử dụng bao nhiêu tokens?
   - Chi phí = (tokens_input × 0.00015 + tokens_output × 0.0006) USD
   
3️⃣ THỜI GIAN:
   - Baseline: thời gian = ?s
   - CoT: thời gian = ?s
   - Khác biệt: ?%

4️⃣ KHI NÀO DÙNG CÁI GÌ:
   - ✅ Baseline: Bài toán đơn giản, cần nhanh, bội ngoài
   - ✅ CoT: Bài toán phức tạp, cần chính xác cao, chi phí không quan trọng

Hãy điền các con số vào bảng so sánh trong lab96_comparison.py
""")
    print("=" * 80)


if __name__ == "__main__":
    try:
        result, tokens, elapsed = run_cot_strategy()
        analyze_cot_result(result, tokens, elapsed)
        comparison_guidance()
        
        print("\n" + "🎉 " * 20)
        print("✨ Lab 9.3 hoàn thành thành công! ✨")
        print("🎉 " * 20)
        
    except ValueError as e:
        print(f"❌ Lỗi: {e}")
    except Exception as e:
        print(f"❌ Lỗi API: {e}")
