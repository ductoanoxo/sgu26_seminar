import time
from fibonacci_recursive import fibonacci_recursive

n = 35
start = time.process_time()
result = fibonacci_recursive(n)
end = time.process_time()

print(f"Result: {result}")
print(f"Time taken: {end - start:.3f} seconds")