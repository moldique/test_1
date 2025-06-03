import csv

import pandas as pd


def file_reader_csv(csv_path):
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


def file_reader_exel(exel_path):
    """
    Читает Excel файл и возвращает список словарей с данными.

    Каждая строка Excel файла преобразуется в словарь, где ключи соответствуют названиям столбцов.
    """
    df = pd.read_excel(exel_path)
    data = df.to_dict('records')
    return data
