import os
from decimal import Decimal

import requests
from dotenv import load_dotenv

load_dotenv()


def convert_to_rub(transaction) -> float:
    """
      Конвертирует сумму транзакции в рубли.
      Если валюта не RUB, использует внешний API для получения курса.
    """
    try:
        operation_amount = transaction.get("operationAmount", {})
        amount = Decimal(str(operation_amount.get("amount", 0)))
        currency = operation_amount.get("currency", {})
        currency_code = currency.get("code", "RUB").upper()

        if currency_code == "RUB":
            return float(amount)

        api_key = os.getenv('API_KEY')
        if not api_key:
            raise ValueError("API key not found")

        url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency_code}&symbols=RUB"
        response = requests.get(url, headers={"apikey": api_key}, timeout=10)
        response.raise_for_status()

        rate = Decimal(str(response.json()['rates']['RUB']))
        return float(amount * rate)

    except Exception as e:
        print(f"Ошибка конвертации: {e}")
        return 0.0
