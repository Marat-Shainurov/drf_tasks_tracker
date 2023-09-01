from django.urls import path

from employees.apps import EmployeesConfig
from employees.views import EmployeeListAPIView, EmployeeCreateAPIView, EmployeeUpdateAPIView, EmployeeDeleteAPIView, \
    EmployeeBusynessListAPIView

app_name = EmployeesConfig.name

urlpatterns = [
    # CRUD
    path('employees/', EmployeeListAPIView.as_view(), name='employees_list'),
    path('employees/create/', EmployeeCreateAPIView.as_view(), name='employees_create'),
    path('employees/retrieve/<int:pk>/', EmployeeListAPIView.as_view(), name='employees_retrieve'),
    path('employees/update/<int:pk>/', EmployeeUpdateAPIView.as_view(), name='employees_update'),
    path('employees/delete/<int:pk>/', EmployeeDeleteAPIView.as_view(), name='employees_delete'),

    # adds the tasks counter and a list of each employee's active tasks
    path('employees/busyness/', EmployeeBusynessListAPIView.as_view(), name='employees_busyness_list'),
]
