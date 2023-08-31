from rest_framework.exceptions import ValidationError


def check_tasks_chain_status(task):
    child_tasks = task.child_tasks.all()
    if child_tasks.exists():
        all_child_tasks_done = all(check_tasks_chain_status(child_task) for child_task in child_tasks)
        if all_child_tasks_done and all(child_task.status == 'done' for child_task in child_tasks):
            return True
        else:
            return False
    else:
        return True
