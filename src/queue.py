from src.task import Task
from src.exceptions import TaskError


class TaskQueue:
    def __init__(self, tasks: list[Task] | None = None):
        self.tasks: list[Task] = tasks if tasks else []

    def __iter__(self):
        for task in self.tasks:
            yield task

    def find(self, id: str) -> Task | None:
        for task in self:
            if task.id == id:
                return task
        return None
    
    def add_task(self, task: Task):
        if self.find(task.id) is None:
            self.tasks.append(task)
        else:
            raise TaskError(task, 1)
    
    def delete(self, task_del: Task):
        for task in self:
            if task == task_del:
                self.tasks.remove(task)
                return
        raise TaskError(task, 0)

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