from pathlib import Path
import pandas as pd
import re

def excel_data(file_path: str | Path) -> list[dict]:
    """Загружает данные из Excel и возвращает список словарей."""
    df = pd.read_excel(file_path)
    data = df.to_dict('records')
    return data


def process_bank_search(data:list[dict], search:str)->list[dict]:
    """Функция для поиска банковских операций"""
    finance_dict = []
    for row in data:
        description = str(row.get("description", ""))
        if re.search(search, description, re.IGNORECASE):
            finance_dict.append(row)

    return finance_dict


if __name__ == '__main__':
    # Загрузка данных
    data = excel_data(Path(__file__).parent.parent / 'financial_transactions' / 'transactions_excel.xlsx')

    # Поиск операции "Перевод"
    result = process_bank_search(data, "Перевод")

    # Результат
    print(f"Найдено {len(result)} операций")