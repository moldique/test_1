import pytest
from src.masks import get_mask_card_number, get_mask_account
from typing import Dict


@pytest.fixture
def card_numbers() -> Dict[str, str]:
    return {
        "standard": "7000792289606361",
        "with_spaces": "7000 7922 8960 6361",
        "with_dashes": "7000-7922-8960-6361",
        "short": "123456789012",
        "empty": ""
    }


# Тесты для маскирования номера карты
def test_mask_card_standard(card_numbers: Dict[str, str]) -> None:
    assert get_mask_card_number(card_numbers["standard"]) == "7000 79** **** 6361"


def test_mask_card_with_spaces(card_numbers: Dict[str, str]) -> None:
    assert get_mask_card_number(card_numbers["with_spaces"]) == "7000 79** **** 6361"


def test_mask_card_with_dashes(card_numbers: Dict[str, str]) -> None:
    assert get_mask_card_number(card_numbers["with_dashes"]) == "7000 79** **** 6361"


def test_mask_card_invalid_length(card_numbers: Dict[str, str]) -> None:
    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
        get_mask_card_number(card_numbers["short"])


def test_mask_card_empty_input(card_numbers: Dict[str, str]) -> None:
    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
        get_mask_card_number(card_numbers["empty"])


@pytest.fixture
def account_numbers() -> Dict[str, str]:
    return {
        "standard": "73654108430135874305",
        "with_spaces": "7365 4108 4301 3587 4305",
        "short": "123",
        "empty": ""
    }


# Тесты для маскирования номера счета
def test_mask_account_standard(account_numbers: Dict[str, str]) -> None:
    assert get_mask_account(account_numbers["standard"]) == "**4305"


def test_mask_account_with_spaces(account_numbers: Dict[str, str]) -> None:
    assert get_mask_account(account_numbers["with_spaces"]) == "**4305"


def test_mask_account_short(account_numbers: Dict[str, str]) -> None:
    with pytest.raises(ValueError, match="Номер счета должен содержать минимум 4 цифры"):
        get_mask_account(account_numbers["short"])


def test_mask_account_empty_input(account_numbers: Dict[str, str]) -> None:
    with pytest.raises(ValueError, match="Номер счета должен содержать минимум 4 цифры"):
        get_mask_account(account_numbers["empty"])
