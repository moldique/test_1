from typing import Any, Dict, Iterator


def filter_by_currency(transactions: list[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Генератор, который фильтрует транзакции по заданной валюте.
    """
    for transaction in transactions:
        operation_amount = transaction.get("operationAmount", {})
        transaction_currency = operation_amount.get("currency", {}).get("code")
        if transaction_currency == currency:
            yield transaction


def transaction_descriptions(transactions: list[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, который возвращает описание каждой транзакции.
    """
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в заданном диапазоне.
    """
    if start > end:
        raise ValueError("Start must be less than or equal to end")

    for number in range(start, end + 1):
        yield f"{number:016d}"[:4] + " " + f"{number:016d}"[4:8] + " " + f"{number:016d}"[
                                                                         8:12] + " " + f"{number:016d}"[12:16]
