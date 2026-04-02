from typing import Any

import pytest


# _________________________________ДЛЯ test_processing_________________________________
@pytest.fixture
def operation_data() -> list[dict[str, Any]]:
    """Общая фикстура со списком для фильтрации и сортировки"""
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2024-03-11T02:26:18.671407'},
        {'id': 2, 'state': 'CANCELED', 'date': '2023-05-24T10:15:00.000000'},
        {'id': 3, 'state': 'EXECUTED', 'date': '2025-01-01T00:00:00.000000'},
        {'id': 4, 'state': 'CANCELED', 'date': '2025-01-01T00:00:00.000000'},
        {'id': 5, 'state': 'PENDING', 'date': '2022-12-31T23:59:59.999999'},
    ]


@pytest.fixture
def empty_list() -> list[Any]:
    """Фикстура для проверки пустого списка"""
    return []


# _________________________________ДЛЯ test_masks_________________________________
@pytest.fixture
def standard_card_number() -> str:
    """Фикструра правильного ввода номера карты"""
    return '8403867812345678'


@pytest.fixture
def standard_account_number() -> str:
    """Фикструра правильного ввода номера счета"""
    return '43740123789432175640'


@pytest.fixture
def incorrect_input() -> str:
    """Общая фикструра неккоректного ввода данных"""
    return '4376rjunei 34rf3 erf'


@pytest.fixture
def empty_input() -> str:
    """Фикстура для проверки пустого ввода"""
    return ""


# _________________________________ДЛЯ test_widget_________________________________
@pytest.fixture
def clean_input_card() -> str:
    """Фикструра правильного ввода номера и названия карты"""
    return "Visa 4321567812345678"


@pytest.fixture
def clean_complex_input_card() -> str:
    return "Maestro Gold 1234567812345678"


@pytest.fixture
def clean_input_account() -> str:
    """Фикструра правильного ввода счета"""
    return "Счет 43740123789432175640"


@pytest.fixture
def date_verification() -> str:
    """Фикструра ввода даты"""
    return "2024-03-11T02:26:18.671407"


@pytest.fixture
def no_date_verification() -> str:
    """Фикструра отсутствия даты"""
    return "4567щльд"
