import json
import logging
from pathlib import Path

file_path = (
    Path(__file__).parent.parent / 'data' / 'operations.json'
)  # .parent - "выход повыше", то есть сначала вышли из src, потом в корень, а потом по заданному маршруту

# Путь логгера
log_dir = Path(__file__).parent.parent / 'logs'

# Создание логов
logger = logging.getLogger('utils')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_dir / 'utils.log', mode='w', encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def reception_json(path: str | Path) -> list:
    """Принимает путь до JSON-файла и возвращает список словарей"""
    logger.info('Запуск функции обработки пути и возвращения списка словарей')

    # Проверяем, существует ли файл вообще
    if not Path(path).exists():
        # Сообщение логера
        logger.error(f'Файл {path} не существует')
        return []

    try:
        with open(path, 'r', encoding='utf-8') as file:
            # Пробуем прочитать данные
            data = json.load(file)
            # Проверяем, что внутри именно список
            if isinstance(data, list):
                logger.info(f'Файл {path} успешно загружен, получен список из {len(data)} элементов')
                return data
            else:
                logger.error(f'Файл {data} не является списком')
                return []
    except (json.JSONDecodeError, FileNotFoundError) as ex:
        logger.error(f'Файл пустой, поврежден или не найден. Произошла ошибка: {ex}.')
        # Если файл пустой, поврежден или не найден — возвращаем пустой список
        return []
