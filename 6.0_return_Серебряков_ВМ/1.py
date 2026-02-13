def get_boundaries(target, margin):
    low_limit = target - margin
    high_limit = target + margin
    return low_limit, high_limit
a,b = get_boundaries(100, 20)
print(f"Нижний предел: {a}, верхний предел: {b}")