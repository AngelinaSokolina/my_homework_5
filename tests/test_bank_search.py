import tempfile     # Это модуль для создания временных файлов и папок
from pathlib import Path
from typing import Any

import pandas as pd

from src.bank_search import excel_data, process_bank_search


# ТЕСТЫ ДЛЯ excel_data

def test_excel_data_returns_list() -> None:
    """Проверяет, что функция возвращает список"""
    # Создаём временный Excel-файл с тестовыми данными
    test_data: pd.DataFrame = pd.DataFrame([{"description": "test", "amount": 100}])

    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        tmp_path: str = tmp.name
        test_data.to_excel(tmp_path, index=False)

    try:
        result: list[dict[str, Any]] = excel_data(tmp_path)
        # Проверка: результат должен быть списком
        assert isinstance(result, list)
    finally:
        # Удаляем временный файл
        Path(tmp_path).unlink()


def test_excel_data_returns_dicts() -> None:
    """Проверяет, что элементы списка — словари"""
    test_data: pd.DataFrame = pd.DataFrame([{"description": "test", "amount": 100}])

    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        tmp_path: str = tmp.name
        test_data.to_excel(tmp_path, index=False)

    try:
        result: list[dict[str, Any]] = excel_data(tmp_path)
        assert isinstance(result[0], dict)
    finally:
        Path(tmp_path).unlink()


def test_excel_data_correct_values() -> None:
    """Проверяет, что данные загружаются правильно"""
    test_data: pd.DataFrame = pd.DataFrame([{"description": "Тест", "amount": 500}])

    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        tmp_path: str = tmp.name
        test_data.to_excel(tmp_path, index=False)

    try:
        result: list[dict[str, Any]] = excel_data(tmp_path)
        # Проверяем, что значения совпадают с исходными
        assert result[0]['description'] == "Тест"
        assert result[0]['amount'] == 500
    finally:
        Path(tmp_path).unlink()


# ТЕСТЫ ДЛЯ process_bank_search

def test_process_bank_search_returns_list() -> None:
    """Проверяет, что функция возвращает список"""
    data: list[dict[str, Any]] = [{"description": "Перевод организации", "amount": 100}]
    result: list[dict[str, Any]] = process_bank_search(data, "Перевод")
    assert isinstance(result, list)


def test_process_bank_search_finds_match() -> None:
    """Проверяет, что функция находит подходящие транзакции"""
    data: list[dict[str, Any]] = [
        {"description": "Перевод организации", "amount": 100},  # должна найтись
        {"description": "Оплата услуг", "amount": 200},  # не должна найтись
    ]
    result: list[dict[str, Any]] = process_bank_search(data, "Перевод")

    # Проверка: нашлась только одна транзакция
    assert len(result) == 1
    assert result[0]['description'] == "Перевод организации"


def test_process_bank_search_case_insensitive() -> None:
    """Проверяет, что поиск не зависит от регистра"""
    data: list[dict[str, Any]] = [
        {"description": "ПЕРЕВОД организации", "amount": 100},
        {"description": "перевод с карты", "amount": 200}
    ]
    result: list[dict[str, Any]] = process_bank_search(data, "Перевод")
    assert len(result) == 2


def test_process_bank_search_empty_list() -> None:
    """Проверяет обработку пустого списка транзакций"""
    result: list[dict[str, Any]] = process_bank_search([], "Перевод")
    assert result == []


def test_process_bank_search_partial_match() -> None:
    """Проверяет частичное совпадение (искомая строка внутри описания)"""
    data: list[dict[str, Any]] = [
        {"description": "Срочный Перевод организации", "amount": 100},  # "Перевод" внутри
        {"description": "Оплата услуг", "amount": 200},  # нет "Перевод"
    ]
    result: list[dict[str, Any]] = process_bank_search(data, "Перевод")
    # Проверка: нашлась только одна транзакция
    assert len(result) == 1


def test_process_bank_search_missing_description() -> None:
    """Проверяет обработку транзакций без поля description"""
    data: list[dict[str, Any]] = [
        {"amount": 100},  # нет description
        {"description": "Перевод организации", "amount": 200}
    ]
    result: list[dict[str, Any]] = process_bank_search(data, "Перевод")
    assert len(result) == 1
