from pathlib import Path

import pandas as pd


# df = pd.read_excel(Path(__file__).parent / 'transactions_excel.xlsx')

def load_excel_data(file_path: str | Path) -> list[dict]:
    """Загружает данные из Excel и возвращает список словарей."""
    df = pd.read_excel(file_path)
    return df.to_dict('records')

def speak_question(data: list[dict]) -> None:
    """Пользователь вводит свой id, чтобы посмотреть информацию о счете"""
    df = pd.DataFrame(data)

    while True:
        question = input("Если вы хотите узнать информацию о счете, введите свой id: ")
        try:
            user_id = int(question)
            mask = df['id'] == user_id
            if mask.any():
                print(df.loc[mask])
                break
            else:
                print('Извините, введенный id не найден')
        except ValueError:
            print('Ввод неверный! Введите только цифры без пробелов')

if __name__ == '__main__':
    data = load_excel_data(Path(__file__).parent / 'transactions_excel.xlsx')
    speak_question(data)