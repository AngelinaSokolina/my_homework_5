import pandas as pd


"""Пользователь вводит свой id, чтобы посмотреть информацию о счете"""

df = pd.read_excel('transactions_excel.xlsx')


def speak_question()-> None:
    question = int(input("Если вы хотите узнать информацию о счете, введите свой id: "))
    mask = df['id'] == question
    if mask.any():
        print(df.loc[mask])
    else:
        print('Извините, введенный id не найден')
