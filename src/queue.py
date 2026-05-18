from src.task import Task
from src.exceptions import TaskError
from datetime import datetime


class TaskIterator:
    def __init__(self, tasks: dict[str, Task]):
        self._tasks = tasks
        self._keys = list(tasks.keys())
        self._index = 0

    def __next__(self):
        if self._index >= len(self._keys):
            raise StopIteration
        current_key = self._keys[self._index]
        self._index += 1
        return self._tasks[current_key]

    def __iter__(self):
        return self


class TaskQueue:
    def __init__(self, tasks: list[Task] | None = None):
        self._tasks: dict[str, Task] = {t.id: t for t in tasks} if tasks else {}

    def __iter__(self):
        return TaskIterator(self._tasks)

    def __len__(self):
        return len(self._tasks)

    def find(self, id: str) -> Task | None:
        return self._tasks.get(id)

    def add_task(self, task: Task):
        if task.id in self._tasks:
            raise TaskError(task, 1)
        self._tasks[task.id] = task

    def delete(self, task_del: Task):
        if task_del.id in self._tasks:
            del self._tasks[task_del.id]
        else:
            raise TaskError(task_del, 0)

    def filter_by_priority(self, priority: int):
        for task in self:
            if task.priority == priority:
                yield task

    def filter_by_date(self, min_date: datetime):
        '''
        Для фильтра через данные datetime. Результат: таски, созданные ранее указанной даты.
        '''
        for task in self:
            if task.created_at >= min_date:
                yield task

    def filter_by_days(self, days: int):
        '''
        Для фильтра по количеству дней. Результат: таски, с создания которых прошло меньше указанных дней.
        '''
        for task in self:
            if (datetime.now() - task.created_at).days <= days:
                yield task

    def filter_by_status(self, status: str):
        for task in self:
            if task.status == status:
                yield task
