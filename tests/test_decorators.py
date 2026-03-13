from pathlib import Path

import pytest
from _pytest.capture import CaptureFixture

from src.decorators import log, my_function

"""Тестирование работы декоратора"""


def test_log_capsys(capsys: CaptureFixture[str]) -> None:
    @log()
    def check_my_function(a: int, b: int) -> int:
        return a + b

    check_my_function(4, 50)
    result = capsys.readouterr().out.strip()
    assert result == "check_my_function ok"

    """Тест логирования ошибки в консоль"""


def test_log_error(capsys: CaptureFixture[str]) -> None:
    @log()
    def fail_func() -> None:
        raise ValueError("Ошибка!")

    with pytest.raises(ValueError):
        fail_func()

    result: str = capsys.readouterr().out
    assert "fail_func error: ValueError" in result

    """Тест записи лога в файл"""


def test_log_file(tmp_path: Path) -> None:
    log_file: Path = tmp_path / "test.log"

    @log(filename=str(log_file))
    def test_file_func(x: int) -> int:
        return x * 2

    test_file_func(5)

    # Читаем и проверяем содержимое файла
    log_content: str = log_file.read_text(encoding="utf-8")
    assert "test_file_func ok" in log_content

    """Тест того, что декоратор не портит возвращаемое значение функции"""


def test_log_results() -> None:
    assert my_function(2, 5) == 7
    assert my_function(-2, 5) == 3


"""Проверка @wraps"""


def test_log_wrap() -> None:
    assert my_function.__name__ == "my_function"
