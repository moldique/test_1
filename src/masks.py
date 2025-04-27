def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты в формате XXXX XX** **** XXXX
    :param card_number: Номер карты (строка или число)
    :return: Маскированный номер карты
    """
    str_number = str(card_number).strip()
    if len(str_number) != 16 or not str_number.isdigit():
        raise ValueError("Номер карты должен состоять из 16 цифр")

    masked = (
        f"{str_number[:4]} {str_number[4:6]}** **** {str_number[-4:]}"
    )
    return masked


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета в формате **XXXX
    :param account_number: Номер счета (строка или число)
    :return: Маскированный номер счета
    """
    str_number = str(account_number).strip()
    if len(str_number) < 4 or not str_number.isdigit():
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    return f"**{str_number[-4:]}"

