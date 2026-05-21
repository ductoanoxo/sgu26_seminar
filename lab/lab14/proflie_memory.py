from memory_profiler import profile
from fibonacci_recursive import fibonacci_recursive

@profile
def test_memory():
    # Thử với n nhỏ hơn vì đệ quy sâu rất tốn bộ nhớ stack
    return fibonacci_recursive(30)

if __name__ == "__main__":
    test_memory()