import json

import requests

from src.external_api import convert_to_rub


def load_transactions(file_path) -> list:
    """
    Принимает на вход путь до JSON-файла и возвращает список словарей
    с данными о финансовых транзакциях. Если файл пустой, содержит не список или не найден,
     функция возвращает пустой список
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            transactions = json.load(f)
        if isinstance(transactions, list):
            return transactions
        return []
    except(json.JSONDecodeError, OSError):
        return []


def amount_transaction():
    """
     Функция, которая принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях
    """
    try:
        # Загрузка транзакций
        transactions = load_transactions('../data/operations.json')
        print(f"Загружено транзакций: {len(transactions)}")

        if not transactions:
            print("Нет данных для обработки.")
            return

        # Обработка каждой транзакции
        total_rub = 0.0
        print("\nДетали транзакций:")
        for idx, transaction in enumerate(transactions, 1):
            try:
                if transaction.get("state") != "EXECUTED":
                    print(f"{idx}. Пропущено: транзакция не выполнена (state: {transaction.get('state')})")
                    continue

                amount_rub = convert_to_rub(transaction)
                total_rub += amount_rub

                operation_amount = transaction["operationAmount"]
                currency_name = operation_amount["currency"]["name"]
                currency_code = operation_amount["currency"]["code"]

                print(
                    f"{idx}. {transaction['date']} | "
                    f"{transaction['description']} | "
                    f"Сумма: {operation_amount['amount']} {currency_name} ({currency_code}) → {amount_rub:.2f} RUB | "
                    f"Откуда: {transaction.get('from', 'N/A')} | "
                    f"Куда: {transaction.get('to', 'N/A')}"
                )
            except (KeyError, ValueError) as e:
                print(f"{idx}. Ошибка обработки транзакции: {e}")

        # Итог
        print(f"\nОбщая сумма выполненных транзакций: {total_rub:.2f} RUB")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    amount_transaction()
