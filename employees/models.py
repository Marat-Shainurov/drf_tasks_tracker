from django.db import models

from users.models import NULLABLE


class Employee(models.Model):
    name = models.CharField(max_length=50, verbose_name='employee_name')
    surname = models.CharField(max_length=50, verbose_name='employee_surname')
    patronymic = models.CharField(max_length=50, verbose_name='employee_patronymic', **NULLABLE)
    position = models.CharField(max_length=100, verbose_name='employee_position')
    employment_date = models.DateField(verbose_name='employment_date', auto_now_add=True)
    dismissal_date = models.DateField(verbose_name='dismissal_date', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='is_employee_active')

    def __str__(self):
        return f'{self.surname} {self.name}'

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
