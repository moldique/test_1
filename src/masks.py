import logging
import os

# Создаем директорию для логов, если её нет
os.makedirs('../logs', exist_ok=True)

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
    :raises ValueError: Если номер карты невалидный
    """
    try:
        # Удаляем все нецифровые символы
        digits = ''.join(c for c in str(card_number) if c.isdigit())
        logger.info('Удаление всех нецифровых символов и получение номера карты')

        # Проверяем длину номера карты
        if len(digits) != 16:
            raise ValueError("Номер карты должен содержать 16 цифр")

        # Форматируем номер карты с маскировкой
        masked = f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"
        logger.info('Форматирование и маскировка номера карты')
        return masked
    except Exception as ex:
        logger.error(f'Произошла ошибка: {ex}')
        raise  # Пробрасываем исключение дальше


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета в формате **XXXX
    :param account_number: Номер счета (может содержать пробелы и другие разделители)
    :return: Маскированный номер счета
    :raises ValueError: Если номер счета невалидный
    """
    try:
        # Удаляем все нецифровые символы
        digits = ''.join(c for c in str(account_number) if c.isdigit())
        logger.info('Удаление всех нецифровых символов и получение номера счета')

        # Проверяем минимальную длину номера счета
        if len(digits) < 4:
            raise ValueError("Номер счета должен содержать минимум 4 цифры")

        # Возвращаем маскированный номер
        masked = f"**{digits[-4:]}"
        logger.info('Форматирование и маскировка номера счета')
        return masked
    except Exception as ex:
        logger.error(f'Произошла ошибка: {ex}')
        raise  # Пробрасываем исключение дальше


if __name__ == '__main__':
    account_number = str(input())
    print(get_mask_account(account_number))
