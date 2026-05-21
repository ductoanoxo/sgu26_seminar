import math
from typing import Tuple

def get_quadratic_roots_only_if_real(a: int, b: int, c: int) -> Tuple[float, float]:
    """
    Calculates the real roots of a quadratic equation ax^2 + bx + c = 0.
    
    Args:
        a: Quadratic coefficient.
        b: Linear coefficient.
        c: Constant term.
        
    Returns:
        A tuple containing the two real roots (root1, root2).
        
    Raises:
        ValueError: If the roots are complex (discriminant < 0) or if 'a' is zero.
    """
    if a == 0:
        raise ValueError("Coefficient 'a' must not be zero for a quadratic equation.")

    # Calculate the discriminant: b^2 - 4ac
    discriminant = b**2 - 4 * a * c
    
    if discriminant < 0:
        raise ValueError("The quadratic equation has complex roots (no real solutions).")
    
    sqrt_discriminant = math.sqrt(discriminant)
    
    root1 = (-b + sqrt_discriminant) / (2 * a)
    root2 = (-b - sqrt_discriminant) / (2 * a)
    
    return (float(root1), float(root2))