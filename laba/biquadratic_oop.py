import sys
import math


class BiquadraticEquation:

    def __init__(self): #конструктор класса

        self.coef_A = 0.0
        self.coef_B = 0.0
        self.coef_C = 0.0
        self.roots = []

    def get_coef(self, index, prompt):

        while True:
            try:
                if index < len(sys.argv):
                    coef_str = sys.argv[index]
                else:
                    print(prompt)
                    coef_str = input()
                coef = float(coef_str)
                return coef
            except (ValueError, IndexError):
                print("Ошибка: введите действительное число")

    def get_coefs(self):

        self.coef_A = self.get_coef(1, 'Введите коэффициент А:')
        self.coef_B = self.get_coef(2, 'Введите коэффициент B:')
        self.coef_C = self.get_coef(3, 'Введите коэффициент C:')

    def _solve_quadratic(self, a, b, c):

        if a == 0:
            raise ValueError("Коэффициент A не может быть равен 0")
        D = b * b - 4 * a * c
        if D < 0:
            return []
        elif D == 0.0:
            root = -b / (2.0 * a)
            return [root]
        else:
            sqD = math.sqrt(D)
            root1 = (-b + sqD) / (2.0 * a)
            root2 = (-b - sqD) / (2.0 * a)
            return [root1, root2]

    def calculate_roots(self):
        if self.coef_A == 0:
            raise ValueError("Коэффициент A не может быть равен 0 для биквадратного уравнения")

        self.roots = []


        t_roots = self._solve_quadratic(self.coef_A, self.coef_B, self.coef_C)

        for t in t_roots:
            if t > 0:
                self.roots.append(math.sqrt(t))
                self.roots.append(-math.sqrt(t))
            elif t == 0:
                self.roots.append(0.0)

        self.roots = sorted(set(self.roots))

    def get_roots_count(self):

        return len(self.roots)

    def print_roots(self):

        roots_count = self.get_roots_count()

        if roots_count == 0:
            print('Нет действительных корней')
        elif roots_count == 1:
            print(f'Один корень: {self.roots[0]}')
        elif roots_count == 2:
            print(f'Два корня: {self.roots[0]} и {self.roots[1]}')
        elif roots_count == 3:
            print(f'Три корня: {self.roots[0]}, {self.roots[1]} и {self.roots[2]}')
        elif roots_count == 4:
            print(f'Четыре корня: {self.roots[0]}, {self.roots[1]}, {self.roots[2]} и {self.roots[3]}')

    def print_equation(self):

        print(f'Уравнение: {self.coef_A}x⁴ + {self.coef_B}x² + {self.coef_C} = 0')


def main():

    print("Решение биквадратного уравнения Ax⁴ + Bx² + C = 0")

    equation = BiquadraticEquation() # создание объекта класса

    equation.get_coefs()
    equation.print_equation()

    try:
        equation.calculate_roots()
        equation.print_roots()
    except ValueError as e:
        print(f'Ошибка: {e}')


if __name__ == "__main__":
    main()