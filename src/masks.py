import logging


logger = logging.getLogger('save_to_log_masks')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('../logs/save_to_log_masks.log', encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты в формате XXXX XX** **** XXXX
    :param card_number: Номер карты (может содержать пробелы и другие разделители)
    :return: Маскированный номер карты
    """
    try:
        # Удаляем все нецифровые символы
        digits = ''.join(c for c in str(card_number) if c.isdigit())
        logger.info('Удаление всех нецифровых символов и получение номера карты')

        # Проверяем длину номера карты
        if len(digits) != 16:
            raise ValueError("Номер карты должен содержать 16 цифр")

        # Форматируем номер карты с маскировкой
        logger.info('форматирование и маскировка номера карты')
        return f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"
    except Exception as ex:
        logger.error(f'Произошла ошибка: {ex}')


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета в формате **XXXX
    :param account_number: Номер счета (может содержать пробелы и другие разделители)
    :return: Маскированный номер счета
    """
    try:
        # Удаляем все нецифровые символы
        digits = ''.join(c for c in str(account_number) if c.isdigit())
        logger.info('Удаление всех нецифровых символов и получение номера счета')

        # Проверяем минимальную длину номера счета
        if len(digits) < 4:
            raise ValueError("Номер счета должен содержать минимум 4 цифры")

        logger.info('форматирование и маскировка номера счета')
        # Возвращаем маскированный номер
        return f"**{digits[-4:]}"
    except Exception as ex:
        logger.error(f'Произошла ошибка: {ex}')


# Код для проверки вида
if __name__ == '__main__':
    account_number = str(input())
    print(get_mask_account(account_number))
