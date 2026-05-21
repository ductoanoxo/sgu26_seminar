from functools import reduce  


def get_geometric_mean_for_three_numbers(a, b, c): 
    """
    Calculate the geometric mean of three numbers.
    
    The geometric mean is the third root of the product of three numbers.
    It is commonly used to find the average rate of change over time or
    to compare quantities with different units.
    
    Args:
        a (float): The first number.
        b (float): The second number.
        c (float): The third number.
    
    Returns:
        float: The geometric mean of the three numbers (cube root of a*b*c).
    
    Example:
        >>> get_geometric_mean_for_three_numbers(2, 4, 8)
        4.0
        
        >>> get_geometric_mean_for_three_numbers(1, 1, 1)
        1.0
    
    Note:
        All input numbers should be non-negative for meaningful results,
        as taking the root of a negative product may result in complex numbers.
    """
    return (a*b*c)**(1/3)


def get_geometric_mean(*nums: float) -> float: 
    """ 
    Get the geometric mean of a sequence of numbers  
    """ 

    if not len(nums):  
        raise ValueError("Cannot calculate the geometric mean of an empty sequence") 

    product = reduce(lambda a, b: a * b, nums) 
    if product < 0 and len(nums) % 2 == 0: 
        raise ValueError("Cannot calculate the geometric mean") 

    return pow(product, 1 / len(nums)) 


