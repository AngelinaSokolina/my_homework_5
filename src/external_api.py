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

    # Если валюта USD или EUR, идем в API
    if currency_code in ["USD", "EUR"]:
        try:
            # Используем эндпоинт /convert для точности
            url = f"https://api.apilayer.com{currency_code}&amount={amount}"
            headers = {"apikey": API_KEY}

            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Проверка на ошибки (4xx, 5xx)

            data = response.json()
            return float(data.get("result", 0))

        except Exception as e:
            print(f"Ошибка при обращении к API: {e}")
            return 0.0

    return 0.0
