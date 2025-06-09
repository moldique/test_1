from typing import Dict, List

from src.file_reader import file_reader_csv, file_reader_excel
from src.filters import filter_operations_by_description
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.utils import load_transactions
from src.widget import get_date, mask_account_card


def user_choice_1() -> List[Dict]:
    """Запрашивает у пользователя выбор файла для загрузки транзакций и возвращает данные.

    Предлагает пользователю выбрать между JSON, CSV и XLSX файлами. В зависимости от выбора
    загружает данные из соответствующего файла.

    Returns:
        List[Dict]: Список словарей с транзакциями, загруженными из выбранного файла.

    Notes:
        Файлы должны находиться в папке data/ с именами:
        - operations.json для JSON
        - transactions.csv для CSV
        - transactions_excel.xlsx для XLSX
    """
    valid_answers = {'1', '2', '3'}

    while True:
        answer = input("""Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла
""")

        if answer in valid_answers:
            match answer:
                case "1":
                    print('Для обработки выбран JSON-файл')
                    return load_transactions('data/operations.json')
                case "2":
                    print('Для обработки выбран CSV-файл')
                    return file_reader_csv('data/transactions.csv')
                case "3":
                    print('Для обработки выбран XLSX-файл')
                    return file_reader_excel('data/transactions_excel.xlsx')
        else:
            print(f'\nФайл №{answer} недоступен, выберите из предложенных (1, 2 или 3)\n')


def user_choice_2(transactions: List[Dict]) -> List[Dict]:
    """Фильтрует транзакции по статусу, указанному пользователем.

    Args:
        transactions: Список словарей с транзакциями для фильтрации.

    Returns:
        List[Dict]: Список отфильтрованных транзакций по выбранному статусу.

    Notes:
        Доступные статусы: EXECUTED, CANCELED, PENDING
    """
    valid_answers = {'EXECUTED', 'CANCELED', 'PENDING'}

    while True:
        user_input = input("Введите статус, по которому необходимо выполнить фильтрацию.\n"
                           "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n").upper()

        if user_input in valid_answers:
            print(f"Программа: Операции отфильтрованы по статусу \"{user_input}\"")
            return filter_by_state(transactions, user_input)
        else:
            print(f"Программа: Статус операции \"{user_input}\" недоступен.")


def another_questions(filtered_transactions: List[Dict]) -> List[Dict]:
    """Применяет дополнительные фильтры и сортировки к транзакциям на основе пользовательского ввода.

    Args:
        filtered_transactions: Список уже отфильтрованных транзакций.

    Returns:
        List[Dict]: Список транзакций после применения всех дополнительных фильтров и сортировок.

    Notes:
        Запрашивает у пользователя:
        1. Нужно ли сортировать по дате (и порядок сортировки)
        2. Нужно ли фильтровать только рублевые транзакции
        3. Нужно ли фильтровать по ключевому слову в описании
    """
    # Вопрос 1: Сортировка по дате
    while True:
        user_input_1 = input('Отсортировать операции по дате? Да/Нет\n').lower()
        if user_input_1 in ['да', 'нет']:
            break
        print('Пожалуйста, введите только "Да" или "Нет"')

    if user_input_1 == 'да':
        while True:
            user_input_2 = input('Отсортировать по возрастанию или по убыванию?(по возрастанию/по убыванию)\n').lower()
            if user_input_2 in ['по возрастанию', 'по убыванию']:
                break
            print('Пожалуйста, введите только "по возрастанию" или "по убыванию"')

        sort_1 = sort_by_date(filtered_transactions, reverse=(user_input_2 == 'по убыванию'))
    else:
        sort_1 = filtered_transactions

    # Вопрос 2: Только рублевые транзакции
    while True:
        user_input_3 = input('Выводить только рублевые транзакции? Да/Нет\n').lower()
        if user_input_3 in ['да', 'нет']:
            break
        print('Пожалуйста, введите только "Да" или "Нет"')

    if user_input_3 == 'да':
        sort_2 = filter_by_currency(sort_1, 'RUB')
    else:
        sort_2 = sort_1

    # Вопрос 3: Фильтрация по ключевому слову
    while True:
        user_input_4 = input('Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n').lower()
        if user_input_4 in ['да', 'нет']:
            break
        print('Пожалуйста, введите только "Да" или "Нет"')

    if user_input_4 == 'да':
        user_input_5 = input('Введите слово для фильтрации:\n')
        sort_3 = filter_operations_by_description(sort_2, user_input_5)
        print('Распечатываю итоговый список транзакций...')
        return sort_3
    else:
        print('Распечатываю итоговый список транзакций...\n')
        return sort_2


def output_to_user(final_list: List[Dict]) -> None:
    """Выводит отформатированный список транзакций пользователю.

    Args:
        final_list: Финальный список транзакций после всех фильтров и сортировок.

    Notes:
        Для каждой транзакции выводит:
        - Дату в формате ДД.ММ.ГГГГ
        - Описание операции
        - Откуда и куда (с маскировкой номеров карт/счетов)
        - Сумму и валюту операции
    """
    if len(final_list) == 0:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f'Всего банковских операций в выборке: {len(final_list)}\n')
        for i in final_list:
            print(get_date(i["date"]), i["description"])

            from_value = i.get("from", "")
            to_value = i.get("to", "")

            # Проверяем, что from_value и to_value - строки (не None и не float)
            has_from = isinstance(from_value, str) and from_value.strip() != ""
            has_to = isinstance(to_value, str) and to_value.strip() != ""

            if has_from and has_to:
                print(f"{mask_account_card(from_value)} -> {mask_account_card(to_value)}")
            elif has_from:
                print(mask_account_card(from_value))
            else:
                print(mask_account_card(to_value))

            if "currency_code" in i:
                print(f'Сумма: {i["amount"]} {i["currency_code"]}\n')
            else:
                print(f'Сумма: {i["operationAmount"]["amount"]} {i["operationAmount"]["currency"]["code"]}\n')


def main():
    """Основная функция программы, координирующая весь процесс работы с транзакциями.

    Выполняет последовательно:
    1. Загрузку транзакций из файла (через user_choice_1)
    2. Фильтрацию по статусу (через user_choice_2)
    3. Применение дополнительных фильтров и сортировок (через another_questions)
    4. Вывод результатов пользователю (через output_to_user)
    """
    # Получаем транзакции из файла
    transactions = user_choice_1()

    # Фильтруем по статусу
    filtered_transactions = user_choice_2(transactions)

    # Применяем дополнительные фильтры и сортировки
    final_transactions = another_questions(filtered_transactions)

    # Выводим результат пользователю
    output_to_user(final_transactions)


if __name__ == "__main__":
    main()
