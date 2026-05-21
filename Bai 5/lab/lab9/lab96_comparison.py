"""
Lab 9.6: Tổng hợp So sánh Ba Chiến lược Prompting

Mục tiêu:
- Chạy cả ba chiến lược (Baseline, CoT, Chaining) trên cùng bài toán
- So sánh chi phí, thời gian, chất lượng kết quả
- Đưa ra kết luận khi nào dùng chiến lược nào

Yêu cầu trước tiên:
- Hoàn thành Lab 9.1 (Baseline)
- Hoàn thành Lab 9.3 (CoT)
- Hoàn thành Lab 9.5 (Selective Chaining)
"""

import os
import time
import json
from openai import OpenAI
from openai.types.chat import ChatCompletion


# ===== MÃ NGUỒN CẦN HOÀN THIỆN =====
SOURCE_CODE = """def get_geometric_mean(net_returns: Dict[str, float]) -> float:"""

SOURCE_CODE_COMPLEX = """
def get_average_return(net_returns: Dict[str, float]) -> float:
    gross_returns: np.ndarray = get_gross_returns(net_returns)
    gross_average: float = get_geometric_mean(gross_returns)
    net_average: float = get_net_average(gross_average)
    return net_average
"""


class PromptingStrategyComparison:
    """So sánh các chiến lược prompting"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ Thiếu OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.results = {}
    
    # ===== BASELINE STRATEGY =====
    def strategy_baseline(self, source_code: str, task: str = "implement") -> dict:
        """Baseline Strategy - một prompt đơn lẻ"""
        print("\n" + "=" * 80)
        print("🎯 BASELINE STRATEGY")
        print("=" * 80)
        
        start_time = time.time()
        
        system_prompt = "You are provided with a Python function signature. Your task is to implement it."
        user_prompt = f"""
        FUNCTION: {{{{ {source_code} }}}}
        CODE:
        """
        
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        
        elapsed = time.time() - start_time
        
        result = {
            "strategy": "Baseline",
            "tokens": completion.usage.total_tokens,
            "input_tokens": completion.usage.prompt_tokens,
            "output_tokens": completion.usage.completion_tokens,
            "time": elapsed,
            "api_calls": 1,
            "output": completion.choices[0].message.content,
        }
        
        print(f"✅ Tokens: {result['tokens']} | Time: {elapsed:.2f}s | API calls: 1")
        return result
    
    # ===== CHAIN OF THOUGHT STRATEGY =====
    def strategy_cot(self, source_code: str) -> dict:
        """Chain of Thought Strategy - yêu cầu suy nghĩ từng bước"""
        print("\n" + "=" * 80)
        print("🧠 CHAIN OF THOUGHT STRATEGY")
        print("=" * 80)
        
        start_time = time.time()
        
        system_prompt = """You are provided with a Python function.
        Your task is to implement it.
        Think step by step:
        1. Analyze what the function should do
        2. Determine the mathematical operations needed
        3. Write clean, well-documented code"""
        
        user_prompt = f"""
        FUNCTION: {{{{ {source_code} }}}}
        
        Please think step by step and implement the function.
        CODE:
        """
        
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        
        elapsed = time.time() - start_time
        
        result = {
            "strategy": "Chain of Thought",
            "tokens": completion.usage.total_tokens,
            "input_tokens": completion.usage.prompt_tokens,
            "output_tokens": completion.usage.completion_tokens,
            "time": elapsed,
            "api_calls": 1,
            "output": completion.choices[0].message.content,
        }
        
        print(f"✅ Tokens: {result['tokens']} | Time: {elapsed:.2f}s | API calls: 1")
        return result
    
    # ===== SELECTIVE CHAINING STRATEGY =====
    def strategy_selective_chaining(self, source_code: str) -> dict:
        """Selective Chaining - gộp prompts liên quan"""
        print("\n" + "=" * 80)
        print("🔗 SELECTIVE CHAINING STRATEGY")
        print("=" * 80)
        
        start_time = time.time()
        
        messages = [
            {"role": "system", "content": "Your task is to implement missing functions."}
        ]
        
        prompts = [
            f"FUNCTION: {{{{ {source_code} }}}} CODE:",
            "Add type hints and docstring.",
        ]
        
        total_tokens = 0
        final_output = ""
        
        for i, prompt in enumerate(prompts, 1):
            messages.append({"role": "user", "content": prompt})
            
            completion = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            
            output = completion.choices[0].message.content
            messages.append({"role": "assistant", "content": output})
            total_tokens += completion.usage.total_tokens
            final_output = output
        
        elapsed = time.time() - start_time
        
        result = {
            "strategy": "Selective Chaining",
            "tokens": total_tokens,
            "input_tokens": None,  # Không tính chính xác cho chaining
            "output_tokens": None,
            "time": elapsed,
            "api_calls": len(prompts),
            "output": final_output,
        }
        
        print(f"✅ Tokens: {result['tokens']} | Time: {elapsed:.2f}s | API calls: {len(prompts)}")
        return result
    
    # ===== SO SÁNH CÁC CHIẾN LƯỢC =====
    def run_all_strategies(self, source_code: str = SOURCE_CODE) -> dict:
        """Chạy cả ba chiến lược"""
        print("\n" + "=" * 80)
        print("🚀 CHẠY CẢ BA CHIẾN LƯỢC PROMPTING")
        print("=" * 80)
        
        strategies = {}
        
        # Chạy Baseline
        try:
            strategies["baseline"] = self.strategy_baseline(source_code)
        except Exception as e:
            print(f"❌ Baseline failed: {e}")
        
        # Chạy CoT
        try:
            strategies["cot"] = self.strategy_cot(source_code)
        except Exception as e:
            print(f"❌ CoT failed: {e}")
        
        # Chạy Selective Chaining
        try:
            strategies["chaining"] = self.strategy_selective_chaining(source_code)
        except Exception as e:
            print(f"❌ Chaining failed: {e}")
        
        self.results = strategies
        return strategies
    
    # ===== PHÂN TÍCH VÀ SO SÁNH =====
    def print_comparison_table(self):
        """In bảng so sánh"""
        if not self.results:
            print("❌ Chưa có dữ liệu để so sánh. Hãy chạy run_all_strategies() trước.")
            return
        
        print("\n" + "=" * 100)
        print("📊 BẢNG SO SÁNH BA CHIẾN LƯỢC")
        print("=" * 100)
        
        print(f"\n{'Tiêu chí':<25} {'Baseline':<25} {'CoT':<25} {'Chaining':<25}")
        print("-" * 100)
        
        # Tokens
        baseline_tokens = self.results.get("baseline", {}).get("tokens", 0)
        cot_tokens = self.results.get("cot", {}).get("tokens", 0)
        chaining_tokens = self.results.get("chaining", {}).get("tokens", 0)
        
        print(f"{'Tokens':<25} {baseline_tokens:<25} {cot_tokens:<25} {chaining_tokens:<25}")
        
        # Thời gian
        baseline_time = self.results.get("baseline", {}).get("time", 0)
        cot_time = self.results.get("cot", {}).get("time", 0)
        chaining_time = self.results.get("chaining", {}).get("time", 0)
        
        print(f"{'Thời gian (s)':<25} {baseline_time:<25.2f} {cot_time:<25.2f} {chaining_time:<25.2f}")
        
        # API calls
        baseline_calls = self.results.get("baseline", {}).get("api_calls", 1)
        cot_calls = self.results.get("cot", {}).get("api_calls", 1)
        chaining_calls = self.results.get("chaining", {}).get("api_calls", 0)
        
        print(f"{'API calls':<25} {baseline_calls:<25} {cot_calls:<25} {chaining_calls:<25}")
        
        # Chi phí (ước tính)
        # gpt-4o-mini: $0.15 per 1M input, $0.6 per 1M output
        baseline_cost = (baseline_tokens * 0.00015) / 1000
        cot_cost = (cot_tokens * 0.00015) / 1000
        chaining_cost = (chaining_tokens * 0.00015) / 1000
        
        print(f"\n{'Chi phí (USD)':<25} {baseline_cost:<25.6f} {cot_cost:<25.6f} {chaining_cost:<25.6f}")
        
        print("\n" + "=" * 100)
    
    def print_analysis(self):
        """In phân tích chi tiết"""
        if not self.results:
            return
        
        print("\n" + "=" * 100)
        print("🔍 PHÂN TÍCH CHI TIẾT")
        print("=" * 100)
        
        # Tìm chiến lược tốt nhất cho từng tiêu chí
        fastest = min(self.results.items(), key=lambda x: x[1].get("time", float('inf')))
        cheapest = min(self.results.items(), key=lambda x: x[1].get("tokens", float('inf')))
        
        print(f"\n🏆 Chiến lược nhanh nhất: {fastest[0].upper()} ({fastest[1]['time']:.2f}s)")
        print(f"💰 Chiến lược rẻ nhất: {cheapest[0].upper()} ({cheapest[1]['tokens']} tokens)")
        
        # Đánh giá tổng hợp
        print(f"\n📈 Khuyến cáo sử dụng:")
        print(f"   • BASELINE: Bài toán đơn giản, cần tốc độ, chi phí không quan trọng")
        print(f"   • CoT: Bài toán phức tạp, cần độ chính xác cao, có thể tốn chi phí")
        print(f"   • CHAINING: Cần tinh chỉnh từng bước, kiểm soát chi tiết")
        
        print("\n" + "=" * 100)
    
    def save_results(self, filename: str = "lab96_comparison_results.json"):
        """Lưu kết quả vào file JSON"""
        if not self.results:
            print("❌ Chưa có dữ liệu để lưu")
            return
        
        # Xóa 'output' để file không quá lớn, giữ lại số liệu thống kê
        data = {}
        for strategy, result in self.results.items():
            data[strategy] = {k: v for k, v in result.items() if k != "output"}
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Kết quả đã lưu vào: {filename}")
        print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    """Main function"""
    print("=" * 100)
    print("🎯 LAB 9.6: TỔNG HỢP VÀ SO SÁNH BA CHIẾN LƯỢC PROMPTING")
    print("=" * 100)
    
    try:
        # Khởi tạo comparator
        comparator = PromptingStrategyComparison()
        
        # Chạy tất cả chiến lược
        print("\n⏳ Đang chạy các chiến lược (có thể mất vài giây)...")
        comparator.run_all_strategies(SOURCE_CODE)
        
        # In bảng so sánh
        comparator.print_comparison_table()
        
        # In phân tích
        comparator.print_analysis()
        
        # Lưu kết quả
        comparator.save_results()
        
        print("\n" + "🎉 " * 25)
        print("✨ LAB 9.6 HOÀN THÀNH THÀNH CÔNG! ✨")
        print("🎉 " * 25)
        
        print(f"""
📚 TÓM TẮT BÀI HỌC:

1️⃣ BASELINE STRATEGY (Lab 9.1, 9.2)
   - Nhanh nhất, rẻ nhất
   - Thích hợp cho bài toán đơn giản, rõ ràng
   - Không cần giải thích chi tiết

2️⃣ CHAIN OF THOUGHT (Lab 9.3)
   - Mô hình suy nghĩ từng bước trước khi code
   - Tốn token nhưng độ chính xác cao hơn
   - Thích hợp cho bài toán phức tạp, có nhiều bước

3️⃣ CHAINING (Lab 9.4, 9.5)
   - Gộp prompts liên quan, tối ưu hóa chi phí
   - Có thể kiểm soát chi tiết quá trình
   - Thích hợp khi cần tinh chỉnh từng bước

🎓 KHI NÀO DÙNG CHIẾN LƯỢC NÀO?
   ┌────────────────┬──────────────┬────────────────────────┐
   │ Tình huống     │ Chiến lược   │ Lý do                  │
   ├────────────────┼──────────────┼────────────────────────┤
   │ Bài toán đơn   │ Baseline     │ Nhanh, rẻ              │
   │ Bài toán phức  │ CoT          │ Độ chính xác cao       │
   │ Production     │ Chaining     │ Tối ưu chi phí         │
   │ Xây dựng model │ CoT + Chain  │ Kết hợp cả hai         │
   └────────────────┴──────────────┴────────────────────────┘
""")
        
    except ValueError as e:
        print(f"❌ Lỗi: {e}")
    except Exception as e:
        print(f"❌ Lỗi API: {e}")


if __name__ == "__main__":
    main()
