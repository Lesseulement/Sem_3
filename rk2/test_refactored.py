import unittest
from rk2.refactored import DataManager


class TestDataManager(unittest.TestCase):
    def setUp(self):
        """Настройка тестового окружения перед каждым тестом"""
        self.manager = DataManager()

    def test_query_1_structure(self):
        """Тест 1: Проверка структуры данных для запроса 1"""
        result = self.manager.query_1()

        # Проверяем, что результат - список
        self.assertIsInstance(result, list)

        # Проверяем, что список не пустой
        self.assertGreater(len(result), 0)

        # Проверяем структуру каждого элемента
        for item in result:
            self.assertEqual(len(item), 3)  # 3 элемента: модель, объем, компьютер
            self.assertIsInstance(item[0], str)  # модель - строка
            self.assertIsInstance(item[1], int)  # объем - целое число
            self.assertIsInstance(item[2], str)  # компьютер - строка

    def test_query_2_calculation(self):
        """Тест 2: Проверка правильности расчетов для запроса 2"""
        result = self.manager.query_2()

        # Проверяем, что результат - список кортежей
        self.assertIsInstance(result, list)

        # Проверяем количество компьютеров с жесткими дисками
        # В тестовых данных все компьютеры имеют жесткие диски
        self.assertEqual(len(result), len(self.manager.computers))

        # Проверяем структуру каждого элемента
        for computer_name, drive_count in result:
            self.assertIsInstance(computer_name, str)
            self.assertIsInstance(drive_count, int)
            self.assertGreater(drive_count, 0)  # у каждого компьютера должен быть хотя бы 1 диск

        # Проверяем сортировку по количеству дисков (по возрастанию)
        for i in range(len(result) - 1):
            self.assertLessEqual(result[i][1], result[i + 1][1])

    def test_query_3_filtering(self):
        """Тест 3: Проверка фильтрации для запроса 3"""
        result = self.manager.query_3()

        # Проверяем, что результат - список
        self.assertIsInstance(result, list)

        # Проверяем, что все модели заканчиваются на 'TB'
        for item in result:
            model = item[0]
            self.assertTrue(model.endswith("TB"),
                            f"Модель '{model}' не заканчивается на 'TB'")

        # Проверяем сортировку по модели (алфавитная)
        for i in range(len(result) - 1):
            self.assertLessEqual(result[i][0], result[i + 1][0])

    def test_one_to_many_relations(self):
        """Дополнительный тест: проверка связей один-ко-многим"""
        relations = self.manager.get_one_to_many_relations()

        # Проверяем, что у каждого жесткого диска есть компьютер
        self.assertEqual(len(relations), len(self.manager.hard_drives))

        # Проверяем соответствие ID
        for hd in self.manager.hard_drives:
            # Находим компьютер по computer_id
            computer = next((c for c in self.manager.computers
                             if c.id == hd.computer_id), None)
            self.assertIsNotNone(computer,
                                 f"Для жесткого диска {hd.id} не найден компьютер с ID {hd.computer_id}")

    def test_many_to_many_relations(self):
        """Дополнительный тест: проверка связей многие-ко-многим"""
        relations = self.manager.get_many_to_many_relations()

        # Проверяем, что количество связей соответствует промежуточной таблице
        self.assertEqual(len(relations), len(self.manager.computer_hard_drives))


if __name__ == "__main__":
    # Запуск всех тестов
    unittest.main(verbosity=2)