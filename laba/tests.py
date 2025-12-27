import unittest
import math
from biquadratic_oop import BiquadraticEquation
from biquadratic_proc import solve_biquadratic


class TestBiquadratic(unittest.TestCase):
    """Тесты для биквадратного уравнения"""

    def test_four_roots(self):
        """Тест уравнения с 4 корнями: x⁴ - 5x² + 4 = 0"""
        # Процедурный подход
        roots = solve_biquadratic(1, -5, 4)
        expected = [-2, -1, 1, 2]
        self.assertEqual(len(roots), 4)
        for r, e in zip(sorted(roots), sorted(expected)):
            self.assertAlmostEqual(r, e, places=5)

        # ООП подход
        eq = BiquadraticEquation()
        eq.coef_A = 1
        eq.coef_B = -5
        eq.coef_C = 4
        eq.calculate_roots()
        self.assertEqual(eq.get_roots_count(), 4)

    def test_two_roots(self):
        """Тест уравнения с 2 корнями: x⁴ - 3x² = 0"""
        roots = solve_biquadratic(1, -3, 0)
        expected = [-math.sqrt(3), 0, math.sqrt(3)]
        self.assertEqual(len(roots), 3)

    def test_no_roots(self):
        """Тест уравнения без корней: x⁴ + x² + 1 = 0"""
        roots = solve_biquadratic(1, 1, 1)
        self.assertEqual(len(roots), 0)

    def test_one_root(self):
        """Тест уравнения с одним корнем: x⁴ = 0"""
        roots = solve_biquadratic(1, 0, 0)
        self.assertEqual(len(roots), 1)
        self.assertAlmostEqual(roots[0], 0)

    def test_invalid_A_zero(self):
        """Тест с нулевым коэффициентом A"""
        with self.assertRaises(ValueError):
            solve_biquadratic(0, 1, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)