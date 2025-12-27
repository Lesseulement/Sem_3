class HardDrive:
    def __init__(self, id, model, capacity, computer_id):
        self.id = id
        self.model = model
        self.capacity = capacity
        self.computer_id = computer_id


class Computer:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class ComputerHardDrive:
    def __init__(self, computer_id, hard_drive_id):
        self.computer_id = computer_id
        self.hard_drive_id = hard_drive_id


class DataManager:
    def __init__(self):
        self.hard_drives = [
            HardDrive(1, "WD Blue 1TB", 1000, 1),
            HardDrive(2, "Seagate Barracuda 2TB", 2000, 2),
            HardDrive(3, "Samsung 870 EVO 500GB", 500, 2),
            HardDrive(4, "Toshiba P300 3TB", 3000, 3),
            HardDrive(5, "Kingston NV1 1TB", 1000, 4),
            HardDrive(6, "Crucial MX500 2TB", 2000, 5),
        ]

        self.computers = [
            Computer(1, "ИБМ-001"),
            Computer(2, "MacBook-Pro"),
            Computer(3, "Asus-Gaming"),
            Computer(4, "Huawei"),
            Computer(5, "Lenovo-Ultra"),
        ]

        self.computer_hard_drives = [
            ComputerHardDrive(1, 1),
            ComputerHardDrive(2, 2),
            ComputerHardDrive(2, 3),
            ComputerHardDrive(3, 4),
            ComputerHardDrive(4, 5),
            ComputerHardDrive(5, 6),
            ComputerHardDrive(1, 2),
            ComputerHardDrive(4, 1),
            ComputerHardDrive(5, 4),
        ]

    def get_one_to_many_relations(self):
        """Получить связи один-ко-многим (жесткий диск -> компьютер)"""
        return [
            [hd.model, hd.capacity, comp.name]
            for hd in self.hard_drives
            for comp in self.computers
            if hd.computer_id == comp.id
        ]

    def get_many_to_many_relations(self):
        """Получить связи многие-ко-многим через промежуточную таблицу"""
        many_to_many_first = [
            [comp.name, comp_hd.computer_id, comp_hd.hard_drive_id]
            for comp in self.computers
            for comp_hd in self.computer_hard_drives
            if comp.id == comp_hd.computer_id
        ]

        many_to_many = [
            [hd.model, hd.capacity, comp_name]
            for comp_name, comp_id, hd_id in many_to_many_first
            for hd in self.hard_drives
            if hd.id == hd_id
        ]

        return many_to_many

    def query_1(self):
        """Запрос 1: Список всех связанных жестких дисков и компьютеров, отсортированный по жестким дискам"""
        one_to_many = self.get_one_to_many_relations()
        return sorted(one_to_many, key=lambda x: x[0])

    def query_2(self):
        """Запрос 2: Список компьютеров с количеством жестких дисков в каждом, отсортированный по количеству дисков"""
        one_to_many = self.get_one_to_many_relations()
        result = []

        for comp in self.computers:
            drives_in_comp = list(filter(lambda x: x[2] == comp.name, one_to_many))
            if len(drives_in_comp) > 0:
                result.append((comp.name, len(drives_in_comp)))

        result.sort(key=lambda x: x[1])
        return result

    def query_3(self):
        """Запрос 3: Список всех жестких дисков, у которых модель заканчивается на 'TB', и названия их компьютеров"""
        many_to_many = self.get_many_to_many_relations()
        result = []

        for model, capacity, comp_name in many_to_many:
            if model.endswith("TB"):
                result.append([model, capacity, comp_name])

        result.sort(key=lambda x: x[0])
        return result


def main():
    manager = DataManager()

    print("Запрос 1")
    print("Список всех связанных жестких дисков и компьютеров, отсортированный по жестким дискам:")
    arr1 = manager.query_1()
    for i in arr1:
        print(f"Жесткий диск: {i[0]}, объем: {i[1]}ГБ, компьютер: {i[2]}")

    print("\nЗапрос 2")
    print("Список компьютеров с количеством жестких дисков в каждом, отсортированный по количеству дисков:")
    arr2 = manager.query_2()
    for i in arr2:
        print(f"Компьютер: {i[0]}, количество жестких дисков: {i[1]}")

    print("\nЗапрос 3")
    print("Список всех жестких дисков, у которых модель заканчивается на 'TB', и названия их компьютеров:")
    arr3 = manager.query_3()
    for i in arr3:
        print(f"Жесткий диск: {i[0]}, объем: {i[1]}ГБ, компьютер: {i[2]}")


if __name__ == "__main__":
    main()