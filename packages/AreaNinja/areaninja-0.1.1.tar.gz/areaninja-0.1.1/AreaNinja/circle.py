from math import pi

from .geometry import Figure


class Circle(Figure):
    def __init__(self, radius: int | float):
        self.radius = radius
        self._validate()

    def _validate(self) -> None:
        if self.radius <= 0:
            raise ValueError("Radius must be positive")

    def area(self) -> float:
        return pi * self.radius ** 2
