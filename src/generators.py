from typing import Generator


def filter_by_currency(transactions: list[dict], currency_code: str) -> Generator[dict, None, None]:
    """Фильтрует транзакции по коду валюты и выдает их по одной"""
    for transaction in transactions:
        # Проверяем код валюты через глубокий доступ к ключам
        if transaction["operationAmount"]["currency"]["code"] == currency_code:
            yield transaction


def transaction_descriptions(transactions: list[dict]) -> Generator[str, None, None]:
    """Выдает описание каждой операции по очереди"""
    for transaction in transactions:
        descriptions = transaction["description"]
        yield descriptions

        # Заметка для преподавателя:
        # yield f"Перевод с {transaction.get('from')} на {transaction.get('to')}"
        # Я так поняла, что в данной ситуации так делать не нужно,
        # так как в задании просили возвращать именно описание (description) каждой операции.


# Или всё таки нужно?


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """Генератор диапозона номера"""
    for number in range(start, stop + 1):
        card_number = str(number).zfill(16)
        yield f'{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:16]}'