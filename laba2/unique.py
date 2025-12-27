class Unique(object):
    def __init__(self, items, **kwargs):
        self.ignore_case = kwargs.get('ignore_case', False)
        self.items = iter(items)
        self.seen = set()

    def __next__(self):
        while True:
            item = next(self.items)

            # Определяем ключ для сравнения
            if self.ignore_case and isinstance(item, str):
                key = item.lower()
            else:
                key = item

            # Если элемент еще не встречался, добавляем и возвращаем
            if key not in self.seen:
                self.seen.add(key)
                return item

    def __iter__(self):
        return self

# Тест 1: Числа
print("Тест 1 - числа:")
data1 = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
for item in Unique(data1):
    print(item, end=" ")
print()  # Вывод: 1 2

# Тест 2: С генератором
print("\nТест 2 - с генератором:")
def gen_random(num_count, begin, end):
    import random
    for _ in range(num_count):
        yield random.randint(begin, end)

data2 = gen_random(10, 1, 3)
for item in Unique(data2):
    print(item, end=" ")
print()  # Вывод: 1 2 3 (в случайном порядке)

# Тест 3: Строки без ignore_case
print("\nТест 3 - строки (ignore_case=False):")
data3 = ['a', 'A', 'b', 'B', 'a', 'A', 'b', 'B']
for item in Unique(data3):
    print(item, end=" ")
print()  # Вывод: a A b B

# Тест 4: Строки с ignore_case=True
print("\nТест 4 - строки (ignore_case=True):")
data4 = ['a', 'A', 'b', 'B', 'a', 'A', 'b', 'B']
for item in Unique(data4, ignore_case=True):
    print(item, end=" ")
print()  # Вывод: a b