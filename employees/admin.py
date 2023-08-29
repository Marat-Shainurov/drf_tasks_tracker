from django.contrib import admin

from employees.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'patronymic', 'position', 'employment_date', 'dismissal_date', 'is_active')
    search_fields = ('surname', 'position',)
    filter_fields = ('surname', 'employment_date', 'dismissal_date', 'position', 'is_active')
