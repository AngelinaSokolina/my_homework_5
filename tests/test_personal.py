from pathlib import Path
from unittest.mock import Mock, patch

from financial_transactions.personal import load_excel_data, speak_question


@patch('builtins.input')
def test_personal_yes(mock_input: Mock) -> None:
    """Проверка работоспособности кода: id есть"""

    data = load_excel_data(Path(__file__).parent.parent / 'financial_transactions' / 'transactions_excel.xlsx')
    # Настраиваем: при вызове input() вернуть 650703
    mock_input.return_value = "650703"
    # Вызываем функцию
    speak_question(data)


@patch('builtins.input')
def test_personal_no(mock_input: Mock) -> None:
    """Проверка работоспособности кода: id нет"""

    data = load_excel_data(Path(__file__).parent.parent / 'financial_transactions' / 'transactions_excel.xlsx')
    # Настраиваем: при вызове input() сначала вводится неверный ввод и выводится сообщение,
    # а после верный - информация о счете
    mock_input.side_effect = ["5852", "650703"]
    # Вызываем функцию
    speak_question(data)


@patch('builtins.input')
def test_personal_false(mock_input: Mock) -> None:
    """Проверка работоспособности кода: ввод id не из цифр"""
    data = load_excel_data(Path(__file__).parent.parent / 'financial_transactions' / 'transactions_excel.xlsx')
    # Настраиваем: при вызове input() сначало вводится неверный ввод и выводится сообщение,
    # а после вверный - информация о счете
    mock_input.side_effect = ["sedrftgyhujk", "rtgyuhv 438", "650703"]
    # Вызываем функцию
    speak_question(data)
