import pytest
from time import sleep
from src.task import Task
from src.exceptions import IntegerError, StringError, StatusError


def test_tasks() -> None:
    '''
    Тесты дескрипторов.
    '''
    with pytest.raises(StringError): # Id and description test
        task = Task("", "description")
    with pytest.raises(StringError):
        task = Task(0, "description")
    with pytest.raises(StringError):
        task = Task("some_id", "")
    with pytest.raises(StringError):
        task = Task("some_id", 1)

    with pytest.raises(IntegerError): # Priority test
        task = Task("some_id", "description", -1)
    with pytest.raises(IntegerError):
        task = Task("some_id", "description", "priority_1")

    normal_task = Task("id_1", "description", 1)
    assert normal_task.status == "pending"
    with pytest.raises(StatusError):
        normal_task.status = "can't be a status"
    with pytest.raises(StatusError):
        normal_task.status = 1010101
    normal_task.status = "in_progress"
    assert normal_task.status == "in_progress"

    with pytest.raises(IntegerError):
        normal_task.priority = -1
    with pytest.raises(IntegerError):
        normal_task.priority = "string"


def test_age_measurement() -> None:
    task = Task("id", "description")
    time_exist: float = 0.75
    sleep(time_exist)
    assert abs(task.age_seconds - time_exist) < 0.5 # Погрешность