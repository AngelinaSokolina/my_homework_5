from unittest.mock import Mock, patch

import requests

from src.external_api import convert_to_rub


def test_convert_to_rub_rub_currency()-> None:
    """Тест: если валюта RUB, функция возвращает сумму без API"""
    # Транзакция - это входные данные для функции
    transaction = {"operationAmount": {"amount": "100.50", "currency": {"code": "RUB"}}}
    # Вызываем функцию
    result = convert_to_rub(transaction)

    # Проверка результата
    assert result == 100.50  # проверяем, что сумма не изменилась
    assert isinstance(result, float)  # проверяем тип


@patch('requests.get')  # подменяем requests.get на mock_get
def test_convert_to_rub_usd(mock_get: Mock) -> None:   # mock_get приходит сюда
    """Тест: успешная конвертация USD в RUB (с подменой API)"""
    # Транзакция - это входные данные для функции
    transaction = {"operationAmount": {"amount": "1000.00", "currency": {"code": "USD"}}}
    # Подготовка поддельного ответа API
    mock_response = Mock()
    mock_response.json.return_value = {"result": 95000.00}  # .json()
    mock_response.raise_for_status.return_value = None  # .raise_for_status()

    # ПРИВЯЗЫВАЕМ поддельный ответ к requests.get
    mock_get.return_value = mock_response  # вызов get, вернется mock_response

    # Вызываем функцию
    result = convert_to_rub(transaction)

    # Проверка результата
    assert result == 95000.00

    # Проверка вызова API
    mock_get.assert_called_once()  # API вызывался ровно 1 раз

    # Проверка наименования валюты
    args, kwargs = mock_get.call_args
    assert "USD" in args[0]


@patch('requests.get')
def test_convert_to_rub_eur(mock_get: Mock) -> None:
    """Тест: успешная конвертация EUR в RUB (с подменой API)"""
    # Транзакция - это входные данные для функции
    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "EUR"}}}
    # Подготовка поддельного ответа API
    mock_response = Mock()
    mock_response.json.return_value = {"result": 10000.00}
    mock_response.raise_for_status.return_value = None

    # ПРИВЯЗЫВАЕМ поддельный ответ к requests.get
    mock_get.return_value = mock_response

    # Вызываем функцию
    result = convert_to_rub(transaction)

    # Проверка результата
    assert result == 10000.00

    # Проверка вызова API
    mock_get.assert_called_once()

    # Проверка наименования валюты
    args, kwargs = mock_get.call_args
    assert "EUR" in args[0]


@patch('requests.get')
def test_convert_connection_err(mock_get: Mock) -> None:
    """Тест на ошибку ConnectionError (нет интернета)"""
    # Транзакция - это входные данные для функции
    transaction = {"operationAmount": {"amount": "1021.50", "currency": {"code": "USD"}}}
    mock_get.side_effect = requests.exceptions.ConnectionError("No internet")
    # Вызываем функцию
    result = convert_to_rub(transaction)

    assert result == 1021.50


@patch('requests.get')
def test_convert_no_result(mock_get: Mock) -> None:
    """Тест: API вернул ответ без поля result"""
    transaction = {"operationAmount": {"amount": "500.00", "currency": {"code": "USD"}}}

    # Подготовка поддельного ответа API БЕЗ ПОЛЯ result
    mock_response = Mock()
    mock_response.json.return_value = {"info": "some data", "success": True}  # нет result!
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Вызываем функцию
    result = convert_to_rub(transaction)

    # Должна вернуть исходную сумму (amount), так как result нет
    assert result == 500.00
