from pathlib import Path

import pandas as pd

"""Разработчик или сотрудник смотрит информацию по счетам для сводки и статистики"""


def load_data(file_path: str | Path) -> list[dict]:
    """Загружает данные из CSV и возвращает список словарей"""
    df = pd.read_csv(file_path, sep=';')
    return df.to_dict('records')


def get_dataframe(file_path: str | Path) -> pd.DataFrame:
    """Загружает данные из CSV и возвращает DataFrame (для аналитики)"""
    return pd.read_csv(file_path, sep=';')


# Вызов функции
df = load_data(Path(__file__).parent / 'transactions.csv')

# Какие вообще есть столбцы в документе
# print(df.columns.tolist())


def count_by_status(data: list[dict]) -> dict:
    """Сколько операций выполнено, в ожидании, отменены"""
    df = pd.DataFrame(data)
    return {
        'Выполненных операций': len(df[df.state == 'EXECUTED']),
        'Операций "в ожидании"': len(df[df.state == 'PENDING']),
        'Отмененные операции': len(df[df.state == 'CANCELED']),
    }


def count_by_description(data: list[dict], status: str) -> dict:
    """Сколько и какие именно операции: EXECUTED, PENDING, CANCELED"""
    df = pd.DataFrame(data)
    # Фильтр по переданному статусу
    filtered_df = df[df.state == status]

    # Уникальные значения в столбце description
    unique_list = df.description.unique()

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
        'Описание отсутствует': unknown,
    }


def get_currency_rating(data: list[dict], top: int = 10) -> pd.Series:
    """Рейтинг валют в денежных операциях"""
    df = pd.DataFrame(data)
    return df['currency_code'].value_counts().head(top)


if __name__ == '__main__':
    data = load_data(Path(__file__).parent / 'transactions.csv')
    print(count_by_status(data))
    print(count_by_description(data, 'EXECUTED'))
    print(count_by_description(data, 'PENDING'))
    print(count_by_description(data, 'CANCELED'))
    print(get_currency_rating(data, top=10))
