import pytest
from typing import Any, Dict, List
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


@pytest.fixture
def transactions() -> List[Dict[str, Any]]:
    """Фикстура, возвращающая список транзакций для тестирования"""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 8953151,
            "state": "EXECUTED",
            "date": "2018-02-22T12:08:58.425572",
            "operationAmount": {"amount": "2550.00", "currency": {"name": "RUB", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 12345678901234567890",
            "to": "Счет 09876543210987654321",
        },
        {
            "id": 5942234,
            "state": "CANCELED",
            "date": "2023-07-10T15:20:05.206878",
            "operationAmount": {"amount": "150.00", "currency": {"name": "EUR", "code": "EUR"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 1596448206136579",
            "to": "MasterCard 1177661460596306",
        },
        {
            "id": 1234567,
            "state": "EXECUTED",
            "date": "2024-01-01T00:00:01.000000",
            "operationAmount": {"amount": "50550.48", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 11112222333344445555",
            "to": "Счет 99998888777766665555",
        },
    ]


def test_filter_by_currency(transactions: List[Dict[str, Any]]) -> None:
    """Тест функции фильтрации по валюте"""
    result_transaction = filter_by_currency(transactions, "USD")

    # Проверка первой транзакции
    first_transaction = next(result_transaction)
    assert first_transaction["operationAmount"]["currency"]["code"] == "USD"
    assert first_transaction["id"] == 939719570

    # Проверка второй транзакции
    second_transaction = next(result_transaction)
    assert second_transaction["operationAmount"]["currency"]["code"] == "USD"
    assert second_transaction["id"] == 142264268


def test_transaction_descriptions(transactions: List[Dict[str, Any]]) -> None:
    """Тест генератора по выводу операций"""
    descriptions = transaction_descriptions(transactions)
    # Проверяем каждое описание по порядку
    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод с карты на карту"
    assert next(descriptions) == "Перевод организации"


def test_card_number_generator():
    """Тест генератора диапозона карт"""
    expected_result = ["0000 0000 0000 0001", "0000 0000 0000 0002"]
    result = card_number_generator(1, 2)
    assert next(result) == expected_result[0]
