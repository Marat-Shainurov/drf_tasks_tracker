from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from employees.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            'id', 'name', 'surname', 'patronymic', 'position', 'employment_date', 'dismissal_date', 'is_active',
            'full_name'
        )

    def get_full_name(self, employee):
        return f'{employee.surname} {employee.name} {employee.patronymic if employee.patronymic else ""}'
