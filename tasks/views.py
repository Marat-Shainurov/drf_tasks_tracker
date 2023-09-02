from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from tasks.models import Task
from tasks.pagination import TaskPagination
from tasks.serializers import TaskSerializer, ActiveHasParentExecutorSerializer, TaskCreateSerializer


class TaskCreateAPIView(generics.CreateAPIView):
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_task = serializer.save()
        new_task.owner = self.request.user
        new_task.save()


class TaskListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = TaskPagination


class TaskActiveListAPIView(generics.ListAPIView):
    """
    Returns a list of active Task objects.
    Active tasks have 'created' and 'in_progress' as their status value.
    """
    serializer_class = TaskSerializer
    queryset = Task.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]
    pagination_class = TaskPagination


class TaskActiveHasParentList(generics.ListAPIView):
    """
    Returns a list of active Task objects, that have their parent tasks.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TaskPagination

    def get_queryset(self, *args, **kwargs):
        return Task.objects.filter(is_active=True, parent_task__isnull=False)


class ActiveHasParentExecutorList(generics.ListAPIView):
    """
    Returns a list of active Task objects, that have their parent tasks,
    and the 'employee_for_task' field, which offers the most suitable employee for the task.
    'employee_for_task' is chosen between the less loaded employee and the parent task executor.
    ./employees/services/get_most_available_executor function is used to pick the executor.
    """
    serializer_class = ActiveHasParentExecutorSerializer
    queryset = Task.objects.filter(is_active=True, parent_task__isnull=False, executor__isnull=True)
    permission_classes = [IsAuthenticated]
    pagination_class = TaskPagination


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
