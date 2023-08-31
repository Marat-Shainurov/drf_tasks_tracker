from django.db.models import Count

from employees.models import Employee
from tasks.models import Task


def get_most_available_executor(task):
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
