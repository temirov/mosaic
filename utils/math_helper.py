import math
from typing import Callable


class MathHelper:
    @classmethod
    def value_or_max(cls, fn: Callable[[], int], max: int) -> int:
        value = fn()
        if value > max:
            return max
        else:
            return value

    @classmethod
    def value_or_min(cls, fn: Callable[[], int], min: int) -> int:
        value = fn()
        if value < min:
            return min
        else:
            return value

    @classmethod
    def diagonal(cls, left_top: tuple[int, int], right_bottom: tuple[int, int]) -> float:
        return math.dist(left_top, right_bottom)

    @classmethod
    def resize(
            cls,
            size: tuple[int, int],
            diagonal: tuple[tuple[int, int], tuple[int, int]],
            delta: int,
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        right_max, bottom_max = size
        ((left, top), (right, bottom)) = diagonal
        resized_left = cls.value_or_min(lambda: left - delta, 0)
        resized_right = cls.value_or_max(lambda: right + delta, right_max)
        resized_top = cls.value_or_min(lambda: top - delta, 0)
        resized_bottom = cls.value_or_max(lambda: bottom + delta, bottom_max)

        return (resized_left, resized_top), (resized_right, resized_bottom)
