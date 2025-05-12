def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты в формате XXXX XX** **** XXXX
    :param card_number: Номер карты (может содержать пробелы и другие разделители)
    :return: Маскированный номер карты
    """
    # Удаляем все нецифровые символы
    digits = ''.join(c for c in str(card_number) if c.isdigit())

    # Проверяем длину номера карты
    if len(digits) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Форматируем номер карты с маскировкой
    return f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета в формате **XXXX
    :param account_number: Номер счета (может содержать пробелы и другие разделители)
    :return: Маскированный номер счета
    """
    # Удаляем все нецифровые символы
    digits = ''.join(c for c in str(account_number) if c.isdigit())

    # Проверяем минимальную длину номера счета
    if len(digits) < 4:
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    # Возвращаем маскированный номер
    return f"**{digits[-4:]}"


# Код для проверки вида
if __name__ == '__main__':
    account_number = str(input())
    print(get_mask_account(account_number))
