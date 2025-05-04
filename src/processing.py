def filter_by_state(transactions: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    :param transactions: Список словарей для фильтрации.
    :param state: Значение ключа 'state' для фильтрации. По умолчанию 'EXECUTED'.
    :return: Новый список словарей, где 'state' соответствует указанному значению.
    """
    return [transaction for transaction in transactions if transaction.get('state') == state]


def sort_by_date(transactions: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортирует список транзакций по дате.

    Args:
        transactions: Список словарей с транзакциями
        reverse: Порядок сортировки (True - по убыванию, False - по возрастанию)
                По умолчанию True (новые операции сначала)

    Returns:
        Отсортированный список транзакций
    """
    return sorted(transactions, key=lambda x: x['date'], reverse=reverse)
