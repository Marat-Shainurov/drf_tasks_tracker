from django.urls import path

from tasks.apps import TasksConfig
from tasks.views import TaskListAPIView, TaskCreateAPIView, TaskRetrieveAPIView, TaskUpdateAPIView, TaskDeleteAPIView, \
    TaskActiveListAPIView, TaskActiveHasParentList, ActiveHasParentExecutorList

app_name = TasksConfig.name

urlpatterns = [
    path('tasks/', TaskListAPIView.as_view(), name='tasks_list'),
    path('tasks/active/', TaskActiveListAPIView.as_view(), name='active_tasks_list'),
    path('tasks/active/with-parents/', TaskActiveHasParentList.as_view(),
         name='active_tasks_has_parent_list'),
    path('tasks/active/with-parents/with-executor/', ActiveHasParentExecutorList.as_view(),
         name='active_tasks_has_parent_list'),
    path('tasks/create/', TaskCreateAPIView.as_view(), name='tasks_create'),
    path('tasks/retrieve/<int:pk>/', TaskRetrieveAPIView.as_view(), name='tasks_retrieve'),
    path('tasks/update/<int:pk>/', TaskUpdateAPIView.as_view(), name='tasks_update'),
    path('tasks/delete/<int:pk>/', TaskDeleteAPIView.as_view(), name='tasks_delete'),
]
