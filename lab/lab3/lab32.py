def get_geometric_mean(*nums: float) -> float:
    """
    Get the geometric mean of a list of floating-point numbers
    """
    # Your code here
    product = 1.0
    for num in nums:
        product *= num
    return product ** (1 / len(nums))