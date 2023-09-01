from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from employees.models import Employee
from tasks.models import Task
from tasks.serializers import ExecutorTasksSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            'id', 'name', 'surname', 'patronymic', 'full_name', 'position', 'employment_date', 'dismissal_date',
            'is_active',
        )

    def get_full_name(self, employee):
        return f'{employee.surname} {employee.name} {employee.patronymic if employee.patronymic else ""}'


class EmployeeBusynessSerializer(serializers.ModelSerializer):
    tasks_count = SerializerMethodField()
    executor_tasks = ExecutorTasksSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = (
            'id', 'surname', 'name', 'position', 'employment_date', 'tasks_count', 'executor_tasks')

    def get_tasks_count(self, employee):
        if Task.objects.filter(executor=employee, is_active=True).exists():
            return Task.objects.filter(executor=employee, is_active=True).count()
        else:
            return 0
