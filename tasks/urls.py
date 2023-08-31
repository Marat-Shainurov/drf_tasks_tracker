from django.urls import path

from tasks.apps import TasksConfig
from tasks.views import TaskListAPIView, TaskCreateAPIView, TaskRetrieveAPIView, TaskUpdateAPIView, TaskDeleteAPIView, \
    TaskActiveListAPIView, TaskNotDoneHasParentListAPIView

app_name = TasksConfig.name

urlpatterns = [
    path('tasks/', TaskListAPIView.as_view(), name='tasks_list'),
    path('active-tasks/', TaskActiveListAPIView.as_view(), name='active_tasks_list'),
    path('active-tasks-with-parents/', TaskNotDoneHasParentListAPIView.as_view(),
         name='active_tasks_has_parent_list'),
    path('tasks/create/', TaskCreateAPIView.as_view(), name='tasks_create'),
    path('tasks/retrieve/<int:pk>/', TaskRetrieveAPIView.as_view(), name='tasks_retrieve'),
    path('tasks/update/<int:pk>/', TaskUpdateAPIView.as_view(), name='tasks_update'),
    path('tasks/delete/<int:pk>/', TaskDeleteAPIView.as_view(), name='tasks_delete'),
]
