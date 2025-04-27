from math import sqrt

from .geometry import Figure


class Triangle(Figure):
    def __init__(self, a: int | float, b: int | float, c: int | float):
        self.a = a
        self.b = b
        self.c = c
        self._validate()

    def _validate(self) -> None:
        if any([self.a <= 0, self.b <= 0, self.c <= 0]):
            raise ValueError("All sides must be positive")
        elif any([
            self.a + self.b <= self.c,
            self.b + self.c <= self.a,
            self.c + self.a <= self.b
        ]):
            raise ValueError("Invalid triangle")

    def area(self) -> float:
        p = (self.a + self.b + self.c) / 2
        return sqrt((p * (p - self.a) * (p - self.b) * (p - self.c)))

    @property
    def is_right_angled(self) -> bool:
        """Checking that the triangle is right-angled"""
        sides = sorted([self.a, self.b, self.c])
        return round(sides[2] ** 2) == round(sides[0] ** 2 + sides[1] ** 2)
