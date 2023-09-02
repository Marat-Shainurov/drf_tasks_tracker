from django.db.models import Count
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from employees.models import Employee
from employees.pagination import EmployeePagination
from employees.serializers import EmployeeSerializer, EmployeeBusynessSerializer


class EmployeeCreateAPIView(generics.CreateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]


class EmployeeListAPIView(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = EmployeePagination


class EmployeeBusynessListAPIView(generics.ListAPIView):
    """
    Returns a list of employees ordered by the number of assigned tasks (descending ordering),
    with 'executor_tasks' field, which contains a list of assigned tasks for each employee.
    """
    serializer_class = EmployeeBusynessSerializer
    queryset = Employee.objects.annotate(tasks_count=Count('executor_tasks')).order_by('-tasks_count')
    permission_classes = [IsAuthenticated]
    pagination_class = EmployeePagination


class EmployeeRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    permission_classes = [IsAuthenticated]


class EmployeeUpdateAPIView(generics.UpdateAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    permission_classes = [IsAuthenticated]


class EmployeeDeleteAPIView(generics.DestroyAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    permission_classes = [IsAdminUser]
