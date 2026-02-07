from functools import wraps
from typing import Callable


def log(filename=None):
    """Декоратор, который логирует выполнение функции."""
    def wrapper(func: Callable):
        @wraps(func)
        def inner (*args, **kwargs):
            log_message = ""
            try:
                # Пытаемся выполнить функцию
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"
                return result  # Возвращаем результат сразу
            except Exception as e:
                # Если произошла ошибка, собираем детали
                log_message = (f"{func.__name__} error: {type(e).__name__}. "
                    f"Inputs: {args}, {kwargs}")
                raise e
            finally:
                if log_message:
                    if filename:
                        with open(filename, "a", encoding="utf-8") as f:
                            f.write(log_message + "\n")
                else:
                    print(log_message)

        return inner

    return wrapper


@log(filename="mylog.txt")
def my_function(x, y):
    return x + y

my_function(1, 2)