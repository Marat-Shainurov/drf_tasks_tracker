from django.db import models
from rest_framework.exceptions import ValidationError

from employees.models import Employee
from tasks.services import check_tasks_chain_status
from users.models import CustomUser, NULLABLE


class Task(models.Model):
    STATUS_CHOICES = [('created', 'Created'), ('in_progress', 'In_progress'), ('done', 'Done')]

    title = models.CharField(max_length=50, verbose_name='task_title', unique=True)
    description = models.TextField(verbose_name='task_description')
    parent_task = models.ForeignKey('self', verbose_name='parent_task', related_name='child_tasks',
                                    on_delete=models.CASCADE, **NULLABLE)
    executor = models.ForeignKey(Employee, verbose_name='task_executor', on_delete=models.RESTRICT,
                                 related_name='executor_tasks')
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, verbose_name='task_owner', **NULLABLE,
                              related_name='task_owner')
    status = models.CharField(max_length=11, verbose_name='task_status', choices=STATUS_CHOICES, default='created')
    deadline = models.DateTimeField(verbose_name='task_deadline')
    is_active = models.BooleanField(verbose_name='task_activity_flag', default=True)

    def __str__(self):
        return self.title

    def clean_status(self):
        if not self.is_active:
            msg = 'You cannot change the status value of an inactive task. Activate the task or create a new one'
            raise ValidationError(msg)
        elif self.status == 'done' and not check_tasks_chain_status(self):
            raise ValidationError(f'Not all the child tasks of the {self} task are done yet!')
        elif self.status == 'done':
            self.is_active = False

    def save(self, *args, **kwargs):
        self.clean_status()
        super().save(args, **kwargs)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
