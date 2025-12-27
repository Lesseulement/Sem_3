import time

# Способ 1: cm_timer_1
class cm_timer_1:
    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed_time = time.time() - self.start_time
        print(f"time: {elapsed_time:.1f}")

# Способ 2: cm_timer_2
class cm_timer_2:
    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed_time = time.time() - self.start_time
        print(f"time: {elapsed_time:.1f}")

# Тестирование
if __name__ == '__main__':
    print("Тест cm_timer_1:")
    with cm_timer_1():
        time.sleep(2.5)

    print("\nТест cm_timer_2:")
    with cm_timer_2():
        time.sleep(1.5)