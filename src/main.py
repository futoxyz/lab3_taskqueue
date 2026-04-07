from src.source import RandomSource, TaskGiver
from src.constants import COMMANDS, STATUS_LIST
from src.queue import TaskQueue
from src.exceptions import StatusError
import shlex


def main() -> None:
    print(f"Available commands:\n- {"\n- ".join(COMMANDS)}")
    task_queue = TaskQueue()
    while inp := input():
        if inp not in COMMANDS: continue
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
                        print(f"{task.id}: {task.description}. Priority: {task.priority}, Status: {task.status}")
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
                        print("Status updated")
                        break
                if not task_exists: raise ValueError("No such task")
            case "available-statuses":
                print(", ".join(STATUS_LIST))
            case "filter-by-priority":
                prio_filter = str(input("Enter the priority: "))
                try:
                    prio_filter = int(prio_filter)
                except ValueError:
                    raise ValueError(f"Priority must be integer: \"{prio_filter}\"")
                else:
                    for task in task_queue.filter_by_priority(prio_filter):
                        print(f"{task.id}: {task.description}. Priority: {task.priority}, Status: {task.status}")
            case "filter-by-status":
                filter_status = str(input("Enter the status: "))
                if filter_status not in STATUS_LIST:
                    raise StatusError(filter_status)
                for task in task_queue.filter_by_status(filter_status):
                    print(f"{task.id}: {task.description}. Priority: {task.priority}, Status: {task.status}")



if __name__ == "__main__":
    main()