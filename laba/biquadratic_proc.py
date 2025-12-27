import sys
import math


def get_coef(index, prompt):
    """Получить коэффициент от пользователя"""
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


def solve_quadratic(a, b, c):
    """Решить квадратное уравнение at² + bt + c = 0"""
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


def solve_biquadratic(A, B, C):
    """Решить биквадратное уравнение Ax⁴ + Bx² + C = 0"""
    if A == 0:
        raise ValueError("Коэффициент A не может быть равен 0 для биквадратного уравнения")

    roots = []

    # Решаем квадратное относительно t = x²
    t_roots = solve_quadratic(A, B, C)

    # Для каждого t находим x
    for t in t_roots:
        if t > 0:
            roots.append(math.sqrt(t))
            roots.append(-math.sqrt(t))
        elif t == 0:
            roots.append(0.0)

    # Убираем дубликаты и сортируем
    roots = sorted(set(roots))
    return roots


def print_roots(roots):
    """Вывести корни в удобном формате"""
    roots_count = len(roots)

    if roots_count == 0:
        print('Нет действительных корней')
    elif roots_count == 1:
        print(f'Один корень: {roots[0]}')
    elif roots_count == 2:
        print(f'Два корня: {roots[0]} и {roots[1]}')
    elif roots_count == 3:
        print(f'Три корня: {roots[0]}, {roots[1]} и {roots[2]}')
    elif roots_count == 4:
        print(f'Четыре корня: {roots[0]}, {roots[1]}, {roots[2]} и {roots[3]}')


def print_equation(A, B, C):
    """Вывести уравнение в красивом формате"""
    print(f'Уравнение: {A}x⁴ + {B}x² + {C} = 0')


def main():
    """Основная процедурная функция"""
    print("Решение биквадратного уравнения Ax⁴ + Bx² + C = 0")
    print("Процедурная версия")

    # Получаем коэффициенты
    A = get_coef(1, 'Введите коэффициент А:')
    B = get_coef(2, 'Введите коэффициент B:')
    C = get_coef(3, 'Введите коэффициент C:')

    # Выводим уравнение
    print_equation(A, B, C)

    try:
        # Решаем уравнение
        roots = solve_biquadratic(A, B, C)
        # Выводим результат
        print_roots(roots)
    except ValueError as e:
        print(f'Ошибка: {e}')


if __name__ == "__main__":
    main()