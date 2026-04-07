import pytest
import random
from src.task import Task
from src.queue import TaskQueue
from src.exceptions import TaskError
from src.source import RandomSource


def test_task_queue():
    amount = random.randint(10,500)
    source = RandomSource(amount)
    tasks = source.get_tasks()

    collection = TaskQueue()
    for task in tasks:
        collection.add_task(task)
    
    i = 0
    for task in collection:
        assert task == tasks[i]
        i += 1
    assert amount == i
    collection.delete(collection.tasks[random.randint(0, amount - 1)])
    assert len(list(collection)) == amount - 1

    non_existing_task = Task("task_-1", "description", 1)
    with pytest.raises(TaskError):
        collection.delete(non_existing_task)
    
    assert collection.find(non_existing_task) is None
    some_task = collection.tasks[random.randint(0, amount - 1)]
    assert collection.find(some_task.id) == some_task
    with pytest.raises(TaskError):
        collection.add_task(some_task)