import pytest
from src.processing import filter_by_state, sort_by_date
from typing import Dict, List, Any


@pytest.mark.parametrize("state, expected_count", [
    ("EXECUTED", 3),
    ("PENDING", 2),
    ("CANCELED", 1),
    ("UNKNOWN", 0),
])
def test_filter_by_state(state: str, expected_count: int) -> None:
    """Тестирует фильтрацию транзакций по различным статусам."""
    transactions: List[Dict[str, Any]] = [
        {"id": 1, "state": "EXECUTED", "date": "2023-05-01"},
        {"id": 2, "state": "EXECUTED", "date": "2023-05-02"},
        {"id": 3, "state": "PENDING", "date": "2023-05-03"},
        {"id": 4, "state": "EXECUTED", "date": "2023-05-04"},
        {"id": 5, "state": "PENDING", "date": "2023-05-05"},
        {"id": 6, "state": "CANCELED", "date": "2023-05-06"},
    ]
    filtered = filter_by_state(transactions, state)
    assert len(filtered) == expected_count
    assert all(t["state"] == state for t in filtered)


def test_filter_by_state_empty_list() -> None:
    """Тестирует фильтрацию пустого списка транзакций."""
    assert filter_by_state([], "EXECUTED") == []


def test_filter_by_state_no_state_key() -> None:
    """Тестирует фильтрацию, когда у некоторых транзакций нет ключа 'state'."""
    transactions: List[Dict[str, Any]] = [
        {"id": 1, "state": "EXECUTED", "date": "2023-05-01"},
        {"id": 2, "date": "2023-05-02"},  # Нет ключа 'state'
        {"id": 3, "state": "PENDING", "date": "2023-05-03"},
    ]
    filtered = filter_by_state(transactions, "EXECUTED")
    assert len(filtered) == 1
    assert filtered[0]["id"] == 1


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми данными для сортировки."""
    return [
        {"id": 1, "date": "2023-05-01"},
        {"id": 2, "date": "2023-05-10"},
        {"id": 3, "date": "2023-05-05"},
        {"id": 4, "date": "2023-05-01"},  # Такая же дата, как у id=1
        {"id": 5, "date": "2023-01-15"},
    ]


def test_sort_by_date_descending(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тестирует сортировку по убыванию даты (новые сначала)."""
    sorted_transactions = sort_by_date(sample_transactions, reverse=True)
    dates = [t["date"] for t in sorted_transactions]
    assert dates == ["2023-05-10", "2023-05-05", "2023-05-01", "2023-05-01", "2023-01-15"]


def test_sort_by_date_ascending(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тестирует сортировку по возрастанию даты (старые сначала)."""
    sorted_transactions = sort_by_date(sample_transactions, reverse=False)
    dates = [t["date"] for t in sorted_transactions]
    assert dates == ["2023-01-15", "2023-05-01", "2023-05-01", "2023-05-05", "2023-05-10"]


def test_sort_by_date_same_dates(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тестирует сохранение порядка при одинаковых датах (должен сохраняться исходный порядок)."""
    # Добавим ещё одну транзакцию с такой же датой, как у id=1 и id=4
    sample_transactions.append({"id": 6, "date": "2023-05-01"})
    sorted_transactions = sort_by_date(sample_transactions, reverse=False)
    # Получаем все транзакции с датой "2023-05-01"
    may_first = [t for t in sorted_transactions if t["date"] == "2023-05-01"]
    # Проверяем, что их порядок соответствует исходному (id=1, id=4, id=6)
    assert [t["id"] for t in may_first] == [1, 4, 6]


@pytest.mark.parametrize("date_format", [
    "2023-05-01T12:30:45",  # ISO формат с временем
    "01/05/2023",           # Другой формат даты
    "May 1, 2023",          # Текстовый формат
])
def test_sort_by_date_different_formats(date_format: str) -> None:
    """Тестирует сортировку с различными форматами дат."""
    transactions: List[Dict[str, Any]] = [
        {"id": 1, "date": "2023-05-01"},
        {"id": 2, "date": date_format},
        {"id": 3, "date": "2023-01-01"},
    ]
    # Ожидаем, что функция сможет сравнить строки как есть
    sorted_transactions = sort_by_date(transactions, reverse=True)
    assert sorted_transactions[0]["id"] in (1, 2)  # Первой должна быть самая поздняя дата
