from django.db.models import Count

from employees.models import Employee
from tasks.models import Task


def get_most_available_executor(task):
    """
    arg: task: Task
    returns: str
    Returns the most suitable employee for the passed task, in terms of current workload.
    It is either the less busy employee (with minimal number of assigned tasks) or the parent's task executor (if the
    difference between his/her number of task and the less busy employee's number of tasks is <= 2).
    """
    ordered_employees = Employee.objects.annotate(tasks_count=Count('executor_tasks')).order_by('-tasks_count')
    less_busy_employee = ordered_employees.last()
    less_busy_tasks = Task.objects.filter(executor=less_busy_employee).count()

    parent_task = task.parent_task
    parent_task_executor = parent_task.executor
    parent_executor_tasks = Task.objects.filter(executor=parent_task_executor).count()

    if (int(parent_executor_tasks) - int(less_busy_tasks)) <= 2:
        return str(parent_task_executor)
    else:
        return str(less_busy_employee)
