
def test_cache_decorator():
    '''Comprehensive tests for cache decorator'''
    
    call_count = 0
    
    @cache_decorator
    def expensive_function(x):
        nonlocal call_count
        call_count += 1
        return x ** 2
    
    # Test 1: First call should compute
    result1 = expensive_function(5)
    assert result1 == 25
    assert call_count == 1
    
    # Test 2: Second call should use cache
    result2 = expensive_function(5)
    assert result2 == 25
    assert call_count == 1  # Not incremented
    
    # Test 3: Different argument should compute
    result3 = expensive_function(10)
    assert result3 == 100
    assert call_count == 2
    
    print("✅ All tests passed!")
