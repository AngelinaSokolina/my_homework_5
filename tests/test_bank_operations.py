import tempfile  # Это модуль для создания временных файлов и папок
from pathlib import Path
from typing import Any

import pandas as pd

from src.bank_operations import excel_data_operation, process_bank_operations

# ТЕСТЫ excel_data_operation


def test_excel_data_operation_returns_list() -> None:
    """Проверяет, что функция возвращает список"""
    # Создаём временный Excel-файл
    test_data: pd.DataFrame = pd.DataFrame(
        [
            {"description": "Перевод организации", "amount": 100},
            {"description": "Перевод с карты на карту", "amount": 200},
        ]
    )

    # Создаём временный файл
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        tmp_path: str = tmp.name
        test_data.to_excel(tmp_path, index=False)

    try:
        result: list[dict[str, Any]] = excel_data_operation(tmp_path)
        # Проверка: результат должен быть списком
        assert isinstance(result, list)
    finally:
        # Удаляем временный файл
        Path(tmp_path).unlink()


def test_excel_data_operation_returns_dicts() -> None:
    """Проверяет, что элементы списка — словари"""
    test_data: pd.DataFrame = pd.DataFrame([{"description": "Перевод организации", "amount": 100}])

    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        tmp_path: str = tmp.name
        test_data.to_excel(tmp_path, index=False)

    try:
        result: list[dict[str, Any]] = excel_data_operation(tmp_path)
        # Проверка: первый элемент списка должен быть словарём
        assert isinstance(result[0], dict)
    finally:
        Path(tmp_path).unlink()


# ТЕСТЫ process_bank_operations


def test_process_bank_operations_returns_dict() -> None:
    """Проверяет, что функция возвращает словарь"""
    data: list[dict[str, Any]] = [
        {"description": "Перевод организации", "amount": 100},
        {"description": "Перевод с карты на карту", "amount": 200},
    ]
    categories: list[str] = ["Перевод организации", "Перевод с карты на карту"]

    result: dict[str, int] = process_bank_operations(data, categories)

    # Проверка: результат должен быть словарём
    assert isinstance(result, dict)


def test_process_bank_operations_correct_keys() -> None:
    """Проверяет, что ключи словаря совпадают с категориями"""
    data: list[dict[str, Any]] = [{"description": "Перевод организации", "amount": 100}]
    categories: list[str] = ["Перевод организации", "Перевод с карты на карту"]

    result: dict[str, int] = process_bank_operations(data, categories)

    # Проверка: ключи результата = множеству категорий
    assert set(result.keys()) == set(categories)


def test_process_bank_operations_counts_correctly() -> None:
    """Проверяет правильность подсчёта"""
    data: list[dict[str, Any]] = [
        {"description": "Перевод организации", "amount": 100},
        {"description": "Перевод организации", "amount": 200},
        {"description": "Перевод с карты на карту", "amount": 150},
        {"description": "Открытие вклада", "amount": 500},
        {"description": "Просто перевод", "amount": 300},
    ]
    categories: list[str] = ["Перевод организации", "Перевод с карты на карту", "Открытие вклада"]

    result: dict[str, int] = process_bank_operations(data, categories)

    # Проверки: точное количество совпадений
    assert result["Перевод организации"] == 2
    assert result["Перевод с карты на карту"] == 1
    assert result["Открытие вклада"] == 1


def test_process_bank_operations_empty_list() -> None:
    """Проверяет обработку пустого списка транзакций"""
    data: list[dict[str, Any]] = []  # пустой список транзакций
    categories: list[str] = ["Перевод организации", "Перевод с карты на карту"]

    result: dict[str, int] = process_bank_operations(data, categories)

    # Проверка: все категории имеют 0
    assert result["Перевод организации"] == 0
    assert result["Перевод с карты на карту"] == 0


def test_process_bank_operations_no_categories() -> None:
    """Проверяет обработку пустого списка категорий"""
    data: list[dict[str, Any]] = [{"description": "Перевод организации", "amount": 100}]
    categories: list[str] = []  # пустой список категорий

    result: dict[str, int] = process_bank_operations(data, categories)

    # Проверка: результат — пустой словарь
    assert result == {}
