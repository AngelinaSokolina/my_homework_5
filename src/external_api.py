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
        return float(data.get("result", amount)) # Если в JSON нет result, вернем amount

    except Exception as e:
        print(f"Ошибка при обращении к API: {e}")
        return amount
