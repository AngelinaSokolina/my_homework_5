import pandas as pd

# Импортируем функции из модуля developer
from financial_transactions.developer import count_by_status, get_currency_rating


def test_count_by_status() -> None:
    """
    Тестирует функцию count_by_status.
    Проверяет, что функция правильно считает количество операций
    по статусам EXECUTED, PENDING, CANCELED.
    """
    # Тестовый DataFrame с известными данными
    test_data = pd.DataFrame({'state': ['EXECUTED', 'PENDING', 'CANCELED', 'EXECUTED', 'PENDING']})

    # Вызов функции
    result = count_by_status(test_data)

    # Проверка, что результат — словарь
    assert isinstance(result, dict)

    # Проверяем, что в словаре три ключа
    assert set(result.keys()) == {'Выполненных операций', 'Операций "в ожидании"', 'Отмененные операции'}

    # Проверяем правильность подсчёта
    assert result['Выполненных операций'] == 2
    assert result['Операций "в ожидании"'] == 2
    assert result['Отмененные операции'] == 1

    # Проверяем, что сумма трёх чисел равна общему количеству строк
    total = sum(result.values())
    assert total == len(test_data)


def test_get_currency_rating() -> None:
    """
    Тестирует функцию get_currency_rating.
    Проверяет, что функция возвращает топ-N самых частых валют.
    """
    # Тестовый DataFrame с повторяющимися кодами валют
    test_data = pd.DataFrame({'currency_code': ['RUB', 'USD', 'RUB', 'EUR', 'RUB', 'USD', 'RUB', 'EUR', 'RUB']})
    # RUB встречается 5 раз, USD — 2 раза, EUR — 2 раза

    # Вызов функции с top=2
    result = get_currency_rating(test_data, top=2)

    # Проверяем, что результат — Series
    assert isinstance(result, pd.Series)

    # Проверяем, что в результате 2 строки
    assert len(result) == 2

    # Проверяем, что первое место — RUB с количеством 5
    assert result.index[0] == 'RUB'
    assert result.iloc[0] == 5

    # Проверяем, что второе место — USD (или EUR, если порядок другой)
    assert result.iloc[1] == 2
