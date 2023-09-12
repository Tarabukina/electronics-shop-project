"""Здесь надо написать тесты с использованием pytest для модуля item."""
import csv
import pytest
from pathlib import Path

from src.item import Item

test_params_1 = {
    "name": "test_1",
    "price": 0.1,
    "quantity": 0,
}

test_params_2 = {
    "name": "test_2",
    "price": 10,
    "quantity": -2,
}

test_params_3 = {
    "name": "test_3",
    "price": 10 / 3,
    "quantity": 1,
}


@pytest.fixture
def get_instances() -> tuple[Item, Item, Item]:
    return (
        Item(**test_params_1),
        Item(**test_params_2),
        Item(**test_params_3),
    )


@pytest.fixture
def create_test_csv(tmp_path) -> Path:
    path = tmp_path / "test_csv.csv"

    with open(path, "w", encoding="windows-1251") as csvfile:
        field_names = ["name", "price", "quantity"]
        data_test = [
            test_params_1,
            test_params_2,
            test_params_3,
        ]

        writer = csv.DictWriter(csvfile, fieldnames=field_names)

        writer.writeheader()
        writer.writerows(data_test)

    return path


class TestItem:
    example_instance = Item("Камера", 24_000.5, 20)
    assert example_instance.name == "Камера"

    example_instance.name = "hdsfhdshfhds"
    assert example_instance.name == "Камера"

    assert str(example_instance) == "Камера"
    assert repr(example_instance) == "Item('Камера', 24000.5, 20)"

    example_instance.name = "Фотик"
    assert example_instance.name == "Фотик"

    Item.all = []

    def test_calculate_total_price(self, get_instances):
        items = get_instances

        assert items[0].all is items[1].all is items[2].all
        assert len(type(items[0]).all) == 3

        assert items[0].calculate_total_price() == 0
        assert items[1].calculate_total_price() == -20
        assert items[2].calculate_total_price() == 10 / 3

        [item.apply_discount() for item in items]

        assert items[0].calculate_total_price() == 0
        assert items[1].calculate_total_price() == -20
        assert items[2].calculate_total_price() == 10 / 3

    def test_instantiate_from_csv(self, create_test_csv):
        Item.all = []
        Item.instantiate_from_csv(create_test_csv)

        assert len(Item.all) == 3
        assert all(
            [
                item.__class__ is Item
                for item in Item.all
            ]
        )

    def test_string_to_number(self):
        with pytest.raises(TypeError):
            Item.string_to_number(10)

        assert Item.string_to_number("123..2") == 123
        assert Item.string_to_number("") is None