from unittest.mock import patch

import pytest

from main import output_to_user, user_choice_1  # Импорт напрямую из main.py в корне


class TestOutputToUser:
    """Тестирование функции output_to_user"""

    @pytest.fixture
    def sample_transactions(self):
        return [
            {
                "date": "2019-08-26T10:50:58.294041",
                "description": "Перевод организации",
                "from": "Maestro 1596837868705199",
                "to": "Счет 64686473678894779589",
                "operationAmount": {
                    "amount": "31957.58",
                    "currency": {
                        "code": "RUB"
                    }
                }
            }
        ]

    def test_output_empty_list(self, capsys):
        """Тест с пустым списком транзакций"""
        output_to_user([])
        captured = capsys.readouterr()
        assert "Не найдено ни одной транзакции" in captured.out

    def test_output_with_transactions(self, sample_transactions, capsys):
        """Тест с корректными данными транзакций"""
        output_to_user(sample_transactions)
        captured = capsys.readouterr().out

        assert "26.08.2019 Перевод организации" in captured
        assert "Maestro 1596 83** **** 5199 -> Счет **9589" in captured
        assert "31957.58 RUB" in captured


class TestUserChoice1:
    """Тестирование функции user_choice_1"""

    @patch('builtins.input', side_effect=['1'])
    @patch('main.load_transactions', return_value=[{'id': 1, 'amount': 100}])
    def test_choice_json(self, mock_load, mock_input, capsys):
        """Тест выбора JSON файла"""
        result = user_choice_1()
        assert result == [{'id': 1, 'amount': 100}]
        captured = capsys.readouterr()
        assert "Для обработки выбран JSON-файл" in captured.out

    @patch('builtins.input', side_effect=['2'])
    @patch('main.file_reader_csv', return_value=[{'id': 2, 'amount': 200}])
    def test_choice_csv(self, mock_csv, mock_input, capsys):
        """Тест выбора CSV файла"""
        result = user_choice_1()
        assert result == [{'id': 2, 'amount': 200}]
        captured = capsys.readouterr()
        assert "Для обработки выбран CSV-файл" in captured.out
