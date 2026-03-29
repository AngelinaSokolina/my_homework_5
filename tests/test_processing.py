from typing import Any

import pytest

from src.processing import filter_by_state, sort_by_date

# ______________БЛОК ТЕСТА С ДАННЫМИ ВВЕДЕННЫМИ ВРУЧНУЮ______________
"""Тест для функции, которая фильтрует список словарей по значению ключа 'state'."""


@pytest.mark.parametrize(
    "data_filter, state_to_find, expected_filter",
    [
        # 1. Проверка правильности фильтра (Ожидаем СПИСОК с одним словарем)
        (
            [
                {'id': 1, 'state': 'EXECUTED', 'date': '2019-07-03'},
                {'id': 2, 'state': 'CANCELED', 'date': '2018-06-30'},
            ],
            'EXECUTED',
            [{'id': 1, 'state': 'EXECUTED', 'date': '2019-07-03'}],
        ),
        # 2. Отсутствие статуса (Ожидаем пустой список)
        ([{'id': 2, 'state': 'CANCELED', 'date': '2018-06-30'}], 'EXECUTED', []),
        # 3. Пустой входной список
        ([], 'EXECUTED', []),
    ],
)
def test_filter_by_state(
    data_filter: list[dict[str, Any]], state_to_find: str, expected_filter: list[dict[str, Any]]
) -> None:
    assert filter_by_state(data_filter, state_to_find) == expected_filter


# ______________БЛОК ТЕСТА С ФИКСТУРОЙ______________
def test_filter_by_state_executed(operation_data: list[dict[str, Any]]) -> None:
    # Pytest сам подставит сюда список из conftest.py
    result = filter_by_state(operation_data, 'EXECUTED')
    assert len(result) == 2
    assert result[0]['id'] == 1
    assert result[1]['id'] == 3


def test_filter_empty(empty_list: list[dict[str, Any]]) -> None:
    # Pytest подставит пустой список []
    assert filter_by_state(empty_list, 'EXECUTED') == []


# ______________БЛОК ТЕСТА С ДАННЫМИ ВВЕДЕННЫМИ ВРУЧНУЮ______________
"""
Тест для функции сортировки списка словарей по ключу 'date'.
По умолчанию сортировка идет от новых к старым (убывание).
"""


@pytest.mark.parametrize(
    "data_sort, is_reverse, expected_sort",
    [
        # 1. Проверка правильности сортировки по убыванию
        (
            [{'id': 1, 'date': '2019-07-03'}, {'id': 2, 'date': '2018-06-30'}],
            True,
            [{'id': 1, 'date': '2019-07-03'}, {'id': 2, 'date': '2018-06-30'}],
        ),
        # 2. Проверка правильности сортировки по возрастанию
        (
            [{'id': 1, 'date': '2019-07-03'}, {'id': 2, 'date': '2018-06-30'}],
            False,
            [{'id': 2, 'date': '2018-06-30'}, {'id': 1, 'date': '2019-07-03'}],
        ),
        # 3. Проверка одинаковых дат
        (
            [
                {'id': 1, 'date': '2020-07-03'},
                {'id': 2, 'state': 'CANCELED', 'date': '2018-06-30'},
                {'id': 3, 'date': '2020-07-03'},
            ],
            False,
            [
                {'id': 2, 'state': 'CANCELED', 'date': '2018-06-30'},
                {'id': 1, 'date': '2020-07-03'},
                {'id': 3, 'date': '2020-07-03'},
            ],
        ),
    ],
)
def test_sort_by_date(data_sort: list[dict[str, Any]], is_reverse: bool, expected_sort: list[dict[str, Any]]) -> None:
    assert sort_by_date(data_sort, reverse=is_reverse) == expected_sort


"""Дополнительный маленький тест для сортировки, 
когда ожидаем, что внутри этого блока возникнет KeyError"""


def test_sort_by_date_errors() -> None:
    with pytest.raises(KeyError):
        # Передаем список, где у одного словаря нет ключа 'date'
        sort_by_date([{'id': 1, 'date': '2023'}, {'id': 2}], reverse=True)


# ______________БЛОК ТЕСТА С ФИКСТУРОЙ______________
def test_sort_by_date_executed_ascending(operation_data: list[dict[str, Any]]) -> None:
    # Pytest сам подставит сюда список из conftest.py
    result = sort_by_date(operation_data, False)
    assert len(result) == 5
    assert result[0]['id'] == 5
    assert result[-1]['id'] == 4


def test_sort_by_date_executed_descending(operation_data: list[dict[str, Any]]) -> None:
    # Pytest сам подставит сюда список из conftest.py
    result = sort_by_date(operation_data, True)
    assert result[0]['id'] == 3
    assert result[-1]['id'] == 5


def test_sort_empty(empty_list: list[Any]) -> None:
    # Pytest подставит пустой список []
    assert sort_by_date(empty_list, True) == []
    assert sort_by_date(empty_list, False) == []
