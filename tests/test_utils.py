from unittest.mock import patch

import pytest

from src.utils import load_transactions


@pytest.fixture
def temp_transactions_file(tmp_path):
    # Создаем временный файл для тестов
    test_file = tmp_path / "test_operations.json"
    test_file.write_text("""[{"id": 1, "state": "EXECUTED", "operationAmount": {"amount": "100", "currency": {"code": "USD"}}}]""", encoding="utf-8")
    return test_file


def test_load_transactions(temp_transactions_file):
    # Проверка загрузки файла
    transactions = load_transactions(temp_transactions_file)
    assert len(transactions) == 1
    assert transactions[0]["id"] == 1


def test_convert_to_rub():
    # Мокируем API
    with patch('src.external_api.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"rates": {"RUB": 75.0}}

        from src.external_api import convert_to_rub
        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        }
        assert convert_to_rub(transaction) == 7500.0
