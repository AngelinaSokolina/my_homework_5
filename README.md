# Проект: Банковские операции (обработка данных)

## Описание
Этот проект предназначен для фильтрации и сортировки банковских транзакций. 
Он содержит инструменты для маскировки номеров карт/счетов, а также функции для обработки списков данных по их статусу и дате.

## Состав модулей
*   `src/processing.py` — функции фильтрации и сортировки данных.
*   `src/masks.py` — функции маскировки номеров банковских карт и счетов.
*   `src/widget.py` — дополнительные инструменты для обработки дат и типов карт.

## Установка
1. Клонируйте репозиторий:
```
git clone git@github.com:AngelinaSokolina/my_homework_3.git
```
**Установите зависимости через Poetry:**
```
poetry install
```
## Использование
**Фильтрация по статусу**
Функция `filter_by_state` возвращает список словарей с заданным статусом (по умолчанию EXECUTED):
```
from src.processing import filter_by_state

data = [
    {'id': 1, 'state': 'EXECUTED', 'date': '2019-07-03'},
    {'id': 2, 'state': 'CANCELED', 'date': '2018-06-30'}
]
result = filter_by_state(data, 'EXECUTED')
```

**Сортировка по дате**

Функция `sort_by_date` сортирует данные по дате (по умолчанию от новых к старым):
```
from src.processing import sort_by_date

result = sort_by_date(data, reverse=True)
```
## Тестирование
В проекте реализовано модульное тестирование с использованием `pytest`.
- Для запуска тестов используйте команду: 

`poetry run pytest`.
- Для просмотра покрытия тестами : 

`poetry run pytest --cov=src`
- Покрытие тестами составляет 94% (отчет доступен в папке `htmlcov`).
- Для генерации отчета о покрытии: 

`poetry run pytest --cov=src --cov-report html`.
- Проект поддерживает проверку типов через mypy и соблюдение стиля PEP 8 через flake8.
Для запуска проверок используйте:
```
poetry run flake8 src
poetry run flake8 tests
poetry run mypy src
poetry run mypy tests
```

## Как сохранить это на GitHub:

Так как вы всё еще находитесь в ветке задачи, сохраним изменения в неё же:

1. Добавьте файл и закоммитьте:
```
   git add README.md
   git commit -m "Update README with usage instructions"
```
2. Отправьте в облако:
```
git push origin feature/processing
```
