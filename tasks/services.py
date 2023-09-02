from rest_framework.exceptions import ValidationError


def check_tasks_chain_status(task):
    """
    arg: task: Task
    returns: bool
    Recursive service functions that checks whether each child task of the passed argument has the 'done' status.
    """
    try:
        child_tasks = task.child_tasks.all()
    except ValueError:
        raise ValidationError("A task can't be 'done' while its creation!")
    if child_tasks.exists():
        all_child_tasks_done = all(check_tasks_chain_status(child_task) for child_task in child_tasks)
        if all_child_tasks_done and all(child_task.status == 'done' for child_task in child_tasks):
            return True
        else:
            return False
    else:
        return True
