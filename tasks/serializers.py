from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from tasks.models import Task
from employees.services import get_most_available_executor
from tasks.validators import IsDeadlineOk


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'parent_task', 'executor', 'owner', 'status', 'deadline')
        validators = [IsDeadlineOk('deadline')]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'parent_task', 'executor', 'owner', 'status', 'deadline', 'is_active')


class ExecutorTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'parent_task', 'status', 'deadline')


class ActiveHasParentExecutorSerializer(serializers.ModelSerializer):
    employee_for_task = SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'title', 'deadline', 'parent_task', 'employee_for_task')

    @staticmethod
    def get_employee_for_task(task):
        return [get_most_available_executor(task)]
