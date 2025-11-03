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

hard_drives = [
    HardDrive(1, "WD Blue 1TB", 1000, 1),
    HardDrive(2, "Seagate Barracuda 2TB", 2000, 2),
    HardDrive(3, "Samsung 870 EVO 500GB", 500, 2),
    HardDrive(4, "Toshiba P300 3TB", 3000, 3),
    HardDrive(5, "Kingston NV1 1TB", 1000, 4),
    HardDrive(6, "Crucial MX500 2TB", 2000, 5),
]

computers = [
    Computer(1, "ИБМ-001"),
    Computer(2, "MacBook-Pro"),
    Computer(3, "Asus-Gaming"),
    Computer(4, "Huawei"),
    Computer(5, "Lenovo-Ultra"),
]

computer_hard_drives = [
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


def main():
    # Связь один-ко-многим
    oneToMany = [[hd.model, hd.capacity, comp.name]
                for hd in hard_drives
                for comp in computers
                if hd.computer_id == comp.id]

    print("Запрос 1")
    print("Список всех связанных жестких дисков и компьютеров, отсортированный по жестким дискам:")
    arr1 = sorted(oneToMany, key=lambda x: x[0])
    for i in arr1:
        print(f"Жесткий диск: {i[0]}, объем: {i[1]}ГБ, компьютер: {i[2]}")


    print("\nЗапрос 2")
    print("Список компьютеров с количеством жестких дисков в каждом, отсортированный по количеству дисков:")

    arr2 = []
    for comp in computers:
        drives_in_comp = list(filter(lambda x: x[2] == comp.name, oneToMany))
        if len(drives_in_comp) > 0:
            arr2.append((comp.name, len(drives_in_comp)))

    arr2.sort(key=lambda x: x[1])
    for i in arr2:
        print(f"Компьютер: {i[0]}, количество жестких дисков: {i[1]}")


    print("\nЗапрос 3")
    print("Список всех жестких дисков, у которых модель заканчивается на 'TB', и названия их компьютеров:")

    manyToManyFirst = [[comp.name, comp_hd.computer_id, comp_hd.hard_drive_id]
                      for comp in computers
                      for comp_hd in computer_hard_drives
                      if comp.id == comp_hd.computer_id]

    manyToMany = [[hd.model, hd.capacity, comp_name]
                 for comp_name, comp_id, hd_id in manyToManyFirst
                 for hd in hard_drives
                 if hd.id == hd_id]

    arr3 = []
    for model, capacity, comp_name in manyToMany:
        if model.endswith("TB"):
            arr3.append([model, capacity, comp_name])

    arr3.sort(key=lambda x: x[0])
    for i in arr3:
        print(f"Жесткий диск: {i[0]}, объем: {i[1]}ГБ, компьютер: {i[2]}")


if __name__ == "__main__":
    main()