from unittest.mock import patch

from financial_transactions.personal import speak_question

"""Проверка работоспособности кода: id есть"""
@patch('builtins.input')
def test_personal_yes(mock_input):
    # Настраиваем: при вызове input() вернуть 650703
    mock_input.return_value = "650703"
    # Вызываем функцию
    speak_question()


"""Проверка работоспособности кода: id нет"""
@patch('builtins.input')
def test_personal_no(mock_input):
    # Настраиваем: при вызове input() сначало вводится неверный ввод и выводится сообщение,
    # а после вверный - информация о счете
    mock_input.side_effect = ["5852", "650703"]
    # Вызываем функцию
    speak_question()


"""Проверка работоспособности кода: ввод id не из цифр """
@patch('builtins.input')
def test_personal_false(mock_input):
    # Настраиваем: при вызове input() сначало вводится неверный ввод и выводится сообщение,
    # а после вверный - информация о счете
    mock_input.side_effect = ["sedrftgyhujk","rtgyuhv 438", "650703"]
    # Вызываем функцию
    speak_question()

