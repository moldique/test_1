import re
from collections import Counter

from src.file_reader import file_reader_csv


def filter_operations_by_description(operations: list[dict], search_string: str) -> list[dict]:
    """
    Фильтрует список операций, оставляя только те, в описании которых встречается заданная строка.

    :param operations: Список словарей с данными о банковских операциях.
    :param search_string: Строка для поиска в описании операций.
    :return: Отфильтрованный список операций.
    """
    if not search_string:
        return operations.copy()

    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    filtered_operations = [
        op for op in operations
        if op.get('description') and pattern.search(op['description'])
    ]
    return filtered_operations


def filter_operations_by_category(operations, categories):
    """
    Подсчитывает количество операций по заданным категориям с использованием Counter.

    :param operations: Список словарей с операциями (должен содержать поле 'description').
    :param categories: Список строк (категорий) для поиска в описании операций.
    :return: Словарь {категория: количество_операций}.
    """
    category_counter = Counter()

    for operation in operations:
        description = operation.get('description', '').lower()

        # Находим все категории, которые присутствуют в описании операции
        matched_categories = [
            category for category in categories
            if re.search(rf'\b{re.escape(category.lower())}\b', description)
        ]

        # Если найдена хотя бы одна категория, учитываем первую совпавшую
        if matched_categories:
            category_counter[matched_categories[0]] += 1

    return dict(category_counter)


if __name__ == "__main__":

    list_1 = file_reader_csv('..//data/transactions.csv')
    print(filter_operations_by_description(list_1, 'Открытие'))
    print(filter_operations_by_category(list_1, ['перевод', 'открытие']))
