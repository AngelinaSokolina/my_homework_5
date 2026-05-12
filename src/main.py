import re
from pathlib import Path
from typing import Any, Dict, List

from financial_transactions.developer import load_data  # для CSV
from src.bank_search import excel_data  # для Excel

# Импортируем функции из предыдущих модулей
from src.utils import reception_json  # для JSON


def load_transactions(file_type: int) -> list[dict] | None:
    """Загружает транзакции в зависимости от выбора пользователя:
    1 - JSON, 2 - CSV, 3 - XLSX"""

    base_path = Path(__file__).parent.parent

    if file_type == 1:
        print("Для обработки выбран JSON-файл.")
        file_path = base_path / 'data' / 'operations.json'
        return reception_json(file_path)

    elif file_type == 2:
        print("Для обработки выбран CSV-файл.")
        file_path = base_path / 'financial_transactions' / 'transactions.csv'
        return load_data(file_path)

    elif file_type == 3:
        print("Для обработки выбран XLSX-файл.")
        file_path = base_path / 'financial_transactions' / 'transactions_excel.xlsx'
        return excel_data(file_path)

    return None


def filter_by_status(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по статусу, запрашивая его у пользователя"""

    valid_statuses = ['EXECUTED', 'CANCELED', 'PENDING']

    while True:
        print(
            """
Введите статус, по которому необходимо выполнить фильтрацию.
Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"""
        )
        status_input = input("Ваш выбор: ").strip()

        # Приводим к верхнему регистру для сравнения
        status_upper = status_input.upper()

        if status_upper in valid_statuses:
            print(f"\nОперации отфильтрованы по статусу \"{status_upper}\"")
            # Фильтруем
            filtered = [tr for tr in transactions if str(tr.get('state', '')).upper() == status_upper]
            return filtered
        else:
            print(f"Статус операции \"{status_input}\" недоступен.")


def format_date(date_str: str) -> str:
    """Функция для извлечения даты из транзакции в формат DD.MM.YYYY"""
    if not date_str:
        return "Дата не указана"

    date_str = str(date_str)

    # Убираем время, если есть
    if 'T' in date_str:
        date_str = date_str.split('T')[0]
    if ' ' in date_str:
        date_str = date_str.split(' ')[0]

    parts = re.findall(r'\d+', date_str)

    if len(parts) == 3:
        # Если первая часть = 4 цифры (YYYY.MM.DD), то меняем порядок
        if len(parts[0]) == 4:
            return f"{parts[2]}.{parts[1]}.{parts[0]}"
        else:
            return f"{parts[0]}.{parts[1]}.{parts[2]}"

    # Если не 3 части, возможно дата без разделителей типа 20241225
    if len(parts) == 1 and len(parts[0]) == 8:
        year = parts[0][:4]
        month = parts[0][4:6]
        day = parts[0][6:8]
        return f"{day}.{month}.{year}"

    return date_str


def ask_sort(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Сортировка по дате"""

    while True:
        answer = input("\nОтсортировать операции по дате? Да/Нет: ").strip().lower()

        if answer in ['да']:
            while True:
                # Только если пользователь сказал "да" — спрашиваем направление
                direction = input("\nОтсортировать по возрастанию или по убыванию? ").strip().lower()
                if direction in ['по возрастанию']:
                    reverse = False
                    break
                elif direction in ['по убыванию']:
                    reverse = True
                    break
                else:
                    print("Пожалуйста, введите 'по возрастанию' или 'по убыванию'")

            sorted_transactions = sorted(transactions, key=lambda tr: format_date(tr.get('date', '')), reverse=reverse)
            print("Операции отсортированы.")
            return sorted_transactions

        elif answer in ['нет']:
            return transactions
        else:
            print("Пожалуйста, введите 'да' или 'нет'")


def ask_ruble_only(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Спрашивает, нужно ли оставить только рублёвые транзакции"""
    while True:
        answer_rub = input("\nВыводить только рублевые транзакции? Да/Нет: ").strip().lower()

        if answer_rub in ['да']:
            filtered = [tr for tr in transactions if tr.get('currency_code', '') == 'RUB']
            return filtered

        elif answer_rub in ['нет']:
            return transactions
        else:
            print("Пожалуйста, введите 'да' или 'нет'")


def ask_filter_by_description(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Спрашивает, нужно ли отфильтровать по слову в описании"""
    while True:
        answer_word = (
            input("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет: ").strip().lower()
        )

        if answer_word in ['да']:
            while True:  # цикл для повторного поиска
                search_word = input("Введите слово для поиска: ").strip()
                filtered = []
                for tr in transactions:
                    description = str(tr.get('description', '')).lower()
                    if search_word.lower() in description:
                        filtered.append(tr)

                if filtered:
                    print(f"Найдено {len(filtered)} транзакций, содержащих '{search_word}'.")
                    return filtered  # нашли — возвращаем результат
                else:
                    print(f"Транзакций, содержащих '{search_word}', не найдено.")

                    # Спрашиваем, хочет ли пользователь попробовать снова
                    while True:
                        retry = input("Хотите поискать снова? Да/Нет: ").strip().lower()
                        if retry in ['да']:
                            break  # выходим из цикла retry, идём на новый поиск
                        elif retry in ['нет']:
                            return transactions  # возвращаем исходный список
                        else:
                            print("Пожалуйста, введите 'да' или 'нет'")

        elif answer_word in ['нет']:
            return transactions
        else:
            print("Пожалуйста, введите 'да' или 'нет'")


def mask_card_number(card_str: str) -> str:
    """Маскирует номер карты (показывает только последние 4 цифры)"""
    # Преобразуем в строку, если пришло не строковое значение
    if card_str is None:
        return "Номер карты не найден"

    card_str = str(card_str)

    if not card_str or card_str == 'nan':
        return "Номер карты не найден"

    # Ищем 4 цифры в конце (последние 4 цифры карты/счёта)
    match = re.search(r'(\d{4})$', card_str)
    if match:
        last_four = match.group(1)
        return f"**{last_four}"
    return card_str


def display_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Выводит транзакции в красиво отформатированном виде"""
    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}")

    for tr in transactions:
        # Дата
        date = format_date(tr.get('date', 'Дата не указана'))

        # Описание
        description = tr.get('description', 'Без описания')

        # От кого/откуда и куда
        from_person = tr.get('from', '')
        to_person = tr.get('to', '')

        # Форматируем перевод
        if from_person and to_person:
            # Маскируем номера карт/счетов
            from_masked = mask_card_number(from_person)
            to_masked = mask_card_number(to_person)
            transfer_info = f"{from_masked} -> {to_masked}"
        else:
            transfer_info = "Данные о переводе отсутствуют"

        # Сумма и валюта
        amount = tr.get('amount', 0)
        currency = tr.get('currency_code', 'RUB')
        currency_symbol = "руб." if currency == 'RUB' else currency

        # Вывод
        print(f"{date} {description}")
        if transfer_info:
            print(transfer_info)
        print(f"Сумма: {amount} {currency_symbol}\n")


def main() -> None:
    """Главная функция программы"""
    print(
        """\nПривет! Добро пожаловать в программу работы с банковскими транзакциями
    Выберите необходимый пункт меню:
    1. Получить информацию о транзакциях из JSON-файла
    2. Получить информацию о транзакциях из CSV-файла
    3. Получить информацию о транзакциях из XLSX-файла
    """
    )
    while True:
        try:
            answer = int(input("Ваш выбор: "))
            if 1 <= answer <= 3:
                break
            else:
                print('Ввод неверный! Введите только номер пункта без пробелов')
        except ValueError:
            print('Ввод неверный! Введите только номер пункта без пробелов')

    # Загрузка транзакций
    transactions = load_transactions(answer)

    if not transactions:
        print("Не удалось загрузить транзакции. Проверьте файлы.")
        return

    # Фильтрация по статусу
    transactions = filter_by_status(transactions)

    # Сортировка по дате
    transactions = ask_sort(transactions)

    # Рублёвые транзакции
    transactions = ask_ruble_only(transactions)

    # Фильтрация по слову в описании
    transactions = ask_filter_by_description(transactions)

    # Вывод результатов
    display_transactions(transactions)


if __name__ == '__main__':
    main()
