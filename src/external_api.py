import os

import requests
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
API_KEY = os.getenv("API_KEY")


def convert_to_rub(transaction: dict) -> float:
    """
    Принимает транзакцию и возвращает сумму в рублях (float).
    Если валюта не RUB, обращается к API для конвертации.
    """
    # Достаем данные из словаря транзакции
    operation_amount = transaction.get("operationAmount", {})
    amount = float(operation_amount.get("amount", 0))
    currency_code = operation_amount.get("currency", {}).get("code")

    # Если валюта уже в рублях, просто возвращаем сумму
    if currency_code == "RUB":
        return amount
    # Если любая другая валюта — конвертируем
    try:
        # Используем эндпоинт /convert для точности
        url = f"https://api.apilayer.com/convert?from={currency_code}&to=RUB&amount={amount}"
        headers = {"apikey": API_KEY}

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверка на ошибки (4xx, 5xx)

        # Превращение JSON-ответ в словарь Python
        data = response.json()
        return float(data.get("result", amount))  # Если в JSON нет result, вернем amount

    # ConnectionError: проблемы с сетью
    except requests.exceptions.ConnectionError:
        print("Connection Error. Please check your network connection.")
        return amount

    # HTTPError: если полученный ответ от сервера не является корректным
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}. Please check the URL.")
        return amount

    # TooManyRedirects: если количество перенаправлений запроса превышает максимально допустимое
    except requests.exceptions.TooManyRedirects:
        print("Too many redirects. Please check the URL.")
        return amount

    # RequestException: базовый класс для всех исключений
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return amount

    # Другие непредвиденные ошибки
    except Exception as e:
        print(f"Ошибка при обращении к API: {e}")
        return amount
