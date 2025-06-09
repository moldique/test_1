import csv

import pandas as pd


def file_reader_csv(csv_path: str) -> list[dict]:
    """
    Читает CSV файл и возвращает список словарей с данными.

    Каждая строка CSV файла преобразуется в словарь, где ключи берутся из заголовков столбцов.
    """
    data = []
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')  # Автоматически использует первую строку как ключи
        for row in reader:
            data.append(row)  # Каждая строка становится словарём
        return data


def file_reader_excel(excel_path: str) -> list[dict]:
    """
    Читает Excel файл и возвращает список словарей с данными.

    Каждая строка Excel файла преобразуется в словарь, где ключи соответствуют названиям столбцов.
    """
    try:
        df = pd.read_excel(excel_path)
        return df.to_dict('records')
    except FileNotFoundError:
        print(f"Ошибка: файл не найден по пути {excel_path}")
        return []
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return []


if __name__ == "__main__":
    print(file_reader_csv('..//data/transactions.csv'))
    print(file_reader_excel('..//data/transactions_excel.xlsx'))
