from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from tasks.models import Task
from tasks.serializers import TaskSerializer, ActiveHasParentExecutorSerializer


class TaskCreateAPIView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_task = serializer.save()
        new_task.owner = self.request.user
        new_task.save()


class TaskListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]


class TaskActiveListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]


class TaskActiveHasParentList(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return Task.objects.filter(is_active=True, parent_task__isnull=False)


class ActiveHasParentExecutorList(generics.ListAPIView):
    serializer_class = ActiveHasParentExecutorSerializer
    queryset = Task.objects.filter(is_active=True, parent_task__isnull=False, executor__isnull=True)
    permission_classes = [IsAuthenticated]


class TaskRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]


class TaskUpdateAPIView(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]


class TaskDeleteAPIView(generics.DestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAdminUser]
