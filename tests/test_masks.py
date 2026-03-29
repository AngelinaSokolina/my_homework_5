import pytest

from src.masks import get_mask_account, get_mask_card_number

# ______________БЛОК ТЕСТА С ДАННЫМИ ВВЕДЕННЫМИ ВРУЧНУЮ______________
"""Тест для функции маскировки номера банковской карты"""


@pytest.mark.parametrize(
    "card_number, expected_card",
    [
        # 1. Проверка правильности маскирования
        ("1234567812345678", "1234 56** **** 5678"),
        # 2. Проверка работы с пробелами по краям (strip)
        (" 1234567812345678 ", "1234 56** **** 5678"),
        # 3. Слишком короткий номер карты
        ("12345678", "Ошибка: номер карты должен состоять из 16 цифр"),
        # 4. Слишком длинный номер карты
        ("123456781234567890", "Ошибка: номер карты должен состоять из 16 цифр"),
        # 5. Нестандартные символы (не цифры)
        ("12345678ABCD5678", "Ошибка: номер карты должен состоять из 16 цифр"),
        # 6. Отсутствие номера (пустая строка)
        ("", "Ошибка: номер карты должен состоять из 16 цифр"),
        # 7. Строка с пробелами вместо номера карты
        ("                ", "Ошибка: номер карты должен состоять из 16 цифр"),
    ],
)
def test_mask_card(card_number: str, expected_card: str) -> None:
    assert get_mask_card_number(card_number) == expected_card

    # ______________БЛОК ТЕСТА С ФИКСТУРОЙ______________


def test_mask_card_executed(standard_card_number: str) -> None:
    result = get_mask_card_number(standard_card_number)
    assert result == "8403 86** **** 5678"


def test_incorrect_card_executed(incorrect_input: str) -> None:
    assert get_mask_card_number(incorrect_input) == "Ошибка: номер карты должен состоять из 16 цифр"


def test_empty_card_executed(empty_input: str) -> None:
    assert get_mask_card_number(empty_input) == "Ошибка: номер карты должен состоять из 16 цифр"

    # ______________БЛОК ТЕСТА С ДАННЫМИ ВВЕДЕННЫМИ ВРУЧНУЮ______________
    """Тест для функции маскировки номера банковского счета"""


@pytest.mark.parametrize(
    "account_number, expected_account",
    [
        # 1. Проверка правильности маскирования
        ("12345678123456781212", "**1212"),
        # 2. Проверка работы с пробелами по краям (strip)
        (" 12345678123456781212 ", "**1212"),
        # 3. Слишком короткий номер счета
        ("12345678", "Ошибка: номер счета должен состоять из 20 цифр"),
        # 4. Слишком длинный номер счета
        ("12345678123456781212345", "Ошибка: номер счета должен состоять из 20 цифр"),
        # 5. Нестандартные символы (не цифры)
        ("123456781234567вы212", "Ошибка: номер счета должен состоять из 20 цифр"),
        # 6. Отсутствие номера (пустая строка)
        ("", "Ошибка: номер счета должен состоять из 20 цифр"),
        # 7. Строка с пробелами вместо номера счета
        ("                    ", "Ошибка: номер счета должен состоять из 20 цифр"),
    ],
)
def test_mask_account(account_number: str, expected_account: str) -> None:
    assert get_mask_account(account_number) == expected_account

    # ______________БЛОК ТЕСТА С ФИКСТУРОЙ______________


def test_mask_account_executed(standard_account_number: str) -> None:
    result = get_mask_account(standard_account_number)
    assert result == "**5640"


def test_incorrect_account_executed(incorrect_input: str) -> None:
    assert get_mask_account(incorrect_input) == "Ошибка: номер счета должен состоять из 20 цифр"


def test_empty_account_executed(empty_input: str) -> None:
    assert get_mask_account(empty_input) == "Ошибка: номер счета должен состоять из 20 цифр"
