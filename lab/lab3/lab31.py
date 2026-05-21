def get_geometric_mean_of_two_numbers(
    a: float,
    b: float,
) -> float:
    """
    Get the geometric mean of two floating-point numbers
    """
    # Your code here
    return (a * b) ** 0.5
num1: float = 5.0
num2: float = 20.0
print(f"The geometric mean of {num1} and {num2} is: {get_geometric_mean_of_two_numbers(num1, num2)}")


