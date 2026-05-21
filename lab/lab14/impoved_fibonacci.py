import sys

# Tăng giới hạn số chữ số cho phép chuyển đổi thành chuỗi trong Python
# Vì Fibonacci(1.000.000) có hơn 200.000 chữ số.
sys.set_int_max_str_digits(300000)

def fibonacci_fast_doubling(n):
    """
    Tính số Fibonacci thứ n bằng thuật toán Fast Doubling.
    Độ phức tạp: O(log n)
    """
    if n == 0:
        return (0, 1)
    else:
        # Đệ quy xuống n/2
        a, b = fibonacci_fast_doubling(n >> 1)
        
        # Tính toán các giá trị dựa trên công thức Fast Doubling
        c = a * (b * 2 - a)
        d = a * a + b * b
        
        if n & 1: # Nếu n lẻ
            return (d, c + d)
        else:     # Nếu n chẵn
            return (c, d)

def get_nth_fibonacci(n):
    return fibonacci_fast_doubling(n)[0]

# Thực thi với REQUIRED_INPUT
n = 1000000
result = get_nth_fibonacci(n)

# Chỉ in ra số chữ số hoặc một phần kết quả vì nó quá dài
print(f"Tính thành công Fibonacci({n})")
print(f"Số chữ số của kết quả: {len(str(result))}")