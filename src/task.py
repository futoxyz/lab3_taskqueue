from datetime import datetime
from typing import Any
from src.constants import STATUS_LIST


class IntegerError(Exception):
    def __init__(self, name: Any, type: int = -1):
        match type:
            case 0:
                super().__init__(f"{name} is not an integer!")
            case 1:
                super().__init__(f"{name} can't be negative!")
            case _:
                super().__init__(f"Undefined type given: {name}")


class PositiveInteger:
    def __init__(self, name: str):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise IntegerError(self.name, 0)
        if value < 0:
            raise IntegerError(self.name, 1)

        instance.__dict__[self.name] = value


class StringError(Exception):
    def __init__(self, name: Any, type: int = -1):
        match type:
            case 0:
                super().__init__(f"{name} is not a string!")
            case 1:
                super().__init__(f"{name} can't be an empty line!")
            case _:
                super().__init__(f"Undefined type given: {name}")


class StrValidation:
    def __init__(self, name: str):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise StringError(self.name, 0)
        if value == "":
            raise StringError(self.name, 1)
        instance.__dict__[self.name] = value


class StatusError(Exception):
    def __init__(self, value: Any):
            super().__init__(f"\"{value}\" can't be used as a status!")


class Task:
    id = StrValidation("_id")
    description = StrValidation("_payload")
    priority = PositiveInteger("_priority")

    def __init__(
            self,
            id: str,
            description: str,
            priority: int = 0,
    ):
        self.id = id
        self.description = description
        self.priority = priority
        self.created_at = datetime.now()
        self._status = "pending"

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        if value not in STATUS_LIST:
            raise StatusError(value)
        self._status = value

    @property
    def age_seconds(self) -> float:
        return (datetime.now() - self.created_at).total_seconds()


class TaskQueueError(Exception):
    def __init__(self, value: Any, type: int = -1):
        match type:
            case 0:
                super().__init__(f"No such task in queue -> {value}")
            case 1:
                super().__init__(f"Task id must be unique: task with similar id already exists -> {value}")
            case _:
                super().__init__(f"Undefined type given: {value}")


class TaskQueue:
    def __init__(self, tasks: list[Task] | None = None):
        self.tasks: list[Task] = tasks if tasks else []
    
    def find(self, id: str) -> Task | None:
        for task in self:
            if task.id == id:
                return task
        return None
    
    def add_task(self, task: Task):
        if self.find(task.id) is None:
            self.tasks.append(task)
        else:
            raise TaskQueueError(task, 1)
    
    def __iter__(self):
        for task in self.tasks:
            yield task
    
    def delete(self, task_del: Task):
        for task in self:
            if task == task_del:
                self.tasks.remove(task)
                return
        raise TaskQueueError(task, 0)

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