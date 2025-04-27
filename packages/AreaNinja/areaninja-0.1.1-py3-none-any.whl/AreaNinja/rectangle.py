from .geometry import Figure


class Rectangle(Figure):

    def __init__(self, a: int | float, b: int | float):
        self.a = a
        self.b = b

    def _validate(self):
        if self.a <= 0 or self.b <= 0:
            raise ValueError("All sides must be positive")

    def area(self):
        return self.a * self.b
