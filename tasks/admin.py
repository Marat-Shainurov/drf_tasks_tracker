from django.contrib import admin

from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'parent_task', 'executor', 'owner', 'status', 'deadline', 'is_active',
                    'in_progres_from', 'execution_date')
    search_fields = ('title', 'executor', 'owner', 'status')
    filter_field = ('executor', 'owner', 'status', 'deadline', 'is_active')
