from src.source import RandomSource, TaskGiver
from src.constants import COMMANDS, STATUS_LIST
from src.task import TaskQueue
import shlex


def main() -> None:
    print("Available commands:\n1. add-task\n2. show-tasks\n3. change-task-status\n4. available-statuses")
    task_queue = TaskQueue()
    while inp := input():
        if inp not in COMMANDS and inp != "available-statuses": continue
        match inp:
            case "add-task":
                tasks_rnd = RandomSource(1)
                if isinstance(tasks_rnd, TaskGiver):
                    task_queue.add_task(tasks_rnd.get_tasks())
                    print("Initiated task with generator")
            case "show-tasks":
                if not task_queue:
                    print("No active tasks")
                else:
                    for task in task_queue:
                        print(f"{task.id}: {task.description}. Priority - {task.priority}, status: {task.status}")
            case "change-task-status":
                print("Enter the task id")
                id = str(input())
                task_exists = False
                for task in task_queue:
                    if task.id == id:
                        print("Enter new status")
                        new_status = str(input())
                        task.status = new_status
                        task_exists = True
                        print("Successful")
                        break
                if not task_exists: raise ValueError("No such task")
            case "available-statuses":
                print(", ".join(STATUS_LIST))



if __name__ == "__main__":
    main()