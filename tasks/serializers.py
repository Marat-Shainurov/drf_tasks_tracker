from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from tasks.models import Task
from employees.services import get_most_available_executor


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'parent_task', 'executor', 'owner', 'status', 'deadline')


class ExecutorTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'parent_task', 'status', 'deadline')


class ActiveHasParentExecutorSerializer(serializers.ModelSerializer):
    employee_for_task = SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'title', 'deadline', 'parent_task', 'employee_for_task')

    def get_employee_for_task(self, task):
        return [get_most_available_executor(task)]
