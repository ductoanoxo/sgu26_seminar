"""
Lab 9.4: Naive Chaining Strategy

Mục tiêu:
- Sử dụng một chuỗi các prompt để tinh chỉnh kết quả từng bước
- Lưu lịch sử hội thoại (conversational history)
- So sánh với Baseline và CoT

Chaining Strategy:
- Gửi Prompt 1 (hoàn thiện hàm)
- Gửi Prompt 2 (thêm type hints)
- Gửi Prompt 3 (thêm docstring)
- Mô hình sử dụng kết quả trước đó làm ngữ cảnh

Naive = Không chọn lọc, gửi tất cả prompts liên tiếp
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


def run_naive_chaining():
    """Chạy Naive Chaining Strategy"""
    
    # Khởi tạo OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("❌ Thiếu OPENAI_API_KEY trong biến môi trường!")
    
    client: OpenAI = OpenAI(api_key=api_key)
    
    print("=" * 80)
    print("🔗 NAIVE CHAINING STRATEGY - LỊCH SỬ HỘI THOẠI")
    print("=" * 80)
    
    # Khởi tạo lịch sử hội thoại
    messages = [
        {"role": "system", "content": f"{SURROUND} {SINGLE_TASK}"}
    ]
    
    print("\n💬 Khởi tạo conversational history:")
    print(f"   - System message được thêm vào")
    
    # Chuỗi các prompt
    prompts = [
        get_user_prompt(SOURCE_CODE),  # Prompt 1: Hoàn thiện hàm
        "Add type hints to all variables.",  # Prompt 2: Thêm type hints
        "Include Google Style docstring.",  # Prompt 3: Thêm docstring
    ]
    
    all_outputs = []
    total_tokens = 0
    start_time = time.time()
    
    # Gửi từng prompt lần lượt
    for i, prompt in enumerate(prompts, 1):
        print(f"\n{'=' * 80}")
        print(f"📝 STEP {i}: {['Hoàn thiện hàm', 'Thêm type hints', 'Thêm docstring'][i-1]}")
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
    print("✅ CHAINING STRATEGY - KẾT QUẢ CUỐI CÙNG")
    print(f"{'=' * 80}")
    
    print(f"\n📊 Thông tin tổng hợp:")
    print(f"   - Số prompts: {len(prompts)}")
    print(f"   - Tổng tokens: {total_tokens}")
    print(f"   - Thời gian: {elapsed_time:.2f} giây")
    print(f"   - Tokens bình quân/step: {total_tokens // len(prompts)}")
    
    print(f"\n📝 Kết quả cuối cùng (sau Step 3):")
    print("-" * 80)
    print(all_outputs[-1])
    print("-" * 80)
    
    # Lưu kết quả vào file
    with open("lab94_naive_chaining_result.txt", "w", encoding="utf-8") as f:
        f.write("=== NAIVE CHAINING STRATEGY RESULT ===\n\n")
        f.write(f"Source Code:\n{SOURCE_CODE}\n\n")
        for idx, output in enumerate(all_outputs, 1):
            f.write(f"--- STEP {idx} ---\n{output}\n\n")
        f.write(f"Statistics:\n")
        f.write(f"- Total tokens: {total_tokens}\n")
        f.write(f"- Time: {elapsed_time:.2f}s\n")
        f.write(f"- Messages count: {len(messages)}\n")
    
    print(f"\n💾 Kết quả đã lưu vào: lab94_naive_chaining_result.txt")
    print(f"💾 Lịch sử hội thoại có {len(messages)} messages")
    print("=" * 80)
    
    return all_outputs, total_tokens, elapsed_time, messages


# ===== PHÂN TÍCH KẾT QUẢ =====
def analyze_chaining_result(outputs: list, tokens: int, elapsed: float, messages: list) -> None:
    """Phân tích kết quả từ Chaining"""
    print("\n" + "=" * 80)
    print("🔍 PHÂN TÍCH KẾT QUẢ CHAINING")
    print("=" * 80)
    
    print(f"\n📊 Cấu trúc conversational history:")
    print(f"   - System messages: 1")
    print(f"   - User messages: {len([m for m in messages if m['role'] == 'user'])}")
    print(f"   - Assistant messages: {len([m for m in messages if m['role'] == 'assistant'])}")
    print(f"   - Tổng messages: {len(messages)}")
    
    final_output = outputs[-1]
    checks = {
        "Chứa implementations": ("def" in final_output),
        "Có type hints": ("->" in final_output and "float" in final_output),
        "Có docstring": ('"""' in final_output or "'''" in final_output),
        "Chứa Google style": ("Args:" in final_output or "Returns:" in final_output),
    }
    
    print(f"\n✅ Kiểm tra kết quả cuối cùng:")
    for criterion, passed in checks.items():
        status = "✅" if passed else "⚠️"
        print(f"   {status} {criterion}: {'Có' if passed else 'Không'}")
    
    print(f"\n📈 So sánh các phương pháp:")
    print(f"   - Baseline (Lab 9.1): ~150-200 tokens, 1 prompt")
    print(f"   - CoT (Lab 9.3): ~300-400 tokens, 1 prompt")
    print(f"   - Chaining (Lab 9.4): ~{tokens} tokens, {len([m for m in messages if m['role'] == 'user'])} prompts")
    
    print(f"\n💡 Nhận xét về Naive Chaining:")
    print(f"   - ✅ Tinh chỉnh kết quả theo từng bước cụ thể")
    print(f"   - ✅ Có thể kiểm soát chính xác quá trình")
    print(f"   - ⚠️ Tokens tăng lên do phải gửi lịch sử hội thoại")
    print(f"   - ⚠️ Thường thặc thêm tokens không cần thiết (gọi là 'naive')")
    print("=" * 80)


# ===== GỢI Ý CẢI THIỆN =====
def explain_selective_chaining():
    """Giải thích về Selective Chaining (sẽ làm ở Lab 9.5)"""
    print("\n" + "=" * 80)
    print("💡 GIỚI THIỆU SELECTIVE CHAINING (Lab 9.5)")
    print("=" * 80)
    print("""
Naive Chaining gửi 3 prompts riêng biệt → 3 round-trip API → chập hơn, đắt hơn

Selective Chaining là cải tiến:
- Hợp nhất prompts liên quan 
- VD: Thay vì Step 1, 2, 3 → Gộp thành "Implement + Add type hints" (Step 1)
- Kết quả: Tokens giảm, tốc độ tăng, chất lượng vẫn tốt

Ví dụ:
- Naive: 3 API calls × 150s = 450s
- Selective: 2 API calls × 150s = 300s (gọn gàng hơn)

Hãy xem Lab 9.5 để biết cách cải tiến!
""")
    print("=" * 80)


if __name__ == "__main__":
    try:
        outputs, tokens, elapsed, messages = run_naive_chaining()
        analyze_chaining_result(outputs, tokens, elapsed, messages)
        explain_selective_chaining()
        
        print("\n" + "🎉 " * 20)
        print("✨ Lab 9.4 hoàn thành thành công! ✨")
        print("🎉 " * 20)
        
    except ValueError as e:
        print(f"❌ Lỗi: {e}")
    except Exception as e:
        print(f"❌ Lỗi API: {e}")
