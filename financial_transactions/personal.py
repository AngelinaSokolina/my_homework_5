import pandas as pd
from pathlib import Path

"""Пользователь вводит свой id, чтобы посмотреть информацию о счете"""

df = pd.read_excel(Path(__file__).parent / 'transactions_excel.xlsx')

def speak_question()-> None:
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
