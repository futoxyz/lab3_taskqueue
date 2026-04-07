# Лабораторная работа №3. Очередь задач: итераторы и генераторы
## Запуск uv
```
uv sync
uv venv
```
Для Windows
```
.venv\scripts\Activate
```
Для Linux/MacOS
```
source .venv\Scripts\activate
```
# Задачи
см. [прошлую ЛР](https://github.com/futoxyz/lab2_descriptors)

# Очередь задач
`src\queue.py`
TaskQueue — класс с поддержкой итерации базовых методов Python. Методы очереди:
- **add_task** — Добавить задачу. Очередь не поддерживает таски с одинаковым id.
- **find** — Поиск задачи по id, если задача не найдена возвращает *None*.
- **delete** — Удаление задачи.
- **filter_by_priority** — Фильтр по указанному приоритету.
- **filter_by_status** — Фильтр по указанному статусу.
- **filter_by_date** — Фильтр по крайней указанной дате. Принимает на вход объект *datetime*.
- **filter_by_days** — Фильтр по крайнему указанному целому количеству дней. Принимает на вход лишь число.

# Функция main
Доступны 6 команд: `add-task`, `show-tasks`, `change-task-status` **+** `available-statuses`, `filter-by-priority`, `filter-by-status`

Работает с очередью задач. создаются через генератор, ошибки ввода попадаются валидаторами.

# Запуск тестов
С помощью pytest
```
pytest .
```