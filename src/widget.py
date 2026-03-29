# Импортируем функции из модуля masks
from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """Функция, которая умеет обрабатывать информацию как о картах, так и о счетах"""

    # Разделяем строку на части.
    parts = info.split()

    # Извлекаем номер
    number = parts[-1]

    # Сбор названия, т.е. склеиваем обратно изначальный ввод через пробел
    name = " ".join(parts[:-1])

    # Проверяем, счет это или карта
    if name.lower().replace("ё", "е") == "счет":
        # Используем функцию для счета из модуля masks
        return f"{name} {get_mask_account(number)}"
    else:
        # Используем функцию для карты из модуля masks
        return f"{name} {get_mask_card_number(number)}"


def get_date(date_string: str) -> str:
    """Функция, которая принимает на вход строку с датой и возвращает её в формате ДД.ММ.ГГГГ"""
    # Если строка пустая
    if date_string == "":
        return ""
    # Извлекаем дату до символа 'T' и отсекаем время
    date_part = date_string.split("T")[0]

    # Из этого кусочка вынимаем только цифры
    only_digits = ""
    for char in date_part:
        if char.isdigit():
            only_digits = only_digits + char
    # Проверяем, хватит ли нам цифр для даты (ГГГГММДД — это 8 цифр)
    if len(only_digits) < 8:
        return ""

    # Режем по индексам (теперь там точно только дата!)
    year = only_digits[0:4]
    month = only_digits[4:6]
    day = only_digits[6:8]

    return f"{day}.{month}.{year}"


# Проверка, чтобы запустить файлы и проверить
if __name__ == "__main__":
    # Функция, которая умеет обрабатывать информацию как о картах, так и о счетах
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Счет 73654108430135874305"))

    # Функция, которая принимает на вход строку с датой и возвращает её в формате ДД.ММ.ГГГГ
    print(get_date("2024-03-11T02:26:18.671407"))
