import re

from typing import Optional, Self
from pathlib import Path
from csv import DictReader


class Item:
    """
    Класс для представления товара в магазине.
    """
    pay_rate = 1.0
    csv_source = Path(__file__).resolve().parent / "items.csv"
    all = []

    def __new__(cls, *args, **kwargs) -> Self:
        """"Добавление экземпляра в список экземпляров all: list[Item]"""
        instance = super().__new__(cls)
        cls.all.append(instance)
        return instance

    def __init__(self, name: str, price: float, quantity: int) -> None:
        """
        Создание экземпляра класса item.

        :param name: Название товара.
        :param price: Цена за единицу товара.
        :param quantity: Количество товара в магазине.
        """
        self.__name = name
        self.price = price
        self.quantity = quantity

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        # Для ТЗ.
        # self.__name = value[:10]

        # Для main.py.
        if len(value) <= 10:
            self.__name = value

    @classmethod
    def instantiate_from_csv(cls,
                             data_path: Optional[str | Path] = None) -> None:
        """
        Создает экземпляры класса, выгруженные из csv-файла.
        Экземпляры добавляются в all - атрибут класса, содержащий
        список созданных экземпляров. Если указанный путь не существует,
        то экземпляры не создаются без возбуждения исключения.

        :param data_path: Путь до csv-файла, если не указан
                          используется путь csv_source по умолчанию.
        """
        path = data_path if data_path else cls.csv_source

        cls.all = []

        if Path(path).resolve().exists():
            with open(path, encoding="windows-1251") as csv_file:
                reader = DictReader(csv_file)

                for data in reader:
                    if data:
                        cls(**data)

    @staticmethod
    def string_to_number(string: str) -> int | None:
        """
        Извлекает целые числа из строки.

        :param string: Строка, в которой необходимо
            найти числа.

        :return: Число типа integer, если числа присутствуют
            в string, иначе None.
        """
        if match_ := re.search(
            r"(?P<number>[+-]?\d+(?=[.]?))",
            string,
        ):
            return int(match_.group("number"))

    def calculate_total_price(self) -> float:
        """
        Рассчитывает общую стоимость конкретного товара в магазине.

        :return: Общая стоимость товара.
        """
        return self.price * self.quantity

    def apply_discount(self) -> None:
        """
        Применяет установленную скидку для конкретного товара.
        """
        self.price *= self.pay_rate

    def __repr__(self):
        return (f"{self.__class__.__name__}"
                f"{tuple((value for value in self.__dict__.values()))}")

    def __str__(self):
        return f"{self.name}"