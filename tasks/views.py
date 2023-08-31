from rest_framework import generics

from tasks.models import Task
from tasks.serializers import TaskSerializer, ActiveHasParentExecutorSerializer


class TaskCreateAPIView(generics.CreateAPIView):
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        new_task = serializer.save()
        new_task.owner = self.request.user
        new_task.save()


class TaskListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TaskActiveListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.filter(is_active=True)


class TaskActiveHasParentList(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self, *args, **kwargs):
        return Task.objects.filter(is_active=True, parent_task__isnull=False)


class ActiveHasParentExecutorList(generics.ListAPIView):
    serializer_class = ActiveHasParentExecutorSerializer
    queryset = Task.objects.filter(is_active=True, parent_task__isnull=False, executor__isnull=True)


class TaskRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TaskUpdateAPIView(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TaskDeleteAPIView(generics.DestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
