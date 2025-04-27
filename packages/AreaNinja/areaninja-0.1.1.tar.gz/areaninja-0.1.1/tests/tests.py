import math
import unittest

from geometry import Circle, Triangle


class TestGeometry(unittest.TestCase):

    def test_circle_area(self):
        circle = Circle(3)
        expected_area = math.pi * 9
        self.assertAlmostEqual(circle.area(), expected_area)

    def test_triangle_area(self):
        triangle = Triangle(3, 4, 5)
        expected_area = 6
        self.assertAlmostEqual(triangle.area(), expected_area)

    def test_right_triangle(self):
        triangle = Triangle(3, 4, 5)
        self.assertTrue(triangle.is_right_angled)

    def test_not_right_triangle(self):
        triangle = Triangle(5, 5, 5)
        self.assertFalse(triangle.is_right_angled)

    def test_invalid_circle(self):
        with self.assertRaises(ValueError):
            Circle(-1)

    def test_invalid_triangle(self):
        with self.assertRaises(ValueError):
            Triangle(1, 2, 3)


if __name__ == "__main__":
    unittest.main()
