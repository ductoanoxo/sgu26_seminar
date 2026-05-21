import time

def fibonacci_recursive(n):
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

n = 35

t0 = time.perf_counter()
result = fibonacci_recursive(n)
t1 = time.perf_counter()

print(f"fib({n}) = {result}")
print(f"runtime = {t1 - t0:.6f} seconds")