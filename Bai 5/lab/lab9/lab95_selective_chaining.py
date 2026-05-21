"""
Lab 9.5: Selective Chaining Strategy (Chaining tối ưu)

Mục tiêu:
- Cải thiện Naive Chaining bằng cách chọn lọc prompts
- Gộp một số prompts liên quan thay vì gửi từng cái riêng
- Giảm chi phí tokens, tăng tốc độ, vẫn đạt chất lượng cao

Sự khác biệt Naive vs Selective:
- Naive: Gửi 3 prompts riêng → 3 API calls → 300+ tokens
- Selective: Gộp 2 prompts → 2 API calls → 200+ tokens (tiết kiệm ~30%)
"""

import os
import time
from openai import OpenAI
from openai.types.chat import ChatCompletion


# ===== MÃ NGUỒN CẦN HOÀN THIỆN =====
SOURCE_CODE = """
def get_average_return(net_returns: Dict[str, float]) -> float:
    gross_returns: np.ndarray = get_gross_returns(net_returns)
    gross_average: float = get_geometric_mean(gross_returns)
    net_average: float = get_net_average(gross_average)
    return net_average
"""

# ===== CẤU HÌNH PROMPT =====
SURROUND = """You are provided with a Python function enclosed with {{{ FUNCTION }}} 
that calls functions that should be completed."""
SINGLE_TASK = "Your task is to implement the missing functions."


def get_user_prompt(src: str) -> str:
    """Tạo user prompt từ mã nguồn"""
    return f"""
    FUNCTION: {{{{{{ {src} }}}}}}
    
    CODE:
    """


def run_selective_chaining():
    """Chạy Selective Chaining Strategy"""
    
    # Khởi tạo OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("❌ Thiếu OPENAI_API_KEY trong biến môi trường!")
    
    client: OpenAI = OpenAI(api_key=api_key)
    
    print("=" * 80)
    print("🔗 SELECTIVE CHAINING STRATEGY - CHAINING TỐI ƯU")
    print("=" * 80)
    
    # Khởi tạo lịch sử hội thoại
    messages = [
        {"role": "system", "content": f"{SURROUND} {SINGLE_TASK}"}
    ]
    
    print("\n💬 Chiến lược Selective:")
    print(f"   STEP 1: Hoàn thiện + Thêm type hints (gộp lại)")
    print(f"   STEP 2: Thêm docstring Google style")
    print(f"   → Giảm từ 3 steps xuống 2 steps")
    
    # Chuỗi các prompt được chọn lọc
    prompts = [
        # Step 1: Gộp hoàn thiện + type hints
        get_user_prompt(SOURCE_CODE) + 
        "\nAlso add type hints to all variables.",
        
        # Step 2: Docstring
        "Include Google Style docstring with Args and Returns sections.",
    ]
    
    all_outputs = []
    total_tokens = 0
    start_time = time.time()
    
    # Gửi từng prompt lần lượt (nhưng chỉ 2 thay vì 3)
    for i, prompt in enumerate(prompts, 1):
        print(f"\n{'=' * 80}")
        print(f"📝 STEP {i}: {['Implement + Type hints', 'Google docstring'][i-1]}")
        print(f"{'=' * 80}")
        
        # Thêm user message
        messages.append({"role": "user", "content": prompt})
        print(f"   ✅ User prompt được thêm vào (Step {i})")
        
        # Gửi request
        print(f"   ⏳ Gửi request tới OpenAI API...")
        
        completion: ChatCompletion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        
        output = completion.choices[0].message.content
        tokens_step = completion.usage.total_tokens
        total_tokens += tokens_step
        all_outputs.append(output)
        
        # Thêm assistant message vào lịch sử
        messages.append({"role": "assistant", "content": output})
        
        # In thông tin step này
        print(f"\n   📊 Tokens Step {i}: {tokens_step}")
        print(f"   📄 Output preview (200 ký tự đầu):")
        print(f"   {output[:200]}...")
    
    elapsed_time = time.time() - start_time
    
    # In kết quả cuối cùng
    print(f"\n{'=' * 80}")
    print("✅ SELECTIVE CHAINING STRATEGY - KẾT QUẢ CUỐI CÙNG")
    print(f"{'=' * 80}")
    
    print(f"\n📊 Thông tin tổng hợp:")
    print(f"   - Số prompts: {len(prompts)}")
    print(f"   - Tổng tokens: {total_tokens}")
    print(f"   - Thời gian: {elapsed_time:.2f} giây")
    
    print(f"\n📝 Kết quả cuối cùng (sau Step 2):")
    print("-" * 80)
    print(all_outputs[-1])
    print("-" * 80)
    
    # Lưu kết quả vào file
    with open("lab95_selective_chaining_result.txt", "w", encoding="utf-8") as f:
        f.write("=== SELECTIVE CHAINING STRATEGY RESULT ===\n\n")
        f.write("Chiến lược: Gộp prompts liên quan để giảm API calls\n\n")
        f.write(f"Source Code:\n{SOURCE_CODE}\n\n")
        for idx, output in enumerate(all_outputs, 1):
            f.write(f"--- STEP {idx} ---\n{output}\n\n")
        f.write(f"Statistics:\n")
        f.write(f"- Total tokens: {total_tokens}\n")
        f.write(f"- Time: {elapsed_time:.2f}s\n")
        f.write(f"- Messages count: {len(messages)}\n")
        f.write(f"- API calls: {len(prompts)}\n")
    
    print(f"\n💾 Kết quả đã lưu vào: lab95_selective_chaining_result.txt")
    print(f"💾 Lịch sử hội thoại có {len(messages)} messages")
    print("=" * 80)
    
    return all_outputs, total_tokens, elapsed_time, messages, len(prompts)


# ===== SO SÁNH NAIVE vs SELECTIVE =====
def comparison_with_naive(naive_tokens: int = None):
    """So sánh Selective Chaining với Naive Chaining"""
    print("\n" + "=" * 80)
    print("📊 SO SÁNH: NAIVE vs SELECTIVE CHAINING")
    print("=" * 80)
    
    print(f"""
┌─────────────────────┬──────────────┬──────────────┬─────────────┐
│ Tiêu chí            │ Naive (9.4)  │ Selective(9.5)│ Tiết kiệm   │
├─────────────────────┼──────────────┼──────────────┼─────────────┤
│ API calls           │ 3            │ 2            │ -33%        │
│ Tokens (dự kiến)    │ 300-350      │ 200-250      │ -30%        │
│ Thời gian (dự kiến) │ 1.5s - 2.5s  │ 1.0s - 1.5s  │ -40%        │
│ Chất lượng kết quả  │ Rất tốt ✅   │ Rất tốt ✅   │ Tương đương │
│ Khả năng kiểm soát  │ Cao          │ Trung bình   │ Reduced     │
└─────────────────────┴──────────────┴──────────────┴─────────────┘

💡 Kết luận:
   - Selective Chaining tiết kiệm ~30% chi phí tokens
   - Giảm thời gian xử lý do API calls ít hơn
   - Chất lượng kết quả không giảm sút
   - Thích hợp cho production khi cần tối ưu hóa chi phí

⚠️ Khi nào KHÔNG dùng Selective:
   - Khi cần kiểm soát chi tiết từng bước
   - Khi mỗi prompt cần độc lập để có thể điều chỉnh riêng
   - Khi output từ step trước cần review trước khi tiếp tục
""")
    print("=" * 80)


# ===== PHÂN TÍCH KẾT QUẢ =====
def analyze_selective_result(outputs: list, tokens: int, elapsed: float, api_calls: int) -> None:
    """Phân tích kết quả từ Selective Chaining"""
    print("\n" + "=" * 80)
    print("🔍 PHÂN TÍCH KẾT QUẢ SELECTIVE CHAINING")
    print("=" * 80)
    
    final_output = outputs[-1]
    checks = {
        "Chứa implementations": ("def" in final_output),
        "Có type hints": ("->" in final_output),
        "Có docstring": ('"""' in final_output or "'''" in final_output),
        "Chứa Google style": ("Args:" in final_output or "Returns:" in final_output),
    }
    
    print(f"\n✅ Kiểm tra kết quả cuối cùng:")
    for criterion, passed in checks.items():
        status = "✅" if passed else "⚠️"
        print(f"   {status} {criterion}: {'Có' if passed else 'Không'}")
    
    print(f"\n📈 Thống kê hiệu suất:")
    print(f"   - API calls: {api_calls} (so với Naive: 3)")
    print(f"   - Tokens: {tokens} (dự kiến Naive: 300-350)")
    print(f"   - Thời gian: {elapsed:.2f}s")
    print(f"   - Tokens tiết kiệm: {max(0, 325 - tokens):.0f} ({max(0, (325-tokens)/325*100):.0f}%)")
    
    print(f"\n💡 Lợi ích của Selective:")
    print(f"   ✅ Giảm chi phí tokens")
    print(f"   ✅ Tăng tốc độ (ít API calls)")
    print(f"   ✅ Vẫn đạt chất lượng cao")
    print(f"   ✅ Dễ quản lý hơn Naive (2 steps thay vì 3)")
    print("=" * 80)


if __name__ == "__main__":
    try:
        outputs, tokens, elapsed, messages, api_calls = run_selective_chaining()
        analyze_selective_result(outputs, tokens, elapsed, api_calls)
        comparison_with_naive()
        
        print("\n" + "🎉 " * 20)
        print("✨ Lab 9.5 hoàn thành thành công! ✨")
        print("🎉 " * 20)
        print("\n📌 Tiếp theo: Hãy làm Lab 9.6 để so sánh tất cả 3 chiến lược!")
        
    except ValueError as e:
        print(f"❌ Lỗi: {e}")
    except Exception as e:
        print(f"❌ Lỗi API: {e}")
