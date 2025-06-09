import pytest

from src.filters import filter_operations_by_category, filter_operations_by_description


@pytest.fixture
def sample_operations():
    return [
        {"description": "Перевод организации", "amount": 100},
        {"description": "Перевод с карты на карту", "amount": 2000},
        {"description": "Перевод с карты на карту", "amount": 50},
        {"description": "Открытие вклада", "amount": 75},
        {"description": "Перевод со счета на счет", "amount": 10},
        {"description": "Перевод с карты на карту", "amount": 15},
        {"description": "", "amount": 20},  # Пустое описание
    ]


def test_filter_operations_by_description_basic(sample_operations):
    # Тест на поиск по точному совпадению
    result = filter_operations_by_description(sample_operations, "Перевод организации")
    assert len(result) == 1
    assert result[0]["amount"] == 100


def test_filter_operations_by_description_partial_match(sample_operations):
    # Тест на поиск по части строки
    result = filter_operations_by_description(sample_operations, "карты")
    assert len(result) == 3
    assert all("карты" in op["description"].lower() for op in result)


def test_filter_operations_by_description_case_insensitive(sample_operations):
    # Тест на регистронезависимость
    result = filter_operations_by_description(sample_operations, "ПЕРЕВОД")
    assert len(result) == 5  # Все кроме "Открытие вклада" и пустого описания


def test_filter_operations_by_description_empty_search(sample_operations):
    # Тест на пустую строку поиска (должен вернуть копию всех операций)
    result = filter_operations_by_description(sample_operations, "")
    assert len(result) == len(sample_operations)


def test_filter_operations_by_category_basic(sample_operations):
    # Тест на подсчет операций по категориям
    categories = ["Перевод", "Открытие"]
    result = filter_operations_by_category(sample_operations, categories)
    assert result == {"Перевод": 5, "Открытие": 1}


def test_filter_operations_by_category_no_matches(sample_operations):
    # Тест на случай, когда категории не найдены
    result = filter_operations_by_category(sample_operations, ["Покупка"])
    assert result == {}
