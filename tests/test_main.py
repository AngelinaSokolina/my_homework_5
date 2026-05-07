from unittest.mock import patch, Mock

from src.main import (
    ask_filter_by_description,
    ask_ruble_only,
    ask_sort,
    filter_by_status,
    format_date,
    mask_card_number,
)

# ТЕСТЫ filter_by_status


@patch('builtins.input')
def test_filter_by_status_executed(mock_input: Mock) -> None:
    """Проверяет фильтрацию по статусу EXECUTED"""
    mock_input.return_value = "EXECUTED"

    transactions = [
        {"state": "EXECUTED", "description": "Перевод"},
        {"state": "CANCELED", "description": "Отмена"},
        {"state": "EXECUTED", "description": "Другой перевод"},
    ]

    result = filter_by_status(transactions)

    assert len(result) == 2
    assert all(t['state'] == 'EXECUTED' for t in result)


@patch('builtins.input')
def test_filter_by_status_canceled(mock_input: Mock) -> None:
    """Проверяет фильтрацию по статусу CANCELED"""
    mock_input.return_value = "CANCELED"

    transactions = [
        {"state": "EXECUTED", "description": "Перевод"},
        {"state": "CANCELED", "description": "Отмена"},
        {"state": "CANCELED", "description": "Другая отмена"},
    ]

    result = filter_by_status(transactions)

    assert len(result) == 2
    assert all(t['state'] == 'CANCELED' for t in result)


@patch('builtins.input')
def test_filter_by_status_pending(mock_input: Mock) -> None:
    """Проверяет фильтрацию по статусу PENDING"""
    mock_input.return_value = "PENDING"

    transactions = [
        {"state": "EXECUTED", "description": "Перевод"},
        {"state": "PENDING", "description": "Ожидание"},
        {"state": "PENDING", "description": "Другое ожидание"},
    ]

    result = filter_by_status(transactions)

    assert len(result) == 2
    assert all(t['state'] == 'PENDING' for t in result)


def test_filter_by_status_missing_state() -> None:
    """Проверяет обработку транзакций без поля state"""
    transactions = [{"description": "Перевод"}, {"state": "EXECUTED", "description": "Перевод"}]  # нет state

    # Подменяем input
    with patch('builtins.input', return_value="EXECUTED"):
        result = filter_by_status(transactions)

    assert len(result) == 1


# ТЕСТЫ ask_sort


@patch('builtins.input')
def test_ask_sort_no(mock_input: Mock) -> None:
    """Проверяет, что при ответе 'нет' сортировка не применяется"""
    mock_input.return_value = "нет"

    transactions = [{"date": "2024-12-25", "description": "Позже"}, {"date": "2024-12-20", "description": "Раньше"}]

    result = ask_sort(transactions)

    # Список должен остаться в исходном порядке
    assert result == transactions


@patch('builtins.input')
def test_ask_sort_ascending(mock_input: Mock) -> None:
    """Проверяет сортировку по возрастанию"""
    mock_input.side_effect = ["да", "по возрастанию"]

    transactions = [
        {"date": "2024-12-25", "description": "Позже"},
        {"date": "2024-12-20", "description": "Раньше"},
        {"date": "2024-12-22", "description": "Средняя"},
    ]

    result = ask_sort(transactions)

    # Должно быть отсортировано по возрастанию даты
    assert result[0]['date'] == "2024-12-20"
    assert result[1]['date'] == "2024-12-22"
    assert result[2]['date'] == "2024-12-25"


@patch('builtins.input')
def test_ask_sort_descending(mock_input: Mock) -> None:
    """Проверяет сортировку по убыванию"""
    mock_input.side_effect = ["да", "по убыванию"]

    transactions = [
        {"date": "2024-12-20", "description": "Раньше"},
        {"date": "2024-12-25", "description": "Позже"},
        {"date": "2024-12-22", "description": "Средняя"},
    ]

    result = ask_sort(transactions)

    # Должно быть отсортировано по убыванию даты
    assert result[0]['date'] == "2024-12-25"
    assert result[1]['date'] == "2024-12-22"
    assert result[2]['date'] == "2024-12-20"


# ТЕСТЫ ask_ruble_only


@patch('builtins.input')
def test_ask_ruble_only_yes(mock_input: Mock) -> None:
    """Проверяет фильтрацию только рублёвых транзакций"""
    mock_input.return_value = "да"

    transactions = [
        {"currency_code": "RUB", "amount": 100},
        {"currency_code": "USD", "amount": 200},
        {"currency_code": "RUB", "amount": 300},
        {"currency_code": "EUR", "amount": 400},
    ]

    result = ask_ruble_only(transactions)

    assert len(result) == 2
    assert all(t['currency_code'] == 'RUB' for t in result)


@patch('builtins.input')
def test_ask_ruble_only_no(mock_input: Mock) -> None:
    """Проверяет, что при ответе 'нет' фильтрация не применяется"""
    mock_input.return_value = "нет"

    transactions = [{"currency_code": "RUB", "amount": 100}, {"currency_code": "USD", "amount": 200}]

    result = ask_ruble_only(transactions)

    # Список не изменился
    assert len(result) == 2
    assert result == transactions


@patch('builtins.input')
def test_ask_ruble_only_invalid_then_valid(mock_input: Mock) -> None:
    """Проверяет: сначала неверный ввод, потом 'да'"""
    mock_input.side_effect = ["вкаемпро", "да"]

    transactions = [{"currency_code": "RUB", "amount": 100}, {"currency_code": "USD", "amount": 200}]

    result = ask_ruble_only(transactions)

    assert len(result) == 1
    assert result[0]['currency_code'] == 'RUB'


# ТЕСТЫ ask_filter_by_description


@patch('builtins.input')
def test_ask_filter_by_description_found(mock_input: Mock) -> None:
    """Проверяет фильтрацию по слову в описании (найдено)"""
    mock_input.side_effect = ["да", "Перевод"]

    transactions = [
        {"description": "Перевод организации", "amount": 100},
        {"description": "Оплата услуг", "amount": 200},
        {"description": "Перевод с карты", "amount": 300},
    ]

    result = ask_filter_by_description(transactions)

    assert len(result) == 2
    assert "Перевод" in result[0]['description']
    assert "Перевод" in result[1]['description']


@patch('builtins.input')
def test_ask_filter_by_description_not_found_then_cancel(mock_input: Mock) -> None:
    """Проверяет: не найдено → отмена → возврат исходного списка"""
    mock_input.side_effect = ["да", "xyz", "нет"]

    transactions = [
        {"description": "Перевод организации", "amount": 100},
        {"description": "Оплата услуг", "amount": 200},
    ]

    result = ask_filter_by_description(transactions)

    # Вернулся исходный список
    assert result == transactions


# ТЕСТЫ format_date


def test_format_date_standard() -> None:
    """Проверяет преобразование стандартной даты YYYY-MM-DD"""
    result = format_date("2024-12-25")
    assert result == "25.12.2024"


def test_format_date_with_dots() -> None:
    """Проверяет преобразование даты с точками YYYY.MM.DD"""
    result = format_date("2024.12.25")
    assert result == "25.12.2024"


def test_format_date_with_slashes() -> None:
    """Проверяет преобразование даты со слешами"""
    result = format_date("2024/12/25")
    assert result == "25.12.2024"


def test_format_date_without_separators() -> None:
    """Проверяет преобразование даты без разделителей YYYYMMDD"""
    result = format_date("20241225")
    assert result == "25.12.2024"


def test_format_date_empty() -> None:
    """Проверяет обработку пустой строки"""
    result = format_date("")
    assert result == "Дата не указана"


def test_format_date_with_time() -> None:
    """Проверяет преобразование даты с временем (ISO формат)"""
    result = format_date("2024-12-25T14:30:00")
    assert result == "25.12.2024"


# ТЕСТЫ mask_card_number


def test_mask_card_number_standard() -> None:
    """Проверяет маскировку номера карты (последние 4 цифры)"""
    result = mask_card_number("MasterCard 7771 27** **** 3727")
    assert result == "**3727"


def test_mask_card_number_only_digits() -> None:
    """Проверяет маскировку строки, состоящей только из цифр"""
    result = mask_card_number("1234567890123727")
    assert result == "**3727"


def test_mask_card_number_empty() -> None:
    """Проверяет обработку пустой строки"""
    result = mask_card_number("")
    assert result == "Номер карты не найден"


def test_mask_card_number_account() -> None:
    """Проверяет маскировку номера счёта"""
    result = mask_card_number("Счет **4321")
    assert result == "**4321"
