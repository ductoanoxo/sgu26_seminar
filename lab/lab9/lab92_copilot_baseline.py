"""
Lab 9.2: Baseline Strategy với GitHub Copilot

Mục tiêu:
- Sử dụng GitHub Copilot trong VS Code để hoàn thiện hàm
- So sánh kết quả giữa OpenAI API (Lab 9.1) và GitHub Copilot
- Thấy sự khác biệt trong cách tiếp cận

Hướng dẫn:
1. Mở file này trong VS Code
2. Nhìn vào hàm get_geometric_mean() dưới đây là chữ ký hàm từ Lab 9.1
3. Gõ từng ký tự của function body sẽ thấy Copilot gợi ý ghost text
4. Nhấn Tab để chấp nhận gợi ý, Esc để từ chối
5. Kiểm tra xem Copilot gợi ý gì

GitHub Copilot Baseline:
- Không cần prompt tường minh
- Copilot tự động phân tích ngữ cảnh file
- Nhanh và tương tác trực tiếp
"""

from typing import Dict
import numpy as np


# ===== PHẦN 1: COPILOT GỢI Ý =====
# Hãy tìm bắt đầu gõ hàm này - Copilot sẽ gợi ý phần body
# Copilot sẽ xem lên phía trên thấy import Dict, np và hiểu ngữ cảnh

def get_geometric_mean(net_returns: Dict[str, float]) -> float:
    values = list(net_returns.values())
    
    if not values:
        raise ValueError("net_returns không được rỗng")
    
    # Chuyển sang dạng (1 + r)
    returns = [1 + v for v in values]
    
    # Dùng numpy cho đúng context Copilot (vì đã import np)
    product = np.prod(returns)
    
    n = len(returns)
    return product ** (1 / n) - 1


# ===== PHẦN 2: KIỂM CHỨNG KẾT QUẢ =====
# Sau khi Copilot hoàn thiện hàm, chạy phần này để kiểm chứng

def test_geometric_mean():
    """Kiểm chứng kết quả của Copilot"""
    
    print("=" * 70)
    print("🧪 KIỂM CHỨNG: get_geometric_mean()")
    print("=" * 70)
    
    # Test case 1: Lợi suất dương
    test_case_1 = {"2021": 0.10, "2022": 0.20, "2023": -0.05}
    result_1 = get_geometric_mean(test_case_1)
    expected_1 = (1.10 * 1.20 * 0.95) ** (1/3) - 1
    
    print(f"\n✅ Test Case 1: Lợi suất hỗn hợp")
    print(f"   Input: {test_case_1}")
    print(f"   Kết quả: {result_1:.6f}")
    print(f"   Mong đợi: {expected_1:.6f}")
    print(f"   {'✅ Đúng' if abs(result_1 - expected_1) < 0.0001 else '❌ Sai'}")
    
    # Test case 2: Lợi suất nhỏ
    test_case_2 = {"2021": 0.05, "2022": 0.05, "2023": 0.05}
    result_2 = get_geometric_mean(test_case_2)
    expected_2 = (1.05 * 1.05 * 1.05) ** (1/3) - 1
    
    print(f"\n✅ Test Case 2: Lợi suất đồng đều")
    print(f"   Input: {test_case_2}")
    print(f"   Kết quả: {result_2:.6f}")
    print(f"   Mong đợi: {expected_2:.6f}")
    print(f"   {'✅ Đúng' if abs(result_2 - expected_2) < 0.0001 else '❌ Sai'}")
    
    # Test case 3: Một năm
    test_case_3 = {"2021": 0.15}
    result_3 = get_geometric_mean(test_case_3)
    expected_3 = 0.15
    
    print(f"\n✅ Test Case 3: Lợi suất một năm")
    print(f"   Input: {test_case_3}")
    print(f"   Kết quả: {result_3:.6f}")
    print(f"   Mong đợi: {expected_3:.6f}")
    print(f"   {'✅ Đúng' if abs(result_3 - expected_3) < 0.0001 else '❌ Sai'}")


# ===== PHẦN 3: SO SÁNH COPILOT vs OPENAI API =====
def compare_with_lab91():
    """
    So sánh kết quả Copilot (Lab 9.2) với OpenAI API (Lab 9.1)
    
    Hãy chạy Lab 9.1 trước, sau đó đọc nội dung lab91_baseline_result.txt
    và điền vào bảng so sánh dưới đây:
    """
    
    print("\n" + "=" * 70)
    print("📊 SO SÁNH: COPILOT vs OPENAI API")
    print("=" * 70)
    
    comparison = {
        "Tiêu chí": ["Tốc độ", "Chi phí", "Độ chính xác", "Dễ sử dụng"],
        "Copilot (Lab 9.2)": ["⚡ Rất nhanh", "💰 Miễn phí", "✅ Tốt", "✅ Rất dễ"],
        "OpenAI API (Lab 9.1)": ["🐌 Một vài giây", "💸 Phải trả tiền", "✅ Tốt", "⚠️ Cần setup"]
    }
    
    print("\n")
    for i, criterion in enumerate(comparison["Tiêu chí"]):
        print(f"{criterion:15} | Copilot: {comparison['Copilot (Lab 9.2)'][i]:20} | API: {comparison['OpenAI API (Lab 9.1)'][i]}")
    
    print("\n📝 Nhận xét:")
    print("   - Copilot gợi ý dựa trên ngữ cảnh file (imports, tên biến, type hints)")
    print("   - OpenAI API yêu cầu prompt tường minh (structured prompt)")
    print("   - Copilot nhanh hơn vì không cần gọi API")
    print("   - OpenAI API cần thiết lập API key, nhưng hiệu suất tương tự")
    

# ===== PHẦN 4: GHI CHÚ VỀ COPILOT PROMPT =====
def explain_copilot_prompting():
    """
    Giải thích cách Copilot hoạt động như một "prompt" Baseline
    
    Copilot không cần prompt tường minh. Thay vào đó, nó sử dụng:
    1. Type hints: `net_returns: Dict[str, float]` → Copilot biết input là dict
    2. Tên hàm + docstring: `get_geometric_mean()` → Copilot biết cần tính hình học
    3. Imports ở trên: `import numpy as np` → Copilot sẽ ưu tiên sử dụng numpy
    4. Lịch sử file: Copilot xem các hàm đã viết trước để làm reference
    
    Code clean chính là "prompt" tốt nhất cho Copilot!
    """
    
    print("\n" + "=" * 70)
    print("💡 CÁC TIPS VỀ COPILOT PROMPTING")
    print("=" * 70)
    print(explain_copilot_prompting.__doc__)


if __name__ == "__main__":
    print("\n⚠️  HƯỚNG DẪN SỬ DỤNG LAB 9.2:")
    print("-" * 70)
    print("1. Mở file này (lab92_copilot_baseline.py) trong VS Code")
    print("2. Nhìn vào hàm get_geometric_mean() - thấy 'pass' chưa hoàn thiện")
    print("3. Xóa dòng 'pass' và bắt đầu gõ thân hàm")
    print("4. Copilot sẽ tự động gợi ý ghost text (mã xám nhạt)")
    print("5. Nhấn Tab để chấp nhận, Esc để từ chối")
    print("6. Sau khi hoàn thiện, bỏ comment dòng 'pass' và chạy test")
    print("-" * 70)
    
    try:
        # Chỉ kiểm chứng kết quả nếu hàm đã được hoàn thiện
        if get_geometric_mean.__code__.co_code != b'd\x00S\x00':
            test_geometric_mean()
            compare_with_lab91()
            explain_copilot_prompting()
        else:
            print("\n❌ Hàm get_geometric_mean() chưa được hoàn thiện!")
            print("💡 Hãy sử dụng GitHub Copilot để hoàn thiện nó")
            
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        print("💡 Hãy hoàn thiện hàm get_geometric_mean() trước")
