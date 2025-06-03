import json
import logging

from src.external_api import convert_to_rub

logger = logging.getLogger('save_to_logs_units')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('../logs/save_to_logs_units.log', encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_transactions(file_path) -> list:
    """
    Принимает на вход путь до JSON-файла и возвращает список словарей
    с данными о финансовых транзакциях. Если файл пустой, содержит не список или не найден,
     функция возвращает пустой список
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            transactions = json.load(f)
            logger.info(f'открытие файла: {file_path}')
        if isinstance(transactions, list):
            return transactions
        return []
    except Exception as ex:
        logger.error(f'Файл не найден или произошла ошибка: {ex}, создан пустой список')
        return []


def amount_transaction():
    """
     Функция, которая принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях
    """
    try:
        logger.info('Получение транзакций')
        # Загрузка транзакций
        transactions = load_transactions('../data/operations.json')
        print(f"Загружено транзакций: {len(transactions)}")

        if not transactions:
            print("Нет данных для обработки.")
            return

        logger.info('Обработка каждой транзакции и суммирование суммы')
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
                logger.error(f'Произошла ошибка обработки транзакций: {e}')

        # Итог
        print(f"\nОбщая сумма выполненных транзакций: {total_rub:.2f} RUB")
        logger.info(f'Вывод итоговой суммы пользователю: {total_rub:.2f}')

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        logger.error(f'Произошла ошибка: {e}')


if __name__ == "__main__":
    amount_transaction()
