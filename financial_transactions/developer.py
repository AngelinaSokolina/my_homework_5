import pandas as pd
from pathlib import Path

"""Разработчик или сотрудник смотрит инфомацию по счетам для сводки и статистики"""

# Функция загрузки данных из csv

def load_data(file_path) -> pd.DataFrame:
    df_clin = pd.read_csv(file_path, sep=';')
    return df_clin

# Вызов функции
df = load_data(Path(__file__).parent / 'transactions.csv')


"""Какие вообще есть столбцы в документе"""
# print(df.columns.tolist())


"""Сколько операций выполнено, в ожидании, отменены"""

def count_by_status(df):
    return {
        'Выполненных операций': len(df[df.state == 'EXECUTED']),
        'Операций "в ожидании"': len(df[df.state == 'PENDING']),
        'Отмененные операции': len(df[df.state == 'CANCELED'])
    }


# Уникальные значения в столбце description
unique_list = df.description.unique()

"""Сколько и какие именно операции: EXECUTED, PENDING, CANCELED"""

def count_by_description(df, status):
    # Фильтр по переданному статусу
    filtered_df = df[df.state == status]

    # Общее количество
    total = len(filtered_df)

    # Счет по типам описаний
    # (используем unique_list, который определён снаружи)
    organization = len(filtered_df[filtered_df.description == unique_list[0]])
    from_card = len(filtered_df[filtered_df.description == unique_list[1]])
    opening_deposit = len(filtered_df[filtered_df.description == unique_list[2]])
    from_account = len(filtered_df[filtered_df.description == unique_list[3]])
    unknown = len(filtered_df[filtered_df.description.isna()])

    return {
        'Общее количество': total,
        'Перевод организации': organization,
        'Перевод с карты на карту': from_card,
        'Открытие вклада': opening_deposit,
        'Перевод со счета на счет': from_account,
        'Описание отсутствует': unknown
    }


"""Рейтинг валют в денежных операциях"""

def get_currency_rating(df, top):
    currency_rating = df['currency_code'].value_counts().head(top)
    return currency_rating

if __name__ == '__main__':
    print(count_by_status(df))
    print(count_by_description(df, 'EXECUTED'))
    print(count_by_description(df, 'PENDING'))
    print(count_by_description(df, 'CANCELED'))
    print(get_currency_rating(df, top=10))
