import random


def generate_table(x, y):
    return [[random.random() for _ in range(x)] for _ in range(y)]  # noqa: S311
