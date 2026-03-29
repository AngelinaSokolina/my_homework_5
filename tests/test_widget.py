import pytest

from src.widget import get_date, mask_account_card

# ______________БЛОК ТЕСТА С ДАННЫМИ ВВЕДЕННЫМИ ВРУЧНУЮ______________
"""Тест для функции, которая умеет обрабатывать информацию как о картах, так и о счетах"""


@pytest.mark.parametrize(
    "info, expected",
    [
        # 1. Проверка для карты (с названием)
        ("Visa 1234567812345678", "Visa 1234 56** **** 5678"),
        # 2. Проверка для счета (с названием)
        ("Счет 12345678901234567890", "Счет **7890"),
        # 3. Проверка с картой, где много слов в названии
        ("Maestro Gold 1234567812345678", "Maestro Gold 1234 56** **** 5678"),
        # 4. Некорректные данные (например, короткий счет)
        ("Счет 12345", "Счет Ошибка: номер счета должен состоять из 20 цифр"),
    ],
)
def test_mask_account_card(info: str, expected: str) -> None:
    assert mask_account_card(info) == expected

    # ______________БЛОК ТЕСТА С ФИКСТУРОЙ______________


def test_mask_card_executed(clean_input_card: str) -> None:
    result = mask_account_card(clean_input_card)
    assert result == "Visa 4321 56** **** 5678"


def test_complex_mask_card_executed(clean_complex_input_card: str) -> None:
    result = mask_account_card(clean_complex_input_card)
    assert result == "Maestro Gold 1234 56** **** 5678"


def test_mask_account_executed(clean_input_account: str) -> None:
    result = mask_account_card(clean_input_account)
    assert result == "Счет **5640"


# ______________БЛОК ТЕСТА С ДАННЫМИ ВВЕДЕННЫМИ ВРУЧНУЮ______________
"""Тест для функции, которая принимает на вход строку с датой и возвращает её в формате ДД.ММ.ГГГГ"""


@pytest.mark.parametrize(
    "string, expected_formatted_date",
    [
        # 1. Проверка корректности функции
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        # 2. Проверка различных входных форматах даты
        ("2024-03-11T01407", "11.03.2024"),
        ("2024-03-11T017", "11.03.2024"),
        (r"2024\03\11T045rftgybhuni17", "11.03.2024"),
        ("2024/03/11T017", "11.03.2024"),
        ("2024.03?11T01sxrdcfvgh7", "11.03.2024"),
        # 3. Проверка при отсутствии даты
        ("", ""),
        ("45678рогшщльд", ""),
    ],
)
def test_get_date(string: str, expected_formatted_date: str) -> None:
    assert get_date(string) == expected_formatted_date

    # ______________БЛОК ТЕСТА С ФИКСТУРОЙ______________


def test_get_date_executed(date_verification: str) -> None:
    result = get_date(date_verification)
    assert result == "11.03.2024"


def test_no_get_date_executed(no_date_verification: str) -> None:
    result = get_date(no_date_verification)
    assert result == ""
