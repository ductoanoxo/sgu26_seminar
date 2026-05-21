import time

def fibonacci_recursive(n):
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

print("n\tfib(n)\truntime(s)")
for n in range(10, 41, 5):
    t0 = time.perf_counter()
    val = fibonacci_recursive(n)
    t1 = time.perf_counter()
    print(f"{n}\t{val}\t{t1 - t0:.6f}")