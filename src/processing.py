from typing import Any


def filter_by_state(data: list[dict[str, Any]], state: str = 'EXECUTED') -> list[dict[str, Any]]:
    """Функция фильтрует список словарей по значению ключа 'state'."""

    result_filtering = []
    # Перебираем каждый словарь в списке
    for item in data:
        # Проверяем, совпадает ли значение по ключу 'state' с искомым
        if item.get('state') == state:
            result_filtering.append(item)

    return result_filtering


def sort_by_date(data: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """
    Функция для сортировки списка словарей по ключу 'date'.
    По умолчанию сортировка идет от новых к старым (убывание).
    """
    # sorted — берет список data и делает его копию, чтобы отсортировать
    # key=lambda x: x['date'] — ИЩЕТ КЛЮЧ ПО СЛОВУ
    # reverse=reverse — если True, то сначала новые, если False — старые
    return sorted(data, key=lambda x: x['date'], reverse=reverse)
