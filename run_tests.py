import unittest
from test_refactored import TestDataManager

if __name__ == "__main__":
    # Создаем TestSuite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDataManager)

    # Запускаем тесты с детальным выводом
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Выводим итоговую статистику
    print("\n" + "=" * 50)
    print(f"Всего тестов: {result.testsRun}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    print("=" * 50)