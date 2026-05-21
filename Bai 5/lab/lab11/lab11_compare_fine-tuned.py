def calculate_discriminant(a: int, b: int, c: int) -> float:
    return (b ** 2) - (4 * a * c)


def has_real_roots(discriminant: float) -> bool:
    return discriminant >= 0


def calculate_roots(a: int, b: int, discriminant: float) -> tuple:
    root1 = (-b + discriminant ** 0.5) / (2 * a)
    root2 = (-b - discriminant ** 0.5) / (2 * a)
    return root1, root2


def get_quadratic_roots_only_if_real(a: int, b: int, c: int):
    discriminant = calculate_discriminant(a, b, c)
    if not has_real_roots(discriminant):
        return None
    return calculate_roots(a, b, discriminant)