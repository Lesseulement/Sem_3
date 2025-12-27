import random

def gen_random(num_count, begin, end):
    result = []
    for i in range(num_count):
        result.append(random.randint(begin, end))
    return result

print("5 чисел от 1 до 3:")
print(gen_random(5, 1, 3))

print("\n10 чисел от -5 до 5:")
print(gen_random(10, -5, 5))

print("\n3 числа от 10 до 10:")
print(gen_random(3, 10, 10))