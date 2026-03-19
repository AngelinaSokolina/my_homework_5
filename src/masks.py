import logging
from pathlib import Path

# Путь логгера
log_dir = Path(__file__).parent.parent / 'logs'

# Создание логов
logger = logging.getLogger('masks')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_dir / 'masks.log', mode='w', encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера банковской карты"""
    logger.info('Запуск функции маскировки номера банковской карты')

    # Очищаем строку от возможных пробелов (на всякий случай)
    card_number = card_number.strip()

    # Проверяем условия, потому что недоверяем вводу пользователя
    if not card_number.isdigit() or len(card_number) != 16:
        logger.error('Введено неверное количество цифр номера карты')

        return "Ошибка: номер карты должен состоять из 16 цифр"

    # Если всё ок, маскируем
    mask_card = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"

    return mask_card


def get_mask_account(account_number: str) -> str:
    """Функция маскировки номера банковского счета"""
    logger.info('Запуск маскировки номера банковского счета')

    # Очистка от пробелов
    account_number = account_number.strip()

    # Проверяем условия ввода пользователя
    if not account_number.isdigit() or len(account_number) != 20:
        logger.error('Введено неверное количество цифр номера карты')

        return "Ошибка: номер счета должен состоять из 20 цифр"

    # Если всё ок, маскируем
    mask_account = f"**{account_number[-4:]}"

    return mask_account
