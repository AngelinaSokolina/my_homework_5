import json
from pathlib import Path

file_path = Path(__file__).parent.parent / 'data' / 'operations.json' #.parent - "выход повыше", то есть сначала вышли из src, потом в корень, а потом по заданному маршруту

def reception_json(path: str | Path) -> list:
    """ Принимает путь до JSON-файла и возвращает список словарей"""
    # Проверяем, существует ли файл вообще
    if not Path(path).exists():
        return []

    try:
        with open(path, 'r', encoding='utf-8') as file:
            # Пробуем прочитать данные
            data = json.load(file)

            # Проверяем, что внутри именно список
            if isinstance(data, list):
                return data
            else:
                return []
    except (json.JSONDecodeError, FileNotFoundError):
        # Если файл пустой, поврежден или не найден — возвращаем пустой список
        return []

