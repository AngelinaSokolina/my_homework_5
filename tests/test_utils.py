import json
from unittest.mock import mock_open, patch, Mock

from src.utils import reception_json


def test_reception_json_success() -> None:
    """Тестируем успешное чтение файла с корректным JSON-списком"""
    # Это те данные, которые "как бы" лежат в файле
    test_data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    json_string = json.dumps(test_data)

    # СОЗДАЕМ ЯВНЫЙ MOCK ДЛЯ OPEN
    mock_file = mock_open(read_data=json_string)

    # ПОДМЕНА ОТКРЫТИЯ ФАЙЛА
    # mock_open - специальная функция, которая создает подделку open()
    # read_data - это то, что "прочитается" из файла
    # json.dumps(test_data) превращает список в JSON-строку
    with patch("builtins.open", mock_file):
        with patch("pathlib.Path.exists") as mock_exists:
            # Говорим, что файл существует
            mock_exists.return_value = True

            # ВЫЗЫВАЕМ ФУНКЦИЮ
            result = reception_json("fake_patch.json")

            # Проверка результата
            assert result == test_data  # должно вернуть наш тестовый список
            assert isinstance(result, list)  # и это должен быть список


def test_reception_json_not_list() -> None:
    """Тестируем случай, когда в файле не список, а словарь"""

    test_data = {"key": "value"}  # это словарь!

    with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
        result = reception_json("fake_patch.json")

        assert result == []  # ожидаем пустой список


@patch("pathlib.Path.exists")
def test_reception_json_file_not_exists(mock_exists: Mock) -> None:
    """Тестируем случай, когда файл не существует"""
    # Настройка mock: файл НЕ существует
    mock_exists.return_value = False

    # Вызов функции с любым путем
    result = reception_json("fake_file.json")

    # Проверка результата
    assert result == []  # ожидаем пустой список

    # Проверка вызова
    mock_exists.assert_called_once()


def test_reception_json_corrupted_file() -> None:
    """Тестируем случай, когда файл поврежден (невалидный JSON)"""
    # Подделка open, которая вернет невалидный JSON
    mock_file = mock_open(read_data="это не json { [;")

    with patch("builtins.open", mock_file):
        # НЕ подменяем json.load - пусть реально пытается прочитать
        result = reception_json("corrupted.json")

        assert result == []  # ожидаем пустой список


def test_reception_json_empty_file() -> None:
    """Проверка пустого файла"""

    with patch("builtins.open", mock_open(read_data="")):
        # Пустой файл вызовет JSONDecodeError
        result = reception_json("empty.json")

        assert result == []


print(f"Функция импортирована из: {reception_json.__module__}")
print(f"Путь к файлу функции: {reception_json.__code__.co_filename}")
