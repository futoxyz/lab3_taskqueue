from src.source import RandomSource, TaskGiver
from src.constants import COMMANDS
import shlex


def main() -> None:
    print("Available commands:\n1. add-task\n2. show-tasks\n3. change-task-status")
    task_list: list[Task] = []
    while inp := input():
        if inp not in COMMANDS: continue
        match inp:
            case "add-task":
                tasks_rnd = RandomSource(1)
                if isinstance(tasks_rnd, TaskGiver):
                    task_list += tasks_rnd.get_tasks()
                    print("Initiated task with generator")
            case "show-tasks":
                if not task_list:
                    print("No active tasks")
                else:
                    for task in task_list:
                        print(f"{task.id}: {task.description}. Priority - {task.priority}, status: {task.status}")
            case "change-task-status":
                print("Enter the task id")
                id = str(input())
                task_exists = False
                for task in task_list:
                    if task.id == id:
                        print("Enter new status")
                        new_status = str(input())
                        task.status = new_status
                        task_exists = True
                        break
                if not task_exists: raise ValueError("No such task")




if __name__ == "__main__":
    main()