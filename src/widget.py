from src.masks import get_mask_card_number, get_mask_account

def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета в переданной строке, сохраняя тип (название карты или 'Счет')
    :param account_info: Строка с типом и номером (например, "Visa Platinum 7000792289606361" или "Счет 73654108430135874305")
    :return: Строка с маскированным номером
    """
    # Разделяем строку на части (тип и номер)
    parts = account_info.split()

    # Проверяем, что строка содержит как минимум тип и номер
    if len(parts) < 2:
        raise ValueError(
            "Некорректный формат входных данных. Ожидается строка типа 'Visa Platinum 7000792289606361' или 'Счет 73654108430135874305'")

    # Тип карты/счета - это все части кроме последней
    account_type = " ".join(parts[:-1])
    number = parts[-1]

    # Определяем тип (карта или счет) и применяем соответствующую маскировку
    if account_type.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{account_type} {masked_number}"

from datetime import datetime

def get_date(date_str: str) -> str:
    """
    Преобразует дату из формата 'YYYY-MM-DDTHH:MM:SS.mmmmmm' в 'DD.MM.YYYY'
    :param date_str: Строка с датой в формате ISO 8601
    :return: Строка с датой в формате ДД.ММ.ГГГГ
    """
    try:
        # Парсим исходную дату
        date_obj = datetime.fromisoformat(date_str)
        # Форматируем в нужный формат
        return date_obj.strftime("%d.%m.%Y")
    except ValueError as e:
        raise ValueError(f"Некорректный формат даты: {date_str}") from e


# Код для проверки вида
if __name__ == "__main__":
    user_card_or_account_number = input()
    # вводим номер карты или счета клиента
    print(mask_account_card(user_card_or_account_number))
    # вывод замаскированного номера карты или аккаунта
