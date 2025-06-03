from unittest.mock import MagicMock, mock_open, patch

import pytest

from src.file_reader import file_reader_csv, file_reader_exel

# Фиктивные данные для тестов
EXCEL_MOCK_DATA = [{
    'id': 650703.0,
    'state': 'EXECUTED',
    'date': '2023-09-05T11:30:32Z',
    'amount': 16210.0,
    'currency_name': 'Sol',
    'currency_code': 'PEN',
    'from': 'Счет 58803664561298323391',
    'to': 'Счет 39745660563456619397',
    'description': 'Перевод организации'
}]

CSV_MOCK_DATA = """id;state;date;amount;currency_name;currency_code;from;to;description
650703.0;EXECUTED;2023-09-05T11:30:32Z;16210.0;Sol;PEN;Счет 58803664561298323391;Счет 39745660563456619397;Перевод организации
"""


def test_file_reader_csv():
    """Тест чтения CSV файла с правильной структурой"""
    with patch('builtins.open', mock_open(read_data=CSV_MOCK_DATA)):
        with patch('csv.DictReader') as mock_reader:
            mock_reader.return_value = [{
                'id': '650703.0',
                'state': 'EXECUTED',
                'date': '2023-09-05T11:30:32Z',
                'amount': '16210.0',
                'currency_name': 'Sol',
                'currency_code': 'PEN',
                'from': 'Счет 58803664561298323391',
                'to': 'Счет 39745660563456619397',
                'description': 'Перевод организации'
            }]

            result = file_reader_csv('dummy_path.csv')

            assert len(result) == 1
            assert result[0]['id'] == '650703.0'
            assert result[0]['state'] == 'EXECUTED'
            assert result[0]['description'] == 'Перевод организации'


def test_file_reader_excel():
    """Тест чтения Excel файла с правильной структурой"""
    with patch('pandas.read_excel') as mock_read_excel:
        # Создаем mock DataFrame с нужной структурой
        mock_df = MagicMock()
        mock_df.to_dict.return_value = EXCEL_MOCK_DATA

        mock_read_excel.return_value = mock_df

        result = file_reader_exel('dummy_path.xlsx')

        assert len(result) == 1
        assert result[0]['id'] == 650703.0
        assert result[0]['state'] == 'EXECUTED'
        assert result[0]['description'] == 'Перевод организации'
        mock_read_excel.assert_called_once_with('dummy_path.xlsx')


def test_file_reader_csv_empty():
    """Тест чтения пустого CSV файла"""
    with patch('builtins.open', mock_open(read_data="id;state;date\n")):
        with patch('csv.DictReader') as mock_reader:
            mock_reader.return_value = []

            result = file_reader_csv('empty.csv')

            assert result == []


def test_file_reader_csv_invalid():
    """Тест обработки CSV файла с некорректными данными"""
    with patch('builtins.open', mock_open(read_data="invalid;data\n1;2")):
        with patch('csv.DictReader') as mock_reader:
            mock_reader.return_value = [{'invalid': '1', 'data': '2'}]

            result = file_reader_csv('invalid.csv')

            assert len(result) == 1
            assert 'id' not in result[0]
            assert 'invalid' in result[0]
