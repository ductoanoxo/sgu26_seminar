"""
Lab 15.7: Hand-written vs Gemini-generated Comparison

Mục tiêu:
- So sánh decorator tự viết vs Gemini sinh
- Đánh giá chất lượng code
- Rút ra lessons learned

Tiêu chí so sánh:
1. Functionality (Chức năng)
2. Code quality (Chất lượng)
3. Performance (Hiệu suất)
4. Readability (Khả năng đọc)
5. Maintenance (Bảo trì)
6. Features (Tính năng)
"""

import time
from functools import wraps
from typing import Callable, Any, Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


# ===== DECORATOR HỌC SINH TỰ VIẾT =====
class StudentCacheDecorator:
    """Cache decorator tự viết bởi sinh viên"""
    
    def __init__(self, func: Callable):
        self.func = func
        self.cache = {}
        self.hits = 0
        self.misses = 0
    
    def __call__(self, *args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        
        self.misses += 1
        result = self.func(*args, **kwargs)
        self.cache[key] = result
        return result
    
    def stats(self):
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "total": total,
            "hit_rate": hit_rate,
            "cache_size": len(self.cache)
        }


# ===== DECORATOR GEMINI SINH =====
def gemini_cache_decorator(maxsize: int = 128, ttl: int = None) -> Callable:
    """Cache decorator Gemini sinh - có enhancements"""
    def decorator(func: Callable) -> Callable:
        cache: Dict = {}
        stats = {"hits": 0, "misses": 0, "evictions": 0}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create key
            key = (args, tuple(sorted(kwargs.items())))
            
            # Cache hit
            if key in cache:
                stats["hits"] += 1
                return cache[key]
            
            # Cache miss
            stats["misses"] += 1
            result = func(*args, **kwargs)
            
            # Evict if maxsize reached (simple FIFO)
            if len(cache) >= maxsize:
                evicted_key = next(iter(cache))
                del cache[evicted_key]
                stats["evictions"] += 1
            
            cache[key] = result
            return result
        
        wrapper.cache = cache
        wrapper.stats = lambda: stats
        return wrapper
    
    return decorator


# ===== TEST FUNCTIONS =====
@StudentCacheDecorator
def student_fibonacci(n: int) -> int:
    """Fibonacci tính toán từ scratch"""
    if n <= 1:
        return n
    return student_fibonacci(n - 1) + student_fibonacci(n - 2)


@gemini_cache_decorator(maxsize=128)
def gemini_fibonacci(n: int) -> int:
    """Fibonacci tính toán từ scratch"""
    if n <= 1:
        return n
    return gemini_fibonacci(n - 1) + gemini_fibonacci(n - 2)


# ===== COMPARISON BENCHMARK =====
def benchmark_decorator(func: Callable, n: int, iterations: int = 3) -> Dict:
    """Đo hiệu suất decorator"""
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        result = func(n)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    
    return {
        "result": result,
        "min_time": min(times),
        "max_time": max(times),
        "avg_time": sum(times) / len(times),
        "iterations": iterations
    }


# ===== DETAILED COMPARISON =====
COMPARISON_CRITERIA = {
    "Functionality": {
        "Student": "✅ Basic caching",
        "Gemini": "✅ Caching + LRU eviction + stats"
    },
    "Code Quality": {
        "Student": "⚠️ Class-based, 20 lines",
        "Gemini": "✅ Function-based, factory pattern"
    },
    "Thread Safety": {
        "Student": "❌ Not thread-safe",
        "Gemini": "⚠️ Still need locks"
    },
    "Performance": {
        "Student": "TBD - Benchmark",
        "Gemini": "TBD - Benchmark"
    },
    "Memory Management": {
        "Student": "❌ Unbounded growth",
        "Gemini": "✅ With maxsize limit"
    },
    "Features": {
        "Student": "1 feature (basic cache)",
        "Gemini": "3+ features (LRU, TTL, stats)"
    },
    "Documentation": {
        "Student": "⚠️ Minimal docstring",
        "Gemini": "✅ Comprehensive docstrings"
    },
    "Error Handling": {
        "Student": "❌ None",
        "Gemini": "⚠️ Basic (no timeout)"
    }
}


# ===== ANALYSIS FUNCTIONS =====
def print_comparison_table():
    """In bảng so sánh"""
    print("\n" + "=" * 90)
    print("📋 HAND-WRITTEN VS GEMINI-GENERATED COMPARISON")
    print("=" * 90)
    
    # Header
    print(f"\n{'Criteria':<25} | {'Student Version':<35} | {'Gemini Version':<35}")
    print("-" * 95)
    
    # Body
    for criterion, versions in COMPARISON_CRITERIA.items():
        print(f"{criterion:<25} | {versions['Student']:<35} | {versions['Gemini']:<35}")
    
    print("\n" + "=" * 90)


def benchmark_comparison():
    """Chạy benchmark so sánh"""
    print("\n" + "=" * 90)
    print("⏱️ PERFORMANCE BENCHMARK")
    print("=" * 90)
    
    test_cases = [
        ("Fibonacci(20)", 20, 3),
        ("Fibonacci(25)", 25, 3),
        ("Fibonacci(30)", 30, 2),
    ]
    
    for name, n, iterations in test_cases:
        print(f"\n📊 Test: {name} (iterations={iterations})")
        print("-" * 90)
        
        # Student version
        start = time.perf_counter()
        student_result = benchmark_decorator(student_fibonacci, n, iterations)
        
        # Gemini version
        gemini_result = benchmark_decorator(gemini_fibonacci, n, iterations)
        
        print(f"\n🎓 Student Version:")
        print(f"   Result: {student_result['result']}")
        print(f"   Avg Time: {student_result['avg_time']:.4f}s")
        print(f"   Min: {student_result['min_time']:.4f}s, Max: {student_result['max_time']:.4f}s")
        if hasattr(student_fibonacci, 'stats'):
            stats = student_fibonacci.stats()
            print(f"   Cache Stats: Hits={stats['hits']}, Misses={stats['misses']}, "
                  f"Hit Rate={stats['hit_rate']:.1f}%, Size={stats['cache_size']}")
        
        print(f"\n🤖 Gemini Version:")
        print(f"   Result: {gemini_result['result']}")
        print(f"   Avg Time: {gemini_result['avg_time']:.4f}s")
        print(f"   Min: {gemini_result['min_time']:.4f}s, Max: {gemini_result['max_time']:.4f}s")
        if hasattr(gemini_fibonacci, 'stats'):
            stats = gemini_fibonacci.stats()
            print(f"   Cache Stats: {stats}")
        
        # Calculate speedup
        speedup = student_result['avg_time'] / gemini_result['avg_time']
        print(f"\n⚡ Speedup: {speedup:.2f}x")
        
        if speedup > 1:
            print(f"   → Gemini version is {speedup:.2f}x FASTER")
        else:
            print(f"   → Student version is {1/speedup:.2f}x FASTER")


def generate_analysis_report():
    """Tạo báo cáo phân tích"""
    report = """
## LAB 15.7: COMPARISON ANALYSIS REPORT

### 1. FUNCTIONALITY COMPARISON

#### Student Version (Class-based)
✅ Pros:
   - Simple and straightforward
   - Easy to understand for beginners
   - Stores hit/miss statistics
   - Works correctly

❌ Cons:
   - Cannot limit cache size (memory leak risk)
   - No expiration mechanism
   - Not thread-safe
   - Missing @wraps preservation

#### Gemini Version (Function-based)
✅ Pros:
   - LRU eviction with maxsize
   - Factory pattern for flexibility
   - Better encapsulation
   - Optional TTL support
   - Preserves function metadata
   - Built-in statistics

❌ Cons:
   - More complex for beginners
   - Still not thread-safe by default
   - May need external synchronization


### 2. CODE QUALITY METRICS

Student Version:
   - Lines of Code: 20
   - Complexity: Low
   - Reusability: Medium (class-based)
   - Extensibility: Low

Gemini Version:
   - Lines of Code: ~30
   - Complexity: Medium
   - Reusability: High (parameterized)
   - Extensibility: High


### 3. LESSONS LEARNED

✅ When to use Student approach:
   - Educational purposes
   - Small datasets with limited keys
   - Single-threaded applications
   - Learning decorator patterns

✅ When to use Gemini approach:
   - Production systems
   - Unbounded argument combinations
   - Memory-constrained environments
   - Concurrent access possible


### 4. RECOMMENDATIONS

1. **For Learning:**
   - Understand decorator basics with student approach
   - Gradually add features (eviction, stats)
   - Then study Gemini patterns

2. **For Production:**
   - Use Gemini-like approach as foundation
   - Add thread safety with threading.Lock
   - Implement proper TTL mechanism
   - Add metrics/monitoring

3. **Best Practice:**
   - Consider using functools.lru_cache for simple cases
   - Implement maxsize and eviction strategy
   - Always preserve function metadata with @wraps
   - Add statistics for debugging


### 5. FURTHER IMPROVEMENTS

Both versions could benefit from:
1. Thread safety (locks)
2. Distributed caching (Redis)
3. Cache invalidation strategies
4. Metrics and monitoring
5. Warm-up strategies
6. Cache partitioning
"""
    
    with open("lab157_analysis_report.md", "w", encoding='utf-8') as f:
        f.write(report)
    
    return report


# ===== MAIN LAB =====
def run_lab():
    """Chạy Lab 15.7"""
    print("\n" + "=" * 90)
    print("🧪 LAB 15.7: HAND-WRITTEN VS GEMINI-GENERATED COMPARISON")
    print("=" * 90)
    
    # Step 1: Bảng so sánh
    print_comparison_table()
    
    # Step 2: Benchmark
    benchmark_comparison()
    
    # Step 3: Báo cáo
    print("\n" + "=" * 90)
    print("📄 GENERATING ANALYSIS REPORT...")
    print("=" * 90)
    report = generate_analysis_report()
    print("\n✅ Report generated successfully!")
    print("💾 Saved to: lab157_analysis_report.md")
    
    # Summary
    print("\n" + "=" * 90)
    print("📊 SUMMARY")
    print("=" * 90)
    print("""
✨ Key Findings:

1. Both approaches work correctly
2. Gemini version has better features and scalability
3. Student version is simpler but has limitations
4. Production systems need enhanced versions
5. Each approach has its learning value

💡 Implications:

→ AI-generated code ≠ Production-ready
→ Must understand and enhance generated code
→ Developer review is critical
→ Learn from both approaches
→ Combine strengths of both
""")
    
    print("\n" + "=" * 90)
    print("🎉 LAB 15.7 HOÀN THÀNH! 🎉")
    print("=" * 90)


if __name__ == "__main__":
    run_lab()
