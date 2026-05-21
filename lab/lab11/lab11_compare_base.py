def calculate_discriminant(a: int, b: int, c: int) -> int:
    return b**2 - 4 * a * c


def calculate_real_roots(a: int, b: int, discriminant: float) -> tuple:
    root_part = discriminant**0.5
    denominator = 2 * a
    root_1 = (-b + root_part) / denominator
    root_2 = (-b - root_part) / denominator
    return root_1, root_2


def get_quadratic_roots_only_if_real(a: int, b: int, c: int):
    discriminant = calculate_discriminant(a, b, c)

    if discriminant < 0:
        return None

    return calculate_real_roots(a, b, discriminant)