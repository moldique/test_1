import pytest
from src.widget import (mask_account_card, get_date)


# Тесты для функции mask_account_card
@pytest.mark.parametrize(
    "input_str, expected_output",
    [
        # Тесты для карт
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
        # Тесты для счетов
        ("Счет 73654108430135874305", "Счет **4305"),
        ("счет 73654108430135874305", "счет **4305"),  # Проверка case-insensitive
    ],
)
def test_mask_account_card_valid(input_str: str, expected_output: str) -> None:
    """Проверяем корректность маскировки для разных типов карт и счетов."""
    assert mask_account_card(input_str) == expected_output


@pytest.mark.parametrize(
    "invalid_input",
    [
        "",  # Пустая строка
        "VisaPlatinum",  # Только тип
        "7000792289606361",  # Только номер
        "Счет",  # Только тип счета
    ],
)
def test_mask_account_card_invalid(invalid_input: str) -> None:
    """Проверяем, что функция корректно обрабатывает некорректные входные данные."""
    with pytest.raises(ValueError):
        mask_account_card(invalid_input)


# Тесты для функции get_date
@pytest.mark.parametrize(
    "input_date, expected_output",
    [
        ("2023-04-12T10:30:00.000000", "12.04.2023"),
        ("1999-12-31T23:59:59.999999", "31.12.1999"),
        ("2000-01-01T00:00:00.000000", "01.01.2000"),
    ],
)
def test_get_date_valid(input_date: str, expected_output: str) -> None:
    """Проверяем корректность преобразования даты."""
    assert get_date(input_date) == expected_output


@pytest.mark.parametrize(
    "invalid_date",
    [
        "",  # Пустая строка
        "12.04.2023",  # Уже в неправильном формате
        "not-a-date",  # Совсем не дата
        "2023-04-12T",  # Дата с T но без времени
    ],
)
def test_get_date_invalid(invalid_date: str) -> None:
    """Проверяем обработку некорректных форматов даты."""
    with pytest.raises(ValueError):
        get_date(invalid_date)


# Дополнительные тесты для проверки устойчивости
def test_mask_account_card_case_insensitive() -> None:
    """Проверяем, что функция корректно обрабатывает разные регистры для слова 'счет'."""
    assert mask_account_card("сЧеТ 73654108430135874305") == "сЧеТ **4305"


def test_get_date_with_timezone() -> None:
    """Проверяем, что функция корректно обрабатывает дату с часовым поясом."""
    assert get_date("2023-04-12T10:30:00.000000+03:00") == "12.04.2023"
