import re
from pathlib import Path
import pandas as pd

def excel_data_operation(file_path: str | Path) -> list[dict]:
    """Загружает данные из Excel и возвращает список словарей"""
    df = pd.read_excel(file_path)
    data = df.to_dict('records')
    return data


def process_bank_operations(data:list[dict], categories:list)->dict:
    """Функция для группировки по категориям"""
    ok_dict = {categ: 0 for categ in categories}
    for row in data:
        description = str(row.get("description", ""))
        for categ in categories:
            if re.search(categ, description, re.IGNORECASE):
                ok_dict[categ] += 1

    return ok_dict



if __name__ == '__main__':
    # Загрузка данных
    data = excel_data_operation(Path(__file__).parent.parent / 'financial_transactions' / 'transactions_excel.xlsx')
    categories = ["Перевод организации", "Перевод с карты на карту", "Открытие вклада", "Перевод со счета на счет"]
    stats = process_bank_operations(data, categories)
    print(stats)
