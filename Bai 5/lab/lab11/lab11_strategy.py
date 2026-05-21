def get_quadratic_roots_only_if_real(a, b, c):
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return None
    root1 = (-b + discriminant**0.5) / (2 * a)
    root2 = (-b - discriminant**0.5) / (2 * a)
    return root1, root2