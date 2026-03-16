import src.source as src
import src.task as task_ref
import random
import pytest
import os


def test_generator_api() -> None:
    first = random.randint(10, 1000)
    second = random.randint(10, 1000)

    source_gen = src.RandomSource(first)
    tasks_gen = source_gen.get_tasks()

    source_api = src.APISource(second)
    tasks_api = source_api.get_tasks()

    assert isinstance(source_gen, src.TaskGiver)
    assert isinstance(source_api, src.TaskGiver)

    for task in tasks_gen:
        assert isinstance(task, task_ref.Task)
    for task in tasks_api:
        assert isinstance(task, task_ref.Task)

    assert len(tasks_gen) == first
    assert len(tasks_api) == second


def test_file() -> None:
    '''
    Файл 'tasks.txt' заведомо имеет верный формат.
    '''
    with pytest.raises(ValueError):
        source = src.FileSource("src/main.py")
        source.get_tasks()

    source = src.FileSource("tests/tasks.txt")
    print(source.get_tasks())

    tasks = source.get_tasks()
    assert isinstance(source, src.TaskGiver)
    for task in tasks:
        assert isinstance(task, task_ref.Task)